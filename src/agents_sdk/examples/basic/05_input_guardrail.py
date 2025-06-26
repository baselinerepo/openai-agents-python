# implementing input guardrail

import asyncio
from agents import (
    Agent,
    GuardrailFunctionOutput,
    Runner,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    TResponseInputItem,
    input_guardrail)
from pydantic import BaseModel

# define model constant
MODEL: str = "gpt-4o-mini"

class MathHomeworkOutput(BaseModel):
    is_math_homework: bool
    reasoning: str

# the guardrail agent
guardrail_agent = Agent(
    model=MODEL,
    name="Guardrail Check",
    instructions="Check if the user is asking you to do their math homework.",
    output_type=MathHomeworkOutput,
)

# define input guardrail
@input_guardrail
async def math_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    input_data: str | list[TResponseInputItem]
    ) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(MathHomeworkOutput)

    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=final_output.is_math_homework,
    )

# define customer suport agent
cs_agent = Agent(
    model=MODEL,
    name="Customer support agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    input_guardrails=[math_guardrail]
)

# define main async function
async def main():
    # this should trip the guardrail
    try:
        result = await Runner.run(cs_agent, "Hello, can you help me solve for x: 2x + 3 = 11?")
        print(result.final_output)
        print("Guardrail didn't trip - this is unexpected")
    except InputGuardrailTripwireTriggered:
        print("Math homework guardrail tripped")

# run asynchronously
if __name__ == "__main__":
    asyncio.run(main())

# final output
# "Math homework guardrail tripped"