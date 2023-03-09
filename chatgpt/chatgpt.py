# Taken from https://til.simonwillison.net/gpt3/chatgpt-api
import openai

class ChatGPT:
    def __init__(self, system="", verbose=0):
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({"role": "system", "content": system})

        self.verbose=verbose
    
    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result
    
    # can call different models, for these purposes it's really only useful
    # to use the two different available chatgpt models
    # gpt-3.5-turbo and gpt-3.5-turbo-0301
    # the latter of which doesn't pay strong attention to system messages in favor of the user prompts
    def execute(self, model="gpt-3.5-turbo"):
        completion = openai.ChatCompletion.create(model=model, messages=self.messages)
        # Uncomment this to print out token usage each time, e.g.
        # {"completion_tokens": 86, "prompt_tokens": 26, "total_tokens": 112}
        if self.verbose>0:
            print(completion.usage)
        return completion.choices[0].message.content