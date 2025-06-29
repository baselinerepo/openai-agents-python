# Function calling example with search_knowledge_base function
# import necessary libraries
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with API Key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY") or os.getenv("_OPENAI_API_KEY"))

# Define the json schema for function calling
tools = [{
    "type": "function",
    "name": "search_knowledge_base",
    "description": "Search the knowledge base for information on a topic.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The user question or search query."
            },
            "options": {
                "type": "object",
                "properties": {
                    "num_results": {
                        "type": "integer",
                        "description": "Number of top results to return."
                    },
                    "domain_filter": {
                        "type": ["string", "null"],
                        "description": "Optional domain to narrow the search (e.g. 'finance', 'medical'). Pass null if not needed."
                    },
                    "sort_by": {
                        "type": ["string", "null"],
                        "enum": ["relevance", "date", "popularity", "alphabetical"],
                        "description": "How to sort results. Pass null if not needed."
                    }
                },
                "required": ["num_results", "domain_filter", "sort_by"],
                "additionalProperties": False
            }
        },
        "required": ["query", "options"],
        "additionalProperties": False
    }
}]

# Create a response using the OpenAI client with function calling
response = client.responses.create(
    model="gpt-4o-mini",
    input=[{"role": "user", "content": "Can you find information about ChatGPT in the AI knowledge base?"}],
    tools=tools,
    tool_choice="auto"
)

# Print the response from the model
print(response.output)

# response object
#[ResponseFunctionToolCall(
#    arguments='{"query":"ChatGPT","options":{"num_results":5,"domain_filter":null,"sort_by":"relevance"}}', 
#    call_id='call_vSGAsv7GLGgADP7BLTqWO4bz', 
#    name='search_knowledge_base', 
#    type='function_call', 
#    id='fc_684abfe0945881a184a882f6a1fba74509ab4849031c5d43', 
#    status='completed'
#)]