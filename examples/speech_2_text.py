# Example of using OpenAI's AsyncOpenAI client to transcribe audio from the microphone.
# This example requires the `openai` package and an active OpenAI API key.
import asyncio
import os
import numpy as np
from openai import AsyncOpenAI
from openai.helpers import Microphone

# Record audio from the microphone asynchronously.
async def record_audio():
    """Record audio from the microphone asynchronously."""
    recording = await Microphone(timeout=10.0).record()  # Set a timeout for inactivity
    print("Finished recording audio.")
    return recording  # Get the recorded audio chunk as bytes

# This example demonstrates how to use the OpenAI client to transcribe audio from the microphone asynchronously.
async def main() -> None:

    try:
        # Initialize OpenAI client
        client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Start listening to the microphone
        print("Recording audio from the microphone for next 5 seconds...")
        audio_bytes = await record_audio()

        # Process the audio stream and transcribe it to text
        response = await client.audio.transcriptions.create(
            model="whisper-1",
            #file=("audio.wav", audio_bytes, "audio/wav"),
            file=audio_bytes,
            response_format="text",
        )
        print(f"Transcription: {response['text']}")

    except Exception as e:
        print(f"An error occurred: {e}")


# Ensure the microphone is closed properly
if __name__ == "__main__":
    asyncio.run(main())