## Using tools ##

When generating model responses, you can extend model capabilities using built-in tools. These tools help models access additional context and information from the web or your files.

## Available tools ##

OpenAI offers several built-in tools from the available tools list and let the model decide which tools to use based on conversation.

1. [Function Calling](./file_search/01-file_search_call_tool.py)
    - Call custom code to give the model access to additional data and capabilities
2. [Web Search](./web_search/01-web_search_call_tool.py)
    - Allows model to search the web for latest information before generating a response
3. [Remote MCP Server]()
    - Give the model access to new capabilities via Model Context Protocol (MCP) servers
4. [File Search](./file_search/01-file_search_call_tool.py)
    - Search the content of the uploaded files for context when generating a response
5. [Image Generation](./image_generator/01-image_generation_call_tool.py)
    - Generate or edit images using GPT Image
6. [Code interpreter]()
    - Allow the model to execute code in a secure container
7. [Computer Use]()
    - Create agentic workflows that enable a model to control a computer interface

