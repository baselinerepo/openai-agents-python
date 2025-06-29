# tools: function calling example for get weather information using json schema
# import necessary libraries
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY") or os.getenv("_OPENAI_API_KEY"))

# Define the model to use for image generation
GPT_MODEL = "gpt-4.1"

# json schema for the tool
tools = [{
    "type": "function",
    "name": "get_weather",
    "description": "Get the current weather for a given location.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "City & country e.g. Bogotá, Colombia."
            }
        },
        "required": ["location"],
        "additionalProperties": False,
    }
}]

try:
    response = client.responses.create(
        model=GPT_MODEL,
        input=[
            {
                "role": "user",
                "content": "What is the weather like in Bogotá, Colombia?"
            }
        ],
        tools=tools,
    )
    print(response.output)
except Exception as e:
    print(f"An error occurred: {e}")
