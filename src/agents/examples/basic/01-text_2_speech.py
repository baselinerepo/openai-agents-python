# This script demonstrates how to use the OpenAI API to convert text to speech asynchronously.
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer

# Load environment variables from .env file
load_dotenv()

# Initialize the Asynchronous OpenAI client
openai = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define the main asynchronous function to handle text-to-speech conversion
async def main() -> None:

    # Create a text-to-speech request
    async with openai.audio.speech.with_streaming_response.create(
        model="tts-1",
        input="""I see skies of blue and clouds of white
                The bright blessed days, the dark sacred nights
                And I think to myself
                What a wonderful world""",
        voice="alloy",
        response_format="pcm",
    ) as response:

        # Check if the response is successful
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            return

        # Read the audio content from the response
        audio_content = await response.read()

        # Create a LocalAudioPlayer instance to play the audio
        player = LocalAudioPlayer()
        await player.play(audio_content)

    # Save the audio content to a file
    with open("output.wav", "wb") as audio_file:
        audio_file.write(response.content)


# Print the response to confirm success
if __name__ == "__main__":
    # Run the main function ashynchronously
    import asyncio

    asyncio.run(main())
