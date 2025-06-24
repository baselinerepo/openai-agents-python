# creating a handoff
# handoffs allow an agent to delegate tasks to another agent.
# different agents sceneraios
# for example a customer support app might have agents that each specifically handles tasks
# like order status, refunds, FAQs etc.
# import libraries
from agents import Agent, GuardrailFunctionOutput, InputGuardrail, Runner
import asyncio
from pydantic import BaseModel

class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking about homework.",
    output_type=HomeworkOutput
)

# handoff description provide additional context for determining handoff routing
# math agent
math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problem. Explain your reasoning at each step and include examples",
)

# history agent
history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
)

async def homework_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(HomeworkOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_homework,
    )

# define your handoffs
triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question",
    handoffs=[history_tutor_agent, math_tutor_agent],
    input_guardrails=[
        InputGuardrail(guardrail_function=homework_guardrail),
    ],
)

# main function
async def main():
    result = await Runner.run(triage_agent, "Who was the first president of the United States?")
    print(result.final_output)

    result = await Runner.run(triage_agent, "What is life")
    print(result.final_output)


# run asynchronously
if __name__ == "__main__":
    asyncio.run(main())