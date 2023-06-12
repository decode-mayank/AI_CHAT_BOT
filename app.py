from flask import Flask, request, jsonify
from dotenv import load_dotenv
from config import CONNECTION_STRING
import os

from langchain.document_loaders import PyMuPDFLoader
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

# Create Flask application instance
app = Flask(__name__)

loader = PyMuPDFLoader("data/NIPS-2017-attention-is-all-you-need-Paper.pdf")
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

store = PGVector(
    connection_string=CONNECTION_STRING,
    embedding_function=embeddings,
    collection_name="data_of_nips123",
)

def generate_response(user_message):
    llm = ChatOpenAI(
        openai_api_key=os.environ["OPENAI_API_KEY"],
        model_name='gpt-3.5-turbo',
        temperature=0.1,
        max_tokens=50
    )

    # Conversational memory
    conversational_memory = ConversationBufferWindowMemory(
        memory_key='chat_history',
        k=5,
        return_messages=True
    )

    template = """
    I want you to act as an "Attention Is All You Need" Assistant. You are a helpful bot that provides services related to "Attention Is All You Need".
    If the user asks a greeting question then give helpful response.I will share information with you, and you have to respond accordingly. Your response
    should be a two-line complete sentence.If the user asks a question that is not related to the information, respond with "I am sorry I didn't understand
    your request." without any explanations or additional words.Please follow these instructions strictly and carefully.
    Context: {context}
    Question: {question}
    Answer:
    """

    PROMPT = PromptTemplate(template=template, input_variables=["context", "question"])
    chain_type_kwargs = {"prompt": PROMPT}
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=store.as_retriever(),
        chain_type_kwargs=chain_type_kwargs,
        memory=conversational_memory
    )

    # Generate AI response using prompt templates
    try:
        response = qa.run(user_message)
    except Exception as e:
        response = "I am sorry I didn't understand your request."

    print(conversational_memory)
    return response

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['user_message']
    # Get user's message from JSON request
    response = generate_response(user_message)

    return jsonify({'responses': response})

if __name__ == "__main__":
    app.run(debug=True)
