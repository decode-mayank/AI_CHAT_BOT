import os
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import PyMuPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.pgvector import PGVector
from config import CONNECTION_STRING

from dotenv import load_dotenv

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('api_key')

# Configuration variables
user_id = "3"
folder = "/home/bitcot/Desktop/Task-folder/demo"


def filter_embed():
    file_list = os.listdir(folder)
    filtered_files = [file for file in file_list if user_id in file]

    if len(filtered_files) >= 1:
        for file in filtered_files:
            file_path = os.path.join(folder, file)

            loader = PyMuPDFLoader(file_path)
            documents = loader.load()
            
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0.0)
            docs = text_splitter.split_documents(documents)
            
            embeddings = OpenAIEmbeddings()
                
            db = PGVector.from_documents(
                documents=docs,
                embedding=embeddings,
                collection_name="data_of_nips123",
                connection_string=CONNECTION_STRING,
                openai_api_key=os.environ['OPENAI_API_KEY'],
                pre_delete_collection=False
            )

            retriever = db.as_retriever()
            print(retriever)
    else:
        print("user_id not found")


filter_embed()

