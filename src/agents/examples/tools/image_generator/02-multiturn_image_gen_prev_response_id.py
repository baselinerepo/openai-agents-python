# Multi-turn editing
# You can iteratively edit images by referencing previous response IDs or image IDs.
# This allows you to refine images across multiple turns in a conversation
# list of supported models
# gpt-4o
# gpt-4o-mini
# gpt-4.1
# gpt-4.1-mini
# gpt-4.1-nano
# o3

# Using response IDs
# import dependencies
import os
import base64
from openai import OpenAI

# Initialize the OpenAI client with your API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# define model constant
GPT_MODEL: str = "gpt-4.1-mini"

# built the response api
response = client.responses.create(
    model=GPT_MODEL,
    input="Generate an image of gray tabby cat hugging an otter with an orange scarf",
    tools=[{
        "type": "image_generation"
    }],
)

image_data = [
    output.result
    for output in response.output
    if output.type == "image_generation_call"
]

if image_data:
    image_base64 = image_data[0]
    with open("cat_and_otter.png", "wb") as f:
        f.write(base64.b64decode(image_base64))

# follow up

response_fwup = client.responses.create(
    model=GPT_MODEL,
    previous_response_id=response.id,
    input="Now make it look realistic",
    tools=[{
        "type": "image_generation"
    }],
)

image_data_fwup = [
    output.result
    for output in response_fwup.output
    if output.type == "image_generation_call"
]

if image_data_fwup:
    image_base64 = image_data_fwup[0]
    with open("cat_and_otter_realistic.png", "wb") as f:
        f.write(base64.b64decode(image_base64))
