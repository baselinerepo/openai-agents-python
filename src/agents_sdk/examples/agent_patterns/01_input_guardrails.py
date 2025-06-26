from __future__ import annotations
import asyncio
from pydantic import BaseModel

from agents import (
    Agent,
    GuardrailFunctionOutput,
    Runner,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    TResponseInputItem,
    input_guardrail)

"""
# this example shows how to use input guardrails.

Guardrails are checks that run in parallel to the agent's execution.
They can be used to do things like:
- Check if input messages are off-topic
- Check that input messages don't violate any policies
- Take over control of the agent's execution if an unexpected input is detected

In this example, we'll setup an input guardrail that trips if the user is asking to do math homework.
If the guardrail trips, we'll respond with a refusal message.
"""

# define model constant
MODEL: str = "gpt-4o-mini"

### Step 1. An agent-based guardrail that is triggered if the user is asking to do math homework
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
    ctx: RunContextWrapper[None], agent: Agent, input_data: str | list[TResponseInputItem]
    ) -> GuardrailFunctionOutput:
    """
    This is an input guardrail function
    """
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(MathHomeworkOutput)

    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=final_output.is_math_homework,
    )

### Step 2. The run loop

# define main async function
async def main():

    # define customer suport agent
    customer_support_agent = Agent(
        model=MODEL,
        name="Customer support agent",
        instructions="You are a customer support agent. You help customers with their questions.",
        input_guardrails=[math_guardrail],
    )

    input_data: list[TResponseInputItem] = []

    while True:
        user_input = input("Enter a message: ")
        input_data.append({
            "role": "user",
            "content": user_input,
        })

        # this should trip the guardrail
        try:
            result = await Runner.run(customer_support_agent, input_data)
            print(result.final_output)
            # if the guardrail didn't trigger, we use the result as the input for the next run
            input_data = result.to_input_list()
            print("Guardrail didn't tripped")
        except InputGuardrailTripwireTriggered:
            # if guardrail is triggered, we instead add a refusal message to the input
            message = "Sorry, I can't help you with your math homework."
            print(f"{message}, Math homework guardrail tripped")
            input_data.append({
                "role": "assistant",
                "content": "message",
            })


# run asynchronously
if __name__ == "__main__":
    asyncio.run(main())

# Final Output
# Enter a message: What's the capital of California?
# The capital of California is Sacramento.
# Guardrail didn't tripped
# Enter a message:  Can you help me solve for x: 2x + 5 = 11                                   
# Sorry, I can't help you with your math homework., Math homework guardrail tripped