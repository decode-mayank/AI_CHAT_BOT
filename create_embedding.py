from dotenv import load_dotenv
import os

from config import CONNECTION_STRING
from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.pgvector import PGVector
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chains import RetrievalQA
from langchain import PromptTemplate

load_dotenv()

# Set up OpenAI credentials
os.environ['OPENAI_API_KEY'] = os.getenv('api_key')

def generate_response(user_message):

    loader = WebBaseLoader("https://www.espn.com/")
    documents = loader.load()
    
    # Create embeddings
    embeddings = OpenAIEmbeddings()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0.0)
    docs = text_splitter.split_documents(documents)

    db = PGVector.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name="data_of_website1",
        connection_string=CONNECTION_STRING,
        openai_api_key=os.environ['OPENAI_API_KEY'],
        
    )

    llm = ChatOpenAI(
        openai_api_key=os.environ["OPENAI_API_KEY"],
        model_name='gpt-3.5-turbo',
        temperature=0.2,
        max_tokens=50
    )


    template = """
    You are act as information provider for website.if user ask any question about service and category then provide website one direct link for particular page.
    You are able to show main section in list.you  provides a relevant answer based on the website content.you response is no more than a few sentences long.
    context: {context}
    Question: {question}
    Answer:
    """

    PROMPT = PromptTemplate(template=template, input_variables=["context", "question"])
    chain_type_kwargs = {"prompt": PROMPT}
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=db.as_retriever(),
        chain_type_kwargs=chain_type_kwargs,
    )

    
    response = qa.run(user_message)
    print(response)
  

user_input = input("type any thing")
generate_response(user_input)