# function calling tools with precise latitude and longitude instead of general
# location parameter leveraging JSON schema for weather data
# import required libraries
import os
import json
import requests

from openai import OpenAI
from typing import List, Dict, Any

# Define the model to be used
MODEL = "gpt-4o-mini"

# Initialize OpenAI client with API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY") or os.getenv("_OPENAI_API_KEY"))

# Utility function to get the current weather based on latitude and longitude
def get_response(
    input_messages: List[Dict[str, str]],
    model: str = MODEL,
    temperature: float = 0.0,
    tools = None,
    tool_choice = None,
) -> tuple[str, dict[str, Any]]:
    """
    Function to get a response from the OpenAI model with optional tools.
    Args:
        input_messages (List[Dict[str, str]]): List of messages to send to the model.
        model (str): The model to use for generating the response.
        temperature (float): Temperature for response variability.
        tools (list, optional): List of tools to be used by the model.
        tool_choice (str, optional): Tool choice strategy.
    Returns:
        tuple[str, dict[str, Any]]: The output text and the response object.
    """

    params = {
        "model": model,
        "input": input_messages,
        "temperature": temperature,
        "tools": tools,
        "tool_choice": tool_choice,
    }

    response = client.responses.create(**params)
    return response.output[0]


def get_weather(latitude, longitude):
    """
    Function to get the current weather for given latitude and longitude.
    This is a mock function that simulates fetching weather data.
    In a real-world scenario, you would call a weather API here.
    """
    # Mock response simulating a weather API call
    base_api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    response = requests.get(base_api_url)
    data = response.json()
    return {
        "latitude": latitude,
        "longitude": longitude,
        "temperature": data['current']['temperature_2m'],
        "wind_speed": data['current']['wind_speed_10m']
    }


# JSON schema for the tool with precise latitude and longitude
# Step 1: Call model with the get_weather tool defined in JSON schema
tools = [{
    "type": "function",
    "name": "get_weather",
    "description": "Get current temperature for provided coordinates in celsius.",
    "parameters": {
        "type": "object",
        "properties": {
            "latitude": {
                "type": "number",
            },
            "longitude": {
                "type": "number",
            }
        },
        "required": ["latitude", "longitude"],
        "additionalProperties": False,
    },
    "strict": True
}]

input_message = [
    {
        "role": "user",
        "content": "What's the current weather like in Bogotá, Colombia?"
    }
]

response_output = get_response(
    model="gpt-4o-mini",
    input_messages=input_message,
    tools=tools,
)

# Step 2: Model decided to call the get_weather function
print(response_output)

# response output
#[
#    ResponseFunctionToolCall(
#        arguments='{"latitude":4.6109,"longitude":-74.0817}', 
#        call_id='call_7pyTkzMy5MbSckXIcQmMNgyR', 
#        name='get_weather', 
#        type='function_call', 
#        id='fc_68496ca1dbb0819e956cae36ed47b541097f74d9603a25e4', 
#        status='completed'
#    )
#]

# Step 3: Execute the get_weather function with the provided arguments
tool_call = response_output
args = json.loads(tool_call.arguments)

result = get_weather(args['latitude'], args['longitude'])

# Step 4: Supply result back to the model so that it can incorporate
# it into the final response
input_message.append(tool_call)
input_message.append({
    "type": "function_call_output",
    "call_id": tool_call.call_id,
    "output": str(result)
})

response_output_2 = client.responses.create(
    model="gpt-4o-mini",
    input=input_message,
    tools=tools,
)

# Final response from the model incorporating the weather data
print(response_output_2.output_text)

# Final response output
# "The current weather in Bogotá, Colombia, is about 12.7°C with a wind speed of 3.6 m/s."