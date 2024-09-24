from openai import OpenAI
import base64
from dotenv import load_dotenv

load_dotenv()

IMAGE_PATH = "./src/google-image.png"
MODEL = "gpt-4o-mini"

client = OpenAI()

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def get_image_to_text(image_path):
    base64_image = encode_image(image_path)
    # print(base64_image)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": [
                {"type": "text", "text": "describe the image"},  # Set the prompt
                {"type": "image_url", "image_url": {
                    "url": f"data:image/png;base64,{base64_image}"
                    }
                }
            ]}
        ],
        temperature=0.0,
    )

    image_description = response.choices[0].message.content

    print(image_description)
    return image_description


if __name__ == "__main__":
    get_image_to_text(IMAGE_PATH)