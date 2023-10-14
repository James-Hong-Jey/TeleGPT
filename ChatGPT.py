import openai

try: 
    with open('./prompt.txt','r') as file:
        prompt = file.read()
except FileNotFoundError:
    print(f"You need to make a prompt.txt")

def get_response(user_prompt):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    # prompt=generate_prompt_date(prompt),
    messages=[
        {"role": "system", "content": prompt},
         {"role": "user", "content": user_prompt}
    ],
    max_tokens=1024,
    temperature=0.7,
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.0
    )
    return response