# Example of using OpenAI's Python client to make streaming requests
# import dependencies
import os
from dotenv import load_dotenv
from openai import OpenAI, AsyncOpenAI

# Load environment variables from .env file
load_dotenv()

# The synchronous main function
def sync_main() -> None:
    # Initialize the OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Model constants
    GPT_MODEL: str = "gpt-4o-mini"
    TEMPERATURE: float = 0.0

    # Streaming:
    # Create a sync chat completion request to the gpt-4o-mini model with streaming enabled
    print("\n---- gpt-4o-mini Chat Completion Streaming Request ----")
    response = client.completions.create(
        model=GPT_MODEL,
        max_tokens=5,
        temperature=TEMPERATURE,
        prompt="1,2,3,",
        stream=True
    )

    # You can manually iterate over the response
    first = next(response)
    print(f"got response data: {first.to_json()}")

    # Or you can automatically iterate over the response
    for chunk in response:
        print(chunk.to_json())


# define the asynchronous main function
async def async_main() -> None:
    # Initialize the asynchronous OpenAI client
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Model constants
    GPT_MODEL: str = "gpt-4o-mini"
    TEMPERATURE: float = 0.0

    # Streaming:
    # Create a sync chat completion request to the gpt-4o-mini model with streaming enabled
    print("\n---- gpt-4o-mini async Chat Completion Streaming Request ----")
    response = await client.completions.create(
        model=GPT_MODEL,
        max_tokens=5,
        temperature=TEMPERATURE,
        prompt="1,2,3,",
        stream=True
    )

    # You can manually iterate over the response
    # In Python 3.10+ you can also use the `await anext(response)` builtin instead
    first = await response.__anext__()
    print(f"got response data: {first.to_json()}")

    # Or you can automatically iterate over the response
    # Note that the for loop will not exit until *all* of the data has been processed.
    async for chunk in response:
        print(chunk.to_json())


# run asynchronous and synchronous main functions
if __name__ == "__main__":
    # Run the synchronous main function
    import asyncio

    sync_main()
    asyncio.run(async_main())