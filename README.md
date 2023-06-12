# AI_CHAT_BOT

This code is an implementation of a chatbot using OpenAI's language model GPT-3.5. The chatbot is trained on a given PDF file and can answer questions related to the contents of the PDF.

# Installation

# Setup Project
   git clone https://github.com/decode-mayank/AI_CHAT_BOT
	
# Requirements

   pip install -r requirements.txt

You also need to have an OpenAI API key to access the GPT-3.5 model.

Reference example.env to create .env file

	api_key = 
	
# Setup PGvector
  
 Compile and install the extension (supports Postgres 11+)

	cd /tmp
	git clone --branch v0.4.4 https://github.com/pgvector/pgvector.git
	cd pgvector
	make
	make install # may need sudo

# Getting Started

Enable the extension (do this once in each database where you want to use it)
	
	CREATE EXTENSION vector;

# Usage

1. Set your OpenAI API key in the code by replacing enter your openai api key here with your actual key.
2. In app.py file, add the path to the PDF file you want to train the chatbot on by setting the PdfReader path to the file's location.
3. Run the app.py and wait for the chatbot to initialize.
4. Enter your questions or prompts into the text box and hit enter to receive a response from the chatbot.
