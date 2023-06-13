import os
from langchain.embeddings.openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('api_key')

# Configuration variables
user_id = "2"
folder = "/home/bitcot/Desktop/Task-folder/demo"

# Create the OpenAIEmbeddings object
embeddings = OpenAIEmbeddings()

file_list = os.listdir(folder)

filtered_files = [file for file in file_list if user_id in file]

for file in filtered_files:
    file_path = os.path.join(folder, file)
    with open(file_path, "r") as file:
        content = file.read()

        # Create embeddings for the content
        document_embedding = embeddings.embed_documents(content)
        
        print(document_embedding)
        print("*"*10)
        print(f"File: {file}")
        # Process the embedding, such as storing or ana