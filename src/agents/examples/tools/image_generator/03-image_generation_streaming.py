# The image generation tool supports streaming partial images as the 
# final result is being generated. This provides faster visual feedback 
# for users and improves perceived latency.
# You can set the number of partial images (1-3) with the partial_images parameter.

# import libraries
import os
import base64
from openai import OpenAI

# Initialize the OpenAI client with your API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# define model constant
GPT_MODEL: str = "gpt-4.1"

response_stream = client.responses.create(
    model=GPT_MODEL,
    input="Draw a gorgeous image of a river made of white owl feathers, snaking its way through a serene winter landscape",
    stream=True,
    tools=[{"type": "image_generation", "partial_images": 2}]
)

for event in response_stream:
    if event.type == "response.image_generation_call.partial_image":
        idx = event.partial_image_index
        image_base64 = event.partial_image_b64
        image_bytes = base64.b64decode(image_base64)
        with open(f"river{idx}.png", "wb") as f:
            f.write(image_bytes)
