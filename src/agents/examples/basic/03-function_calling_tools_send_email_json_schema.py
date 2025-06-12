# function calling example with send_email function
# import necessary libraries
from openai import OpenAI

# Initialize OpenAI client with API key
client = OpenAI()

# Function calling tool to send email
tools = [{
    "type": "function",
    "name": "send_email",
    "description": "Send an email to a given recipient with a subject and message.",
    "parameters": {
        "type": "object",
        "properties": {
            "to": {
                "type": "string",
                "description": "The recipient email address.",
            },
            "subject": {
                "type": "string",
                "description": "Email subject line."
            },
            "body": {
                "type": "string",
                "description": "Body of the email message.",
            }
        },
        "required": ["to", "subject", "body"],
        "AdditionalProperties": False
    }
}]

try:
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[{"role": "user", "content": "Can you send an email to ashish.hatkar@gmail.com and top8234568@yahoo.com saying just wanting to say hi?"}],
        tools=tools
    )
    print(response.output)
except Exception as e:
    print(f"An error occurred: {e}")

# response output
#[
#    ResponseFunctionToolCall(
#        arguments='{"to":"ashish.hatkar@gmail.com","subject":"Hello!","body":"Hi!"}', 
#        call_id='call_58MHX9aqjWZQMAbEyCDRTUEj', 
#        name='send_email', 
#        type='function_call', 
#        id='fc_68493c659f2081a394c12c3de8e47bda0f69003a5048eb2e', 
#        status='completed'
#    ),
#    ResponseFunctionToolCall(
#        arguments='{"to":"top8234568@yahoo.com","subject":"Hello!","body":"Hi!"}', 
#        call_id='call_LPX3IOiA6MtcuAtwh1BkLcu3', 
#        name='send_email', 
#        type='function_call', 
#        id='fc_68493c660be081a3baa5fd245eb1bb970f69003a5048eb2e', 
#        status='completed'
#    )
#]