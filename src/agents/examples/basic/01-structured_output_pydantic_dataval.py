# Example of using OpenAI's structured output feature with Pydantic models
# import dependencies
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from pydantic import BaseModel

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client with your API key
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define model constants
GPT_MODEL: str = "gpt-4o-mini"
TEMPERATURE: float = 0.7

#-----------------------------------------------------
# STEP 1: Define a Pydantic model for structured output
#-----------------------------------------------------
class WeatherReport(BaseModel):
    city: str
    temperature: float
    condition: str

#-----------------------------------------------------
# STEP 2: Create a function to generate structured output
#-----------------------------------------------------
async def generate_weather_report(city: str) -> WeatherReport:
    # Simulate a weather report generation
    completion = await client.beta.chat.completions.parse(
        model=GPT_MODEL,
        temperature=TEMPERATURE,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"What's the weather like in {city}?"}
        ],
        response_format=WeatherReport
    )

    #-------------------------------------------------------
    # STEP 3: Handle/Parse the structured output
    #-------------------------------------------------------
    if completion.choices:
        report = completion.choices[0].message.parsed
        return WeatherReport(
            city=report.city,
            temperature=report.temperature,
            condition=report.condition
        )
    else:
        raise ValueError("No valid response received.")


# Run the function asynchronously and print the result
if __name__ == "__main__":
    import asyncio
    print(asyncio.run(generate_weather_report("New York")))
