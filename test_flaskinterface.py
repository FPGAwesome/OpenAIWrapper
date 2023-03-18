# Built on request by chatgpt via the prompt: 
# "I've built a small API for chatgpt. How can I make a simple front-end interface for chatting?"
# Because I'm too lazy for writing yet another flask app from scratch. Works... ish, it'll be a to-do

from flask import Flask,jsonify, render_template, request
from chatgpt import chatgpt

import os

app = Flask(__name__)
starting_prompt="Stay very concise, every token costs me money."
chattest = chatgpt.ChatGPT(starting_prompt,verbose=1) # ,model='gpt-4' not cheap, don't use for testing

# Route to render the chat window template
@app.route('/')
def chat_window():
    return render_template('chat_window.html')

# Route to handle chatbot API calls
@app.route('/chatbot', methods=['POST'])
def chatbot_call():
    message = request.form['message']
    response = chattest(message)
    return {'response': response}

# Route to handle saving chat messages
@app.route('/save_messages', methods=['POST'])
def save_messages():
    file = request.form['filename']

    if not os.path.exists('temp'):
        os.makedirs('temp')
    
    # Save the chat history
    chattest.save_chat(os.path.join('temp',file))
    
    return render_template('chat_window.html')


# Route to handle loading chat messages
@app.route('/load_messages', methods=['POST'])
def load_messages():
    file = request.files['file']
    
    # Save uploaded file to a temporary location
    temp_file_path = os.path.join('temp', file.filename)
    file.save(temp_file_path)
    
    # Load the chat history
    chattest.load_chat(temp_file_path)

    messages = chattest.messages#[{'type': msg.type, 'text': msg.text, 'time': msg.time} for msg in chattest.messages]
    return {'messages': messages}

if __name__ == '__main__':
    app.run(debug=True)