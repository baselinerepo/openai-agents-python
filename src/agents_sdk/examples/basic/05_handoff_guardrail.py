# import libraries
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    TResponseInputItem,
    InputGuardrail,
    Runner
)
from pydantic import BaseModel

"""
# This example shows how to use handoffs and guardrails.

Handoffs allows a agent to delegate tasks to another agent.
They can be used to do things like:
- Customer support app might have agents for specific tasks
- Like Order status, refunds, FAQs etc.

Guardrails are checks that run in parallel to the agent's execution.
They can be used to do things like:
- Check if input messages are off-topic
- Check that input messages don't violate any policies
- Take over control of the agent's execution if an unexpected input is detected

Guardrail Steps:
1. First, the guardrail receives the same input passed to the agent.
2. Next, the guardrail function runs to produce a `GuardrailFunctionOutput`, which is
   than wrapped in an `InputGuardrailResult`.
3. Finally, we check the .tripwire_triggered is true, if true, an
   InputGuardrailTripwireTriggered exception is raised.

Tripwires: If the input or output fails the guardrails, the Guardrail will 
signal this with a Tripwire.

In this example, we'll setup an input guardrail that trips if the user is asking to do math homework.
If the guardrail trips, we'll respond with a refusal message.
"""

# model constant
GPT_MODEL: str = "gpt-4o-mini"

### Step 1. An agent-based guardrail that is triggered if the user is asking to do homework
class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str

# implementing a guardrail
guardrail_agent = Agent(
    model=GPT_MODEL,
    name="Guardrail Check",
    instructions="Check if the user is asking about homework.",
    output_type=HomeworkOutput
)

# handoff description provide additional context for determining handoff routing
# the math agent
math_tutor_agent = Agent(
    model=GPT_MODEL,
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problem. Explain your reasoning at each step and include examples",
)

# the history agent
history_tutor_agent = Agent(
    model=GPT_MODEL,
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
)

# define input guardrail function
async def homework_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, input_data: str | list[TResponseInputItem]
    ) -> GuardrailFunctionOutput:
    """
    This is an input guardrail function
    """
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(HomeworkOutput)

    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=final_output.is_homework,
    )

### Step 2. The run loop

# main function
async def main():

    # define your handoffs
    triage_agent = Agent(
        model=GPT_MODEL,
        name="Triage Agent",
        instructions="You determine which agent to use based on the user's homework question",
        handoffs=[history_tutor_agent, math_tutor_agent],
        input_guardrails=[
            InputGuardrail(guardrail_function=homework_guardrail),
        ],
    )

    input_data: list[TResponseInputItem] = []

    while True:
        user_input = input("Enter a message: ")
        input_data.append({
            "role": "user",
            "content": user_input
        })

        # this should trip the guardrail
        try:
            result = await Runner.run(triage_agent, input_data)
            print(result.final_output)

            result = await Runner.run(triage_agent, "What is life")
            print(result.final_output)
            # if the guardrail didn't trigger, we use the result as the input for the next run
            input_data = result.to_input_list()
        except InputGuardrailTripwireTriggered:
            # if guardrail is triggered, we instead add a refusal message to the input
            message = "Sorry, I can't help you with your math homework."
            print(f"{message}, Math homework guardrail tripped")
            input_data.append({
                "role": "assistant",
                "content": "message",
            })


# run the main funciton asynchronously
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())


## final_output
# The first president of the United States was George Washington. He served from April 30, 1789, to March 4, 1797.
# Washington was a central figure in the American Revolutionary War and played a crucial role in the founding of
# the nation. After the war, he was elected unanimously by the Electoral College and is often referred to as the
# “Father of His Country” for his leadership in establishing the principles of the new government. His presidency
# set many precedents that are still followed today, including the formation of a Cabinet and the two-term limit 
# for presidents.