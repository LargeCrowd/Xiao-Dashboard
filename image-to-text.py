import os
from openai import OpenAI
import base64
from dotenv import load_dotenv

load_dotenv()

IMAGE_PATH = "google-image.png"
MODEL = "gpt-4o-mini"

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

base64_image = encode_image(IMAGE_PATH)
# print(base64_image)

client = OpenAI()

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "user", "content": [
            {"type": "text", "text": "describe the image"},  # Set the prompt
            {"type": "image_url", "image_url": {
                "url": f"data:image/png;base64,{base64_image}"
                # "url": "https://upload.wikimedia.org/wikipedia/commons/e/e2/The_Algebra_of_Mohammed_Ben_Musa_-_page_82b.png"
                }
            }
        ]}
    ],
    temperature=0.0,
)

print(response.choices[0].message.content)