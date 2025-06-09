# Example of using tools with an agent sdk
# import necessary libraries
import asyncio
from pydantic import BaseModel
from agents import Agent, Runner, function_tool

class Weather(BaseModel):
    city: str
    temperature_range: str
    conditions: str

@function_tool
def get_weather(city: str) -> Weather:
    print("[debug] get weather called")
    return Weather(city=city, temperature_range="14-20°C", conditions="Sunny with wind.")

agent = Agent(
    name="Hello World",
    instructions="You are a helpful agent.",
    tools=[get_weather],
)

async def main():
    runner = await Runner.run(agent, input="What's the weather in Tokyo?")
    print("Response: ", runner.final_output)
    # the weather in tokyo is sunny.

# run the main function asynchronously
if __name__ == "__main__":
    asyncio.run(main())