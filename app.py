from flask import Flask, request, jsonify
from config import CONNECTION_STRING
from chatbot import generate_response
from script import filter_embed

# Create Flask application instance
app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['user_message']
    # Get user's message from JSON request
    response = generate_response(user_message)
    
    return jsonify({'responses': response})

# @app.route('/user_id',methods=['POST'])
# def filter():

#     user_id = request.json['user_id']
#     response = filter_embed(user_id)

#     return jsonify({"response":response})

if __name__ == "__main__":
    app.run(debug=True)
