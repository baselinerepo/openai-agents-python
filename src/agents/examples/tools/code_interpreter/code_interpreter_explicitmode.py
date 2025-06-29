##------------------------------------------------------------
# The Code Interpreter tool allows models to write and run Python code in a sandboxed environment 
# to solve complex problems in domains like data analysis, coding, and math. Use it for:
#
# 1. Processing files with diverse data and formatting
# 2. Generating files with data and images of graphs
# 3. Writing and running code iteratively to solve problems—for example, a model that 
# writes code that fails to run can keep rewriting and running that code until it succeeds
# import necessary libraries

# the code interpreter tool requires a container object. A container is a fully sandboxed virtual
# machine that the model can run python code in.
# there are 2 ways to create a container
# 1. Auto mode: you can do this by passing the container:
# { "type": "auto", files: ["file1", "file2"] }
# 2. Explicit mode: you create a container using the v1/containers endpoint, and assigns 
# its id as the container value in the tool configuration.
##------------------------------------------------------------
# import dependencies
from openai import OpenAI

# initialize openai client
client = OpenAI()

# explicit container creation
container = client.containers.create(name="test_container")

# define model constant
GPT_MODEL: str = "gpt-4o-mini"

response = client.responses.create(
    model=GPT_MODEL,
    tools=[{
        "type": "code_interpreter",
        "container": container.id
    }],
    tool_choice="required",
    input="use the python tool to calculate what is 4 * 3.82. and then find its square root and then find the square root of that result",
)

print(response.output_text)

# response output
# The calculations are as follows:

# 1. \( 4 \times 3.82 = 15.28 \)
# 2. The square root of \( 15.28 \) is approximately \( 3.91 \).
# 3. The square root of \( 3.91 \) is approximately \( 1.98 \).