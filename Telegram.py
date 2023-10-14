from dotenv import load_dotenv
load_dotenv()
import os
import openai
import re

from typing import Final 
from ChatGPT import *
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


TOKEN = os.getenv("TELEGRAM_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")
openai.api_key = os.getenv("OPENAI_API_KEY")

# Commands
async def startCommand (update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I am James!")

async def helpCommand (update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please type something else")

async def customCommand (update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Custom Command!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    # Check if user is in group or private message
    if message_type == 'group':
        if BOT_USERNAME in text:
            # Remove name from message
            new_text: str = text.replace(BOT_USERNAME, '').strip() 
            # response: str = handle_response(new_text)
            chatgpt_response = get_response(new_text)
            response = chatgpt_response.choices[0].message.content
        else: 
            return
    else: 
        # in a private message there will be no name in the message
        # response: str = handle_response(text)
        chatgpt_response = get_response(text)
        response = chatgpt_response.choices[0].message.content

    print('Bot: ', response, ' (Using ', chatgpt_response.usage.total_tokens, ')')
    
    # Split by punctuation, so no punctuation + lower + split up
    split_response = re.split(r'[,.!?]+', response)
    split_response = [token for token in split_response if token]
    for text in split_response:
        await update.message.reply_text(text.lower().replace('.',''))
    # await update.message.reply_text(response.lower().replace('.','').replace(',',''))

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting Bot..')
    app = Application.builder().token(TOKEN).build()
    
    # Commands
    app.add_handler(CommandHandler('start', startCommand))
    app.add_handler(CommandHandler('help', helpCommand))
    app.add_handler(CommandHandler('custom', customCommand))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polling
    print('Polling..')
    app.run_polling(poll_interval=3) # Polls every 3 seconds

    