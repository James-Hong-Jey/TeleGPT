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
    raw = False
    all = False
    user_prompt = update.message.text.split('/image ')[1]
    # Clean
    if(user_prompt == ""): return

    # Check for all flag
    if "-all " in user_prompt:
        all = True
        user_prompt = user_prompt.replace("-all ","")

    ## Check for raw flag
    if "-raw " in user_prompt:
        print("Making prompt more user specific:")
        raw = True
        user_prompt = user_prompt.replace("-raw ","")

    prompt_message = f'User ({update.message.from_user.first_name}) requested: "{user_prompt}"'
    print(prompt_message)
    with open('history.txt', 'a') as file:
        file.write(prompt_message + "\n")

    if raw:
        user_prompt = "I NEED to test how the tool works with extremely simple prompts. DO NOT add any detail, just use it AS-IS:" + user_prompt

    dalle_response = get_image(user_prompt)
    image_url = dalle_response['data'][0]['url']
    revised_prompt = dalle_response['data'][0]['revised_prompt'] if all else ""
    print(image_url)
    print(revised_prompt)
    await update.message.reply_photo(photo=image_url, caption=revised_prompt)

async def ping (update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("pong")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'persona' not in context.user_data:
        context.user_data['persona'] = 'normal'
    if 'modelName' not in context.user_data:
        context.user_data['modelName'] = 'chat'
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.from_user.first_name}) in {message_type}: "{text}"')

    # Authorised Users Only
    username: str = update.message.from_user.username
    allowed_usernames = ["jeysiao", "yuyufrog"]
    if username not in allowed_usernames:
        return

    # Check if user is in group or private message
    if message_type == 'private':
        chatgpt_response = get_response(text, context.user_data['persona'], context.user_data['modelName'])
        response = chatgpt_response.choices[0].message.content
    else: 
        # # Remove name from message
        # if BOT_USERNAME in text:
            # new_text: str = text.replace(BOT_USERNAME, '').strip() 
            # chatgpt_response = get_response(new_text, context.user_data['persona'], context.user_data['modelName'])
            # response = chatgpt_response.choices[0].message.content
        # else: 
        return
        
    print('Bot: ', response, ' (Using ', chatgpt_response.usage.total_tokens, ')')
    
    # Split by punctuation, so no punctuation + lower + split up
    emojiless_response = emoji.replace_emoji(response, replace='')
    split_response = re.split(r'[,.!?]+', emojiless_response)
    split_response = [token for token in split_response if token]
    for text in split_response:
        await update.message.reply_text(text.lower().replace('.',''))

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update "{update.message.text}" caused error "{context.error}"')
    # await update.message.reply_text(context.error)

if __name__ == '__main__':
    print('Starting Bot..')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('persona', personaCommand))
    app.add_handler(CommandHandler('malay', malay))
    app.add_handler(CommandHandler('normal', normal))
    app.add_handler(CommandHandler('chinese', chinese))

    app.add_handler(CommandHandler('image', image))

    app.add_handler(CommandHandler('ping', ping))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polling
    print('Polling..')
    app.run_polling(poll_interval=1) # Polls every x seconds