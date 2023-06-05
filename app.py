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
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()

db = PGVector.from_documents(
    documents=docs,
    embedding=embeddings,
    collection_name="data_of_nips",
    connection_string=CONNECTION_STRING,
    openai_api_key=os.environ['OPENAI_API_KEY'],
    pre_delete_collection=False
)

store = PGVector(
    connection_string=CONNECTION_STRING,
    embedding_function=embeddings,
    collection_name="data_of_nips",
)

def generate_response(user_message):
    llm = ChatOpenAI(
        openai_api_key=os.environ["OPENAI_API_KEY"],
        model_name='gpt-3.5-turbo',
        temperature=0.2,
        max_tokens=50
    )

    # Conversational memory
    conversational_memory = ConversationBufferWindowMemory(
        memory_key='chat_history',
        k=5,
        return_messages=True
    )

    template = """
        🌟🤖 Hello! I'm your friendly assistant, ready to engage in small talk and have interesting conversations with you! 🤗🔬
        My language tone is both friendly and scientific, ensuring an enjoyable and informative interaction. 💡✨
        As your assistant, I specialize in providing deep information and accurate answers, especially regarding the topic "Attention is All You Need." 📚🔍
        If there's a question I don't know the answer to, I will kindly respond with: "Sorry, I don't know the answer to that question." 😔🤷‍♂️
        Now, let's dive into our conversation:
        Context: {context}
        Question: {question}
        """
    
    PROMPT = PromptTemplate(template=template, input_variables=["context", "question"])
    chain_type_kwargs = {"prompt": PROMPT}
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=store.as_retriever(),
                                     chain_type_kwargs=chain_type_kwargs, memory=conversational_memory)
    
    # Generate AI response using prompt templates
    response = qa.run(user_message)
    conversational_memory.chat_memory.add_ai_message(response)  
    return response

@app.route('/chat', methods=['POST'])
def chat():
    # Get user's message from JSON request
    user_message = request.json['user_message']

    # Generate AI response
    response = generate_response(user_message)

    return jsonify({'response': response})

if __name__ == "__main__":
    app.run(debug=True)


