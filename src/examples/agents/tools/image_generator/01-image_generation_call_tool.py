# The image generation tool allows you to generate images using a text prompt, and optionally image inputs.
# The image_generation_call tool call result will include a base64-encoded image.
# list of supported models
# gpt-4o
# gpt-4o-mini
# gpt-4.1
# gpt-4.1-mini
# gpt-4.1-nano
# o3

# import libraries
import os
import base64
from dotenv import load_dotenv
from openai import OpenAI

# load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client with your API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# define model constant
MODEL: str = "gpt-4o-mini"

response = client.responses.create(
    model=MODEL,
    input="Draw an image of gray tabby cat hugging an otter with an orange scarf",
    tools=[{ "type": "image_generation" }],
)

# save the image to a file
image_data = [
    output.result
    for output in response.output
    if output.type == "image_generation_call"
]

if image_data:
    image_base64 = image_data[0]
    with open("otter.png", "wb") as f:
        f.write(base64.b64decode(image_base64))