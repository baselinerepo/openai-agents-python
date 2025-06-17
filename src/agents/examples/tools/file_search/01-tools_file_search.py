# import necessary libraries
from openai import OpenAI

# initialize openai client
client = OpenAI()

# define model constant
MODEL: str = "gpt-4o-mini"

#--------------------------------------------------------------------
# Step 1: run python3 -m utility
# to create vector store and add files
#--------------------------------------------------------------------

#--------------------------------------------------------------------
# file_search tool
#--------------------------------------------------------------------
response = client.responses.create(
    model=MODEL,
    input="What is deep research by OpenAI?",
    tools=[{
        "type": "file_search",
        "vector_store_ids": ["vs_68515769b68c8191a52b70f27c733fd4"]
    }]
)
print(response)
