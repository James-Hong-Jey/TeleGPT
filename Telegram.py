from dotenv import load_dotenv
load_dotenv()
import os
import openai
import re
import emoji

from ChatGPT import *
from Dalle import *
from telegram import ReplyKeyboardMarkup
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TELEGRAM_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")
openai.api_key = os.getenv("OPENAI_API_KEY")

async def personaCommand (update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["/normal", "/malay", "/chinese"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text("Select a language: ", reply_markup=reply_markup)

async def malay (update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You selected Malay")
    context.user_data['persona'] = 'malay'

async def normal (update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You selected Normal")
    context.user_data['persona'] = 'normal'
    
async def chinese (update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You selected Chinese")
    context.user_data['persona'] = 'chinese'

async def image (update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_prompt = update.message.text.split('/image ')[1]
    print(f'User ({update.message.chat.active_usernames}) requested: "{user_prompt}"')
    dalle_response = get_image(user_prompt)
    await update.message.reply_photo(dalle_response)
    
async def modelNameCommand (update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["/good", "/chat", "/big"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text("Select a Model to use: ", reply_markup=reply_markup)

async def good (update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You selected Good (GPT-4)")
    context.user_data['modelName'] = 'good'

async def chat (update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You selected Chat (GPT-3.5-Turbo)")
    context.user_data['modelName'] = 'chat'

async def big (update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You selected Chat (GPT-3.5-Turbo-16k)")
    context.user_data['modelName'] = 'big'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'persona' not in context.user_data:
        context.user_data['persona'] = 'normal'
    if 'modelName' not in context.user_data:
        context.user_data['modelName'] = 'chat'
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    # Authorised Users Only
    username: str = update.message.from_user.username
    allowed_usernames = ["jeysiao", "yuyufrog"]
    if username not in allowed_usernames:
        await update.message.reply_text("Unauthorised user")
        return

    # Check if user is in group or private message
    if message_type == 'group':
        if BOT_USERNAME in text:
            # Remove name from message
            new_text: str = text.replace(BOT_USERNAME, '').strip() 
            chatgpt_response = get_response(new_text, context.user_data['persona'], context.user_data['modelName'])
            response = chatgpt_response.choices[0].message.content
        else: 
            return
    else: 
        # in a private message there will be no name in the message
        chatgpt_response = get_response(text, context.user_data['persona'], context.user_data['modelName'])
        response = chatgpt_response.choices[0].message.content
        
    print('Bot: ', response, ' (Using ', chatgpt_response.usage.total_tokens, ')')
    
    # Split by punctuation, so no punctuation + lower + split up
    emojiless_response = emoji.replace_emoji(response, replace='')
    split_response = re.split(r'[,.!?]+', emojiless_response)
    split_response = [token for token in split_response if token]
    for text in split_response:
        await update.message.reply_text(text.lower().replace('.',''))

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update "{update.message.text}" caused error "{context.error}"')

if __name__ == '__main__':
    print('Starting Bot..')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('persona', personaCommand))
    app.add_handler(CommandHandler('malay', malay))
    app.add_handler(CommandHandler('normal', normal))
    app.add_handler(CommandHandler('chinese', chinese))

    app.add_handler(CommandHandler('modelname', modelNameCommand))
    app.add_handler(CommandHandler('good', good))
    app.add_handler(CommandHandler('chat', chat))
    app.add_handler(CommandHandler('big', big))
    app.add_handler(CommandHandler('image', image))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polling
    print('Polling..')
    app.run_polling(poll_interval=1) # Polls every x seconds