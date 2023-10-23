# TeleGPT

Personal project to improve my conversational Chinese and Malay. 
I can have a conversation in those respective languages with the bot, 
and subsequently receive feedback about the formality of my language, grammar violations, etc.

Also has the option to select between those languages and the model used (default GPT-3.5-Turbo)

## Requirements
1. python
2. pip
3. Money in your openai account and an API key
4. A bot from @BotFather and an API token

## Quickstart Instructions
1. pip install -r requirements.txt
2. cp sample.env .env
3. Edit .env with your openai API key and bot API token
4. cp sample_prompt.txt prompt.txt
5. Edit prompt.txt with your prompt (from the pov of instructing the machine)
6. python Telegram.py
7. Find your @bot and talk to it, without any commands

## Language Instructions
1. Use /persona then select either /Chinese, /Malay or /Normal to reset to the prompt.txt
2. Use /modelname to switch between the chatgpt models. GPT-3.5-Turbo is sufficient for most uses