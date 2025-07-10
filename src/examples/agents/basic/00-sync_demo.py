# This script demonstrates how to use the OpenAI API to get a response from the GPT-4o-mini model.
import os
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

# gets the api key from the .env file
# override attribute avoids caching the key in the code
load_dotenv(find_dotenv(), override=True)

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# defines the Model constants
GPT_MODEL: str = "gpt-4o-mini"
TEMPERATURE: float = 0.0

# Non-streaming:
# Create a standard chat response request to the GPT-4o-mini model
print(f"---- GPT-4o-mini Chat Response Standard Request ----")
#response = client.chat.completions.create(
response = client.responses.create(
    model=GPT_MODEL,
    temperature=TEMPERATURE,
    input=[
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
#print(response.choices[0].message.content)
print(response.output_text)

# Streaming:
# Create a chat completion request to the GPT-4o-mini model with streaming enabled
print("\n---- GPT-4o-mini Chat Completion Streaming Request ----")
for chunk in client.chat.completions.create(
    model=GPT_MODEL,
    max_tokens=50,
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


# Response headers:
# Print the response headers from the non-streaming request
print("\n\n---- GPT-4o-mini Chat Completion Response Headers ----")
response = client.chat.completions.with_raw_response.create(
    model=GPT_MODEL,
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