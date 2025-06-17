# Upload a file
import requests
from io import BytesIO
from openai import OpenAI

# Initialize OpenAI client with API key
client = OpenAI()

# model constant to use
MODEL: str = "gpt-4o-mini"

#--------------------------------------------------------------------
# upload the file to the File API
#--------------------------------------------------------------------
def upload_file(client, file_path):
    if file_path.startswith("http://") or file_path.startswith("https://"):
        # download the file content from the URL
        response = requests.get(file_path)
        file_content = BytesIO(response.content)
        file_name = file_path.split("/")[-1]
        file_tuple = (file_name, file_content)
        result = client.files.create(
            file=file_tuple,
            purpose="assistants"
        )
    else:
        # Handle local file path
        with open(file_path, "rb") as file_content:
            result = client.files.create(
                file=file_content,
                purpose="assistants"
            )
    print(result.id)
    return result.id

# replace with your own file path or URL
file_id = upload_file(client, "https://cdn.openai.com/API/docs/deep_research_blog.pdf")


#--------------------------------------------------------------------
# create a vector store
#--------------------------------------------------------------------
vector_store = client.vector_stores.create(
    name="knowledge_base"
)
print(vector_store.id)

#--------------------------------------------------------------------
# add the file to the vector store
#--------------------------------------------------------------------
vectorStoreFile = client.vector_stores.files.create(
    vector_store_id=vector_store.id,
    file_id=file_id
)
print(vectorStoreFile)

#--------------------------------------------------------------------
# check status
#--------------------------------------------------------------------
result = client.vector_stores.files.list(
    vector_store_id=vector_store.id
)
print(result)


# response output
#file-6NJYapdqnuYhKGk13x5R36
#vs_685068cbce808191ba444054b5b7be21
#VectorStoreFile(id='file-6NJYapdqnuYhKGk13x5R36', created_at=1750100172, last_error=None, object='vector_store.file', status='in_progress', usage_bytes=0, vector_store_id='vs_685068cbce808191ba444054b5b7be21', attributes={}, chunking_strategy=StaticFileChunkingStrategyObject(static=StaticFileChunkingStrategy(chunk_overlap_tokens=400, max_chunk_size_tokens=800), type='static'))
#SyncCursorPage[VectorStoreFile](data=[VectorStoreFile(id='file-6NJYapdqnuYhKGk13x5R36', created_at=1750100172, last_error=None, object='vector_store.file', status='in_progress', usage_bytes=0, vector_store_id='vs_685068cbce808191ba444054b5b7be21', attributes={}, chunking_strategy=StaticFileChunkingStrategyObject(static=StaticFileChunkingStrategy(chunk_overlap_tokens=400, max_chunk_size_tokens=800), type='static'))], has_more=False, object='list', first_id='file-6NJYapdqnuYhKGk13x5R36', last_id='file-6NJYapdqnuYhKGk13x5R36')
