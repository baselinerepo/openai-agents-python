# tools: function calling example for get weather information using json schema
# import necessary libraries
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY") or os.getenv("_OPENAI_API_KEY"))

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
        model="gpt-4.1",
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
