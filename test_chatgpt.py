from chatgpt import chatgpt

starting_prompt="You are a chatbot imitating a homework assistant for math. You will guide a student through their math problems."
chattest = chatgpt.ChatGPT(starting_prompt,verbose=1)
print(chattest("How do I find the derivative of 2x^ln(x)?"))