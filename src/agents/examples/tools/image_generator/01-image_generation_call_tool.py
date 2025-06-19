# The image generation tool allows you to generate images using a text prompt, and optionally image inputs.
# The image_generation_call tool call result will include a base64-encoded image.
# import necessary libraries
from openai import OpenAI
import base64

# initialize openai client
client = OpenAI()

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