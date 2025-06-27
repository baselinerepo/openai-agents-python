from __future__ import annotations

from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    Runner,
    OutputGuardrailTripwireTriggered,
    RunContextWrapper,
    output_guardrail)

"""
This example shows how to use output guardrails.
Output guardrails are checks that run on the final output of an agent.
They can be used to do check if the output passes certain validation criteria

You can use the `@output_guardrail()` decorator to turn a function into an `OutputGuardrail`,
or create an `OutputGuardrail` manually.

Guardrails return a `GuardrailResult`. If `result.tripwire_triggered` is `True`, a
`OutputGuardrailTripwireTriggered` exception will be raised.

Guardrails are checks that run in parallel to the agent's execution.
They can be used to do things like:
- Check if output messages are off-topic
- Check that output messages don't violate any policies
- Take over control of the agent's execution if an unexpected output is detected

Guardrail Steps:
1. First, the guardrail receives the output produced by the agent
2. Next, the guardrail function runs to produce the `GuardrailFunctionOutput`,
   which is then wrapped in an `OutputGuardrailResult`
3. Finally, we check the tripwire_triggered is true, if true, an
   `OutputGuardrailTripwireTriggered` exception is raised.
   
In this example, we'll setup an output guardrail that trips if the user is asking to do homework.
If the guardrail trips, we'll respond with a refusal message.

Ref: https://openai.github.io/openai-agents-python/guardrails/
"""

# define model constant
MODEL: str = "gpt-4o-mini"

class MessageOutput(BaseModel):
    response: str

class MathOutput(BaseModel):
    is_math: bool
    reasoning: str

# the guardrail agent
guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the output includes any math.",
    output_type=MathOutput,
)

# define output guardrail
@output_guardrail
async def math_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, output: MessageOutput
) -> GuardrailFunctionOutput:
    """
    This is an output guardrail function
    """
    result = await Runner.run(guardrail_agent, output.response, context=ctx.context)
    final_output = result.final_output_as(MathOutput)

    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=final_output.is_math,
    )

### Step 2. The run loop

# define main async function
async def main():

    # define customer suport agent
    customer_support_agent = Agent(
        name="Customer support agent",
        instructions="You are a customer support agent. You help customers with their questions.",
        output_guardrails=[math_guardrail],
        output_type=MessageOutput,
    )

    while True:
        user_input = input("Enter a message: ")

        # this should trip the guardrail
        try:
            result = await Runner.run(customer_support_agent, user_input)
            print(result.final_output)
            print("Guardrail didn't tripped")
        except OutputGuardrailTripwireTriggered:
            print("Math output guardrail tripped.")


# run the main function asynchronously
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
