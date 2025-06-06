# Example of using the OpenAI Python client to interact with the API
# to generate an image using DALL-E 3 based on a given prompt.
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client with your API key
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define the model to use for image generation
model = "dall-e-3"

# Function to generate an image based on a text prompt
async def generate_image(prompt) -> None:
    try:
        # Generate an image based on the prompt
        response = await client.images.generate(
            model=model,
            prompt=prompt,
            n=1,
            size="1024x1024",
        )

        # Extract the image URL from the response
        print(response)

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    import asyncio

    prompt = "A futuristic city skyline at sunset, featuring towering skyscrapers with neon-lit holographic advertisements. The buildings showcase sleek, sci-fi architecture with glass facades reflecting warm hues of orange and purple. Flying cars zoom between structures, leaving behind glowing trails. In the foreground, a bustling street with robotic vendors selling exotic digital wares. The scene is cinematic, with dramatic lighting and intricate details."
    asyncio.run(generate_image(prompt))
