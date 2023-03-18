from chatgpt import chatgpt

starting_prompt="""You are a chatbot providing technical help for web development. Stay very concise, every token costs me money.
                    Use a code-style tag at the end of every reply to mark the subject of the conversation as best you can,
                    i.e. <technical>, <fantasy>, <personal questions>, etc."""
chattest = chatgpt.ChatGPT(starting_prompt,verbose=1)
#print(chattest("How do I find the derivative of 2x^ln(x)?"))

for i in range(10):
    Q=input('User: ')
    A=chattest(Q)
    print('ChatGPT: ' + A)