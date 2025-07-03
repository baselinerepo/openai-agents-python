# Example of using Agent Hooks to track the lifecycle of agents and tools
# import necessary libraries
import random
from typing import Any
from pydantic import BaseModel
from agents import (
    Agent,
    AgentHooks,
    RunContextWrapper,
    Runner,
    Tool,
    function_tool
)

class CustomAgentHooks(AgentHooks):
    def __init__(self, display_name: str):
        self.event_counter = 0
        self.display_name = display_name
    
    async def on_start(self, context: RunContextWrapper, agent: Agent) -> None:
        self.event_counter += 1
        print(f"### ({self.display_name}) {self.event_counter}: Agent {agent.name} started")
    
    async def on_end(self, context: RunContextWrapper, agent: Agent, output: Any) -> None:
        self.event_counter += 1
        print(f"### ({self.display_name}) {self.event_counter}: Agent {agent.name} ended with output: {output}")
    
    async def on_handoff(self, context: RunContextWrapper, agent: Agent, source: Agent) -> None:
        self.event_counter += 1
        print(f"### ({self.display_name}) {self.event_counter}: Agent {agent.name} handed off from {source.name}")
    
    async def on_tool_start(self, context: RunContextWrapper, agent: Agent, tool: Tool) -> None: 
        self.event_counter += 1
        print(f"### ({self.display_name}) {self.event_counter}: Agent {agent.name} started tool {tool.name}")

    async def on_tool_end(self, context: RunContextWrapper, agent: Agent, tool: Tool, result: str) -> None:
        self.event_counter += 1
        print(f"### ({self.display_name}) {self.event_counter}: Agent {agent.name} ended tool {tool.name} with result: {result}")


### define tools for the agents

@function_tool
def random_number_tool(max: int) -> int:
    """
    Generates a random number up to the specified maximum.
    """
    return random.randint(0, max)

@function_tool
def multiply_by_three_tool(x: int) -> int:
    """
    Multiplies the input by three.
    """
    return x * 3

class FinalResult(BaseModel):
    number: int

# the multiply agent
multiply_agent = Agent(
    name="Multiply Agent",
    instructions="Multiply the number by three and return the final result.",
    tools=[multiply_by_three_tool],
    output_type=FinalResult,
    hooks=CustomAgentHooks(display_name="Multiply Agent Hooks"),
)

# the start agent
start_agent = Agent(
    name="Start Agent",
    instructions="Generate a random number. If it's even stop. If it's odd, hand off to the multiply agent.",
    tools=[random_number_tool],
    output_type=FinalResult,
    handoffs=[multiply_agent],
    hooks=CustomAgentHooks(display_name="Start Agent Hooks"),
)

# define async main function
async def main() -> None:
    user_input = input("Enter a maximum number: ")
    try:
        max_number = int(user_input)
        await Runner.run(
            start_agent,
            input=f"Generate a random number between 0 to {max_number}.",
        )
        print("Done!")
    except ValueError:
        print("Invalid input. Please enter a valid integer.")
        return

# run the main function asynccronously
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
