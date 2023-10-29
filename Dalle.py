import openai

def get_image(user_prompt):
    response = openai.Image.create(
    prompt=user_prompt,
    n=1,
    size="1024x1024"
    )
    image_url = dalle_response['data'][0]['url']
    print(image_url)
    return image_url

# response = openai.Image.create_edit(
  # image=open("sunlit_lounge.png", "rb"),
  # mask=open("mask.png", "rb"),
  # prompt="A sunlit indoor lounge area with a pool containing a flamingo",
  # n=1,
  # size="1024x1024"
# )
# image_url = response['data'][0]['url']

# response = openai.Image.create_variation(
  # image=open("corgi_and_cat_paw.png", "rb"),
  # n=1,
  # size="1024x1024"
# )
# image_url = response['data'][0]['url']