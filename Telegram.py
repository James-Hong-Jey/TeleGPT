from dotenv import load_dotenv
load_dotenv()
import os
import openai
import re
import emoji

from ChatGPT import *
from telegram import Update
from telegram import Bot
from telegram.ext import Application, MessageHandler, filters, ContextTypes, Updater

TOKEN = os.getenv("TELEGRAM_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")
openai.api_key = os.getenv("OPENAI_API_KEY")
bot = Bot(token=TOKEN)

def webhook(request):
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot)
        message_type: str = update.message.chat.type
        text: str = update.message.text

        print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

        # Check if user is in group or private message
        if message_type == 'group':
            if BOT_USERNAME in text:
                # Remove name from message
                new_text: str = text.replace(BOT_USERNAME, '').strip() 
                chatgpt_response = get_response(new_text)
                response = chatgpt_response.choices[0].message.content
            else: 
                return
        else: 
            # in a private message there will be no name in the message
            chatgpt_response = get_response(text)
            response = chatgpt_response.choices[0].message.content

        print('Bot: ', response, ' (Using ', chatgpt_response.usage.total_tokens, ')')
        
        # Split by punctuation, so no punctuation + lower + split up
        emojiless_response = emoji.replace_emoji(response, replace='')
        split_response = re.split(r'[,.!?]+', emojiless_response)
        split_response = [token for token in split_response if token]
        for text in split_response:
            # await update.message.reply_text(text.lower().replace('.',''))
            bot.sendMessage(text=text.lower().replace('.',''))
    return "ok"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    # Check if user is in group or private message
    if message_type == 'group':
        if BOT_USERNAME in text:
            # Remove name from message
            new_text: str = text.replace(BOT_USERNAME, '').strip() 
            chatgpt_response = get_response(new_text)
            response = chatgpt_response.choices[0].message.content
        else: 
            return
    else: 
        # in a private message there will be no name in the message
        chatgpt_response = get_response(text)
        response = chatgpt_response.choices[0].message.content

    print('Bot: ', response, ' (Using ', chatgpt_response.usage.total_tokens, ')')
    
    # Split by punctuation, so no punctuation + lower + split up
    emojiless_response = emoji.replace_emoji(response, replace='')
    split_response = re.split(r'[,.!?]+', emojiless_response)
    split_response = [token for token in split_response if token]
    for text in split_response:
        await update.message.reply_text(text.lower().replace('.',''))

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting Bot..')
    app = Application.builder().token(TOKEN).build()

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polling
    # print('Polling..')
    # app.run_polling(poll_interval=3) # Polls every 3 seconds