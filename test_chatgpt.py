from chatgpt import chatgpt

starting_prompt="You are a chatbot providing technical help for web development. Stay very concise, every token costs me money."
chattest = chatgpt.ChatGPT(starting_prompt,verbose=0)
#print(chattest("How do I find the derivative of 2x^ln(x)?"))

for i in range(10):
    Q=input('User: ')
    A=chattest(Q)
    print('ChatGPT: ' + A)