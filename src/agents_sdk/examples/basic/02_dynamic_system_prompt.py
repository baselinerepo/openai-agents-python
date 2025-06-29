# an example of a dynamic system prompt that changes based on the context.
# prerequisites: Install the Agents SDK with `pip install openai-agents`
# import necessary libraries
import random
from typing import Literal
from agents import Agent, RunContextWrapper, Runner

class CustomContext:
    def __init__(self, style: Literal["haiku", "pirate", "robot"]):
        self.style = style

def custom_instructions(run_context: RunContextWrapper[CustomContext], agent: Agent[CustomContext]) -> str:
    context = run_context.context
    if context.style == "haiku":
        return "Only respond in haikus."
    elif context.style == "pirate":
        return "Respond as a pirate."
    else:
        return "Respond normally."

agent = Agent(
    name="Chat agent",
    instructions=custom_instructions,
)

async def main():
    choice: Literal["haiku", "pirate", "robot"] = random.choice(["haiku", "pirate", "robot"])
    context = CustomContext(style=choice)
    print(f"Using style: {choice}\n")

    user_message = "Tell me something interesting."
    print(f"User: {user_message}")
    result = await Runner.run(agent, user_message, context=context)

    print(f"Agent {agent.name} says: {result.final_output}")


# run the main function asynchronously
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())