# Example of using tools with an agent sdk
# import libraries
from agents import Agent, Runner, function_tool
from pydantic import BaseModel

class Weather(BaseModel):
    city: str
    temperature_range: str
    conditions: str

# define functional calling tools
@function_tool
def get_weather(city: str) -> Weather:
    print("[debug] get weather called")
    return Weather(city=city, temperature_range="14-20°C", conditions="Sunny with wind.")

agent = Agent(
    name="Hello World",
    instructions="You are a helpful agent.",
    tools=[get_weather],
)

# define async main function
async def main():
    runner = await Runner.run(agent, input="What's the weather in Tokyo?")
    print("Response: ", runner.final_output)
    # the weather in tokyo is sunny.

# run the main function asynchronously
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())