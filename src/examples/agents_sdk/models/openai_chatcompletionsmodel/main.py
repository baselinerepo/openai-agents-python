# import libraries
import os
from dotenv import load_dotenv
from agents import Agent, AsyncOpenAI, Runner, OpenAIChatCompletionsModel

"""
The Agents SDK comes with out-of-the-box support for OpenAI models in two flavors:
The OpenAIResponsesModel, which calls OpenAI APIs using the new Responses API.
The OpenAIChatCompletionsModel which calls OpenAI APIs using the new Chat completions API.
"""

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with API key
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY") or os.getenv("_OPENAI_API_KEY"))

# Define the model to use for image generation
GPT_MODEL = "gpt-4o-mini"

# Define agents
spanish_agent = Agent(
    name="Spanish agent",
    instructions="You only speak Spanish",
    model="o3_mini",
)

english_agent = Agent(
    name="English agent",
    instructions="You only speak English",
    model=OpenAIChatCompletionsModel(
        model="gpt-4o",
        openai_client=AsyncOpenAI()
    ),
)

triage_agent = Agent(
    name="Triage agent",
    instructions="Handoff to the appropriate agent based on the language of the request.",
    handoffs=[spanish_agent, english_agent],
    model="gpt-3.5-turbo",
)

# define async main function
async def main():
    result = await Runner.run(triage_agent, input="Hola, ¿cómo estás?")
    print(result.final_output)


# run async function asynchronously
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())