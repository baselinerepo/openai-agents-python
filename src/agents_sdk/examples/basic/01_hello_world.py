# This file is part of the Agents SDK project.
# prerequisite: Install the Agents SDK with `pip install openai-agents`
# import necessary libraries
import asyncio
from agents import Agent, Runner

async def main():
    agent = Agent(name="Assistant", instructions="You only respond in haikus.")
    result = await Runner.run(agent, "Tell me a haiku about nature.")
    print(f"Agent {agent.name} says: {result.final_output}")

# run the main function asynchronously
if __name__ == "__main__":
    asyncio.run(main())
    
