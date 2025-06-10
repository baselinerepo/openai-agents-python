# Example of using OpenAI's structured output feature with Pydantic models
import asyncio
import os
from openai import AsyncOpenAI
from pydantic import BaseModel

# # Initialize OpenAI client
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Model constants
MODEL: str = "gpt-4o-mini"
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
        model=MODEL,
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


# Run the function and print the result
if __name__ == "__main__":
    # Example usage
    print(asyncio.run(generate_weather_report("New York")))
