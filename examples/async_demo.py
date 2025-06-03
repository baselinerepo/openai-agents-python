# This script demonstrates how to use the OpenAI API to get a async response from the GPT-4o-mini model.
import os
import asyncio
from openai import AsyncOpenAI

# Initialize the OpenAI client with the API key
client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Model configuration
MODEL: str = "gpt-4o-mini"
TEMPERATURE: float = 0.7

async def main():
    # Non-streaming:
    # Create a async standard chat completion request to the GPT-4o-mini model
    print("---- GPT-4o-mini Chat Completion Standard Request ----")
    response = await client.chat.completions.create(
        model=MODEL,
        max_tokens=50,
        temperature=TEMPERATURE,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that provides concise and accurate information."
            },
            {
                "role": "user",
                "content": "What is the capital of France?"
            }
        ]
    )
    print(response.choices[0].message.content)
    response=None

    # Streaming:
    # Create a async chat completion request to the GPT-4o-mini model with streaming enabled
    print("\n---- GPT-4o-mini Chat Completion Streaming Request ----")
    async for chunk in await client.chat.completions.create(
        model=MODEL,
        max_tokens=500,
        temperature=TEMPERATURE,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that provides concise and accurate information."
            },
            {
                "role": "user",
                "content": "How do I output all files in a directory using Python?"
            }
        ],
        stream=True
    ):
        print(chunk.choices[0].delta.content, end="", flush=True)
        chunk=None

    # Response headers:
    # Print the response headers from the non-streaming request
    print("\n---- GPT-4o-mini Chat Completion Response Headers ----")
    response = await client.chat.completions.with_raw_response.create(
        model=MODEL,
        max_tokens=50,
        temperature=TEMPERATURE,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that provides concise and accurate information."
            },
            {
                "role": "user",
                "content": "What is the capital of France?"
            }
        ]
    )
    completion = response.parse()
    print(response.request_id)
    print(completion.choices[0].message.content)

asyncio.run(main())