# The Code Interpreter tool allows models to write and run Python code in a sandboxed environment 
# to solve complex problems in domains like data analysis, coding, and math. Use it for:
#
# 1. Processing files with diverse data and formatting
# 2. Generating files with data and images of graphs
# 3. Writing and running code iteratively to solve problems—for example, a model that 
# writes code that fails to run can keep rewriting and running that code until it succeeds
# import necessary libraries
from openai import OpenAI

# initialize openai client
client = OpenAI()

# define model constant
MODEL: str = "gpt-4o-mini"

response = client.responses.create(
    model=MODEL,
    tools=[{
        "type": "code_interpreter",
        "container": { "type": "auto" }
    }],
    instructions="You are a personal math tutor. When asked a math question, write and run code to answer the question.",
    input="I need to solve the equation 3x + 11 = 14. Can you help me?",
)

print(response.output_text)

# response output
# The solution to the equation \(3x + 11 = 14\) is \(x = 1\).