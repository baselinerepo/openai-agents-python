# Example of using the OpenAI Python client to interact with the API
# to generate an image using DALL-E 3 based on a given prompt.
import base64
import os
import io
from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client with your API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define the model to use for image generation
model = "dall-e-3"

# Function to generate an image based on a text prompt
def generate_image(prompt, image_name="dall-e-3-image.png") -> None:
    try:
        # Generate an image based on the prompt
        response = client.images.generate(
            model=model,
            prompt=prompt,
            n=1,
            size="1024x1024",
            response_format="b64_json"
        )

        image_data = response.data[0].b64_json
        image_bytes = io.BytesIO(base64.b64decode(image_data))
        image = Image.open(image_bytes)
        image.save(image_name)
        print(f"Image saved as {image_name}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    prompt = "A futuristic city skyline at sunset, featuring towering skyscrapers with neon-lit holographic advertisements. The buildings showcase sleek, sci-fi architecture with glass facades reflecting warm hues of orange and purple. Flying cars zoom between structures, leaving behind glowing trails. In the foreground, a bustling street with robotic vendors selling exotic digital wares. The scene is cinematic, with dramatic lighting and intricate details."
    generate_image(prompt)