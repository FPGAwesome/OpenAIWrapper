# Built on request by chatgpt via the prompt: 
# "I've built a small API for chatgpt. How can I make a simple front-end interface for chatting?"
# Because I'm too lazy for writing yet another flask app from scratch. Works... ish, it'll be a to-do

from flask import Flask, render_template, request
from chatgpt import chatgpt

app = Flask(__name__)
starting_prompt="You are a chatbot providing technical help for web development. Stay very concise, every token costs me money."
chattest = chatgpt.ChatGPT(starting_prompt,verbose=0)

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

if __name__ == '__main__':
    app.run(debug=True)