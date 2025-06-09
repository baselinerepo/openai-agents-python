# Example of using OpenAI's structured output feature with Pydantic models
import os
import time
from openai import AsyncOpenAI
from pydantic import BaseModel
from datetime import date, datetime

# # Initialize OpenAI client
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Model constants
MODEL: str = "gpt-4o-mini"
TEMPERATURE: float = 0.7

#-----------------------------------------------------
# STEP 1: Define a Pydantic model for structured output
#-----------------------------------------------------

class CalendarEvent(BaseModel):
    title: str
    date: str
    time: str
    location: str
    participants: list[str]

#-----------------------------------------------------
# STEP 2: Create a function to generate structured output
#-----------------------------------------------------
async def generate_calendar_event(title: str, date: str, time: str, location: str, participants: list[str]) -> CalendarEvent:
    # Simulate a calendar event generation
    completion = await client.beta.chat.completions.parse(
        model=MODEL,
        temperature=TEMPERATURE,
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Create the event details."},
            {"role": "user", "content": f"Create a calendar for {participants} attending {title} at {location} on {date} {time}."}
        ],
        response_format=CalendarEvent
    )

    #-------------------------------------------------------
    # STEP 3: Handle/Parse the structured output
    #-------------------------------------------------------
    if completion.choices:
        report = completion.choices[0].message.parsed
        return CalendarEvent(
            title=f"Calendar Event for {report.title}",
            date=date,
            time=time,
            location=location,
            participants=[f"{report.participants} OpenAI Team"],
        )
    else:
        raise ValueError("No valid response received.")


# Run the function and print the result
if __name__ == "__main__":
    # Example usage
    import asyncio

    strTime = time.strftime("%H:%M:%S")
    strDate = date.today().strftime("%A")
    print(asyncio.run(generate_calendar_event(title="Science fair", date=strDate, time=strTime, location="New York", participants=["jim, john, jane"])))