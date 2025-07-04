# import libraries
import os
import sqlite3
import json

from dotenv import load_dotenv
from openai import OpenAI
from typing import List, Dict, Any

"""
Workflow:
1. Connect to the external database and schema overview
2. Generating SQL Queries with GPT based on user prompts
3. Executing generated SQL Queries with associated database schema
"""

# define constant
GPT_MODEL: str = "gpt-4o-mini"
TEMPERATURE: float = 0.0

# Load environment variables from .env file
load_dotenv()

# Initialise the sqlite client
sqlite_db_conn = sqlite3.connect('../data/chinook.db')

# Initialize the OpenAI client with the API key
gpt_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


# define db functions
def get_table_names():
    """
    Returns list of user table names in database
    """
    table_names = []
    tables = sqlite_db_conn.execute('SELECT name FROM sqlite_master WHERE type="table"')
    for table in tables.fetchall():
        table_names.append(table[0])
    
    return table_names


def get_column_names(table_name: str):
    """
    Returns list of columns in database
    """
    column_names = []
    columns = sqlite_db_conn.execute(f"PRAGMA table_info('{table_name}');").fetchall()
    for col in columns:
        column_names.append(col[1])
    
    return column_names


def get_database_info():
    """
    Returns list of dicts containing the table name and columns for each table in the database.
    """
    table_dicts = []
    for table_name in get_table_names():
        columns_names = get_column_names(table_name)
        table_dicts.append({"table_name": table_name, "column_names": columns_names})

    return table_dicts


##---------------------- AI Integration Begins -----------------------##

#-------------------------------------------------------------
# Utility function to initialize chat completions API
#-------------------------------------------------------------
def get_chat_completions(
    messages: List[Dict[str, str]],
    model: str = GPT_MODEL,
    temperature: float = 0.0,
    tools = None,
    tool_choice = None,
) -> tuple[str, dict[str, Any]]:
    """
    Function to get a response from the OpenAI model with optional tools.
    Args:
        messages (List[Dict[str, str]]): List of messages to send to the model.
        model (str): The model to use for generating the response.
        temperature (float): Temperature for response variability.
        tools (list, optional): List of tools to be used by the model.
        tool_choice (str, optional): Tool choice strategy.
    Returns:
        tuple[str, dict[str, Any]]: The output text and the response object.
    """

    params = {
        "model": model,
        "temperature": temperature,
        "messages": messages,
        "tools": tools,
        "tool_choice": tool_choice,
    }

    try:
        result = gpt_client.chat.completions.create(**params)
        return result
    except Exception as e:
        print(f"An error occurred: {e}")


#-------------------------------------------------------------
# build the database schema string
#-------------------------------------------------------------
db_schema = get_database_info()
db_schema_string = "\n".join(
    f"Table: {table['table_name']}\nColumns: {', '.join(table['column_names'])}" for table in db_schema
)

#print(db_schema_string)

#-------------------------------------------------------------
# Step 1: Call model with the query_database tool defined in JSON schema
#-------------------------------------------------------------
# JSON schema for the tool with precise latitude and longitude
tools = [{
    "type": "function",
    "function": {
        "name": "query_database",
        "description": "Use this function to answer user questions about music. Input should be a fully formed SQL query.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": f"""
                        SQL query extracting info to answer the user's question.
                        SQL should be written using the database schema:
                        {db_schema_string}
                        The query should be returned in plain text, not in JSON.
                    """,
                }
            },
            "required": ["query"],
            "additionalProperties": False,
        },
        "strict": True # will ensure function calls reliably adhere to the function schema
    }
}]


def query_database(query):
    results = str(sqlite_db_conn.execute(query).fetchall())
    return results

#print(query_database('Select * from album'))


def generate_sql_query(prompt: str):
    """
    Return query chat completions message
    """
    chat_completions_message = get_chat_completions(
        model=GPT_MODEL,
        messages=[
            {
                "role": "system",
                "content": "Answer user questions by generating SQL queries"
            },
            {
                "role": "user",
                "content": prompt
            },
        ],
        tools=tools,
    )

    return chat_completions_message


def extract_execute_sql(prompt: str):
    """
    #-------------------------------------------------------------
    # Extract SQL query from chat completions arguments
    # Execute the sql query_database with the provided arguments
    #-------------------------------------------------------------
    # SAMPLE OUTPUT CHAT COMPLETIONS MESSAGE
    #-------------------------------------------------------------
    #ChatCompletionMessage(
    #    content=None,
    #    refusal=None,
    #    role='assistant',
    #    annotations=[],
    #    audio=None, 
    #    function_call=None,
    #    tool_calls=[ChatCompletionMessageToolCall(
    #        id='call_l0XoM0PhJjwk8rh0P8tHLx2Z',
    #        function=Function(
    #            arguments='{"query":"SELECT Artist.Name, COUNT(Track.TrackId) AS TrackCount \\nFROM Artist \\nJOIN Album ON Artist.ArtistId = Album.ArtistId \\nJOIN Track ON Album.AlbumId = Track.AlbumId \\nGROUP BY Artist.ArtistId \\nORDER BY TrackCount DESC \\nLIMIT 5;"}',
    #            name='query_database'
    #        ),
    #        type='function')]
    #)
    """

    chat_completions_messages = generate_sql_query(prompt)
    tool_call = chat_completions_messages.choices[0].message.tool_calls[0]

    if tool_call.function.name == 'query_database':
        query = json.loads(tool_call.function.arguments)["query"]
        dataset = query_database(query)
        print(f"GPT Generated SQL:\n{query}")
        print(f"Dataset: {dataset}")


##---------------------- AI Integration Ends -----------------------##


if __name__ == "__main__":
    #print(get_table_names())
    #print(get_column_names("employee"))
    #print(get_database_info())

    while True:
        user_input = input("Enter a prompt: ")

        #extract_execute_sql("Who are the top 5 artists by number of tracks?")
        extract_execute_sql(user_input)

# dispose objects
sqlite_db_conn.close()
gpt_client.close()


# Enter a prompt: Who are the top 5 artists by number of tracks?
# SAMPLE OUTPUT QUERY AND DATASET FOR USER PROMPT
# SELECT Artist.Name, COUNT(Track.TrackId) AS TrackCount 
# FROM Artist 
# JOIN Album ON Artist.ArtistId = Album.ArtistId 
# JOIN Track ON Album.AlbumId = Track.AlbumId 
# GROUP BY Artist.Name 
# ORDER BY TrackCount DESC 
# LIMIT 5;
# [('Iron Maiden', 213), ('U2', 135), ('Led Zeppelin', 114), ('Metallica', 112), ('Lost', 92)]
