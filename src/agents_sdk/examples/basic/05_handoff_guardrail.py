#------------------------------------------------------------------------------
# creating a handoff and guardrail
# handoffs allow an agent to delegate tasks to another agent.
# different agents sceneraios
# for example a customer support app might have agents that each specifically handles tasks
# like order status, refunds, FAQs etc.
# Agents : which are LLM equipped with instructions and tools
# Handoffs: which allow agents to delegate task to other agents for specific tasks
# Guardrails: which enables the input to agents to be validated
# Tripwires: if the input or output fails the guardrails. the Guardrail will signal this with a Tripwire
#------------------------------------------------------------------------------
# import libraries
from agents import (Agent, GuardrailFunctionOutput, InputGuardrailTripwireTriggered, RunContextWrapper, TResponseInputItem, InputGuardrail, Runner)
import asyncio
from pydantic import BaseModel

# model constant
MODEL: str = "gpt-4o-mini"

class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str

# implementing a guardrail
guardrail_agent = Agent(
    model=MODEL,
    name="Guardrail check",
    instructions="Check if the user is asking about homework.",
    output_type=HomeworkOutput
)

# handoff description provide additional context for determining handoff routing
# math agent
math_tutor_agent = Agent(
    model=MODEL,
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problem. Explain your reasoning at each step and include examples",
)

# history agent
history_tutor_agent = Agent(
    model=MODEL,
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
)

# define guardrail function
async def homework_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, input_data: str | list[TResponseInputItem]
    ) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(HomeworkOutput)

    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=final_output.is_homework,
    )

# define your handoffs
triage_agent = Agent(
    model=MODEL,
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


## final_output
# The first president of the United States was George Washington. He served from April 30, 1789, to March 4, 1797.
# Washington was a central figure in the American Revolutionary War and played a crucial role in the founding of
# the nation. After the war, he was elected unanimously by the Electoral College and is often referred to as the
# “Father of His Country” for his leadership in establishing the principles of the new government. His presidency
# set many precedents that are still followed today, including the formation of a Cabinet and the two-term limit 
# for presidents.