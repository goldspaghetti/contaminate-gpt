import requests
from PIL import Image
from openai import OpenAI
from config import OPEN_AI_KEY

import os, os.path

# simple version for working with CWD
# print(len([name for name in os.listdir('images/') if os.path.isfile(name)]))


client = OpenAI(api_key=OPEN_AI_KEY)

x = input("what would you like to generate? ")
# i = len(os.listdir('images')) + 1

while x != "":
    response = client.images.generate(
        prompt=f"a moldy, disgusting, vile, contaminated, photorealistic image of {x}",
        size="256x256",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url
    image_response = requests.get(image_url)
    image_data = image_response.content

    with open(f"images/{'_'.join(x.split())}.jpg", "wb") as f:
        f.write(image_data)
    x = input("what would you like to generate? ")
    # i += 1