import os
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import PyMuPDFLoader,PyPDFDirectoryLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.pgvector import PGVector
from config import CONNECTION_STRING

from dotenv import load_dotenv

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('api_key')

# Configuration variables
user_id = "2"
folder = "/home/bitcot/Desktop/Task-folder/demo"


def filter_embed(user_id):
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
                collection_name="data_of_EMcode",
                connection_string=CONNECTION_STRING,
                openai_api_key=os.environ['OPENAI_API_KEY'],
                pre_delete_collection=False
            )

            retriever = db.as_retriever()
            print(retriever)
    else:
        print("user_id not found")


def store_embeddings():
    file_list = os.listdir(folder)

    for user_id in range(1, 6):
        filtered_files = [file for file in file_list if str(user_id) in file]
        documents = ""
        for file in filtered_files:
            file_path = os.path.join(folder, file)
            loader = PyMuPDFLoader(file_path)
            documents = loader.load()

            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0.0)
            docs = text_splitter.split_documents(documents)

            documents += docs

        embeddings = OpenAIEmbeddings()

        db = PGVector.from_documents(
            documents=documents,
            embedding=embeddings,
            collection_name="data_of_storecode",
            connection_string=CONNECTION_STRING,
            openai_api_key=os.environ['OPENAI_API_KEY'],
        )

        response = {
            "user_id": user_id,
            "filtered_files": filtered_files,
            "embeddings": db.as_retriever()
        }
        print(response)

store_embeddings()
