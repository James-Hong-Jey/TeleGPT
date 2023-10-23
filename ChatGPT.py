import openai

prompts = {
    "normal": open('prompt.txt', 'r').read(),
    "chinese": open('chinese.txt', 'r').read(),
    "malay": open('malay.txt', 'r').read()
}

models = {
    "good": "gpt-4",
    "chat": "gpt-3.5-turbo",
    "big": "gpt-3.5-turbo-16k"
}

def get_response(user_prompt, persona, modelName):
    print()
    response = openai.ChatCompletion.create(
    model=models[modelName],
    messages=[
        {"role": "system", "content": prompts[persona]},
         {"role": "user", "content": user_prompt}
    ],
    max_tokens=1024,
    temperature=0.75,
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.0
    )
    return response