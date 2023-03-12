# Taken from https://til.simonwillison.net/gpt3/chatgpt-api
import csv
import openai
import pickle
import tiktoken

class ChatGPT:
    def __init__(self, system="", verbose=0, model="gpt-3.5-turbo"):
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({"role": "system", "content": system})
        self.verbose=verbose

        # Model-related variables

        self.model=model
        # for some token counting utility
        self.encoding=tiktoken.encoding_for_model(model)
    
    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result
    
    # can call different models, for these purposes it's really only useful
    # to use the two different available chatgpt models
    # gpt-3.5-turbo and gpt-3.5-turbo-0301
    # the latter of which doesn't pay strong attention to system messages in favor of the user prompts
    def execute(self):
        completion = openai.ChatCompletion.create(model=self.model, messages=self.messages)
        # Uncomment this to print out token usage each time, e.g.
        # {"completion_tokens": 86, "prompt_tokens": 26, "total_tokens": 112}
        if self.verbose>0:
            print(completion.usage)
        return completion.choices[0].message.content
    
    def print_history(self):
        for i,h in enumerate(self.messages):
            print(i,h)

    # This could be useful for loading prior chats later, maybe change it up
    # with some json instead of csv though
    def dump_history(self,filename='whisper_history.csv'):
        with open(filename,'w') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',')
            for i,h in enumerate(self.messages):
                csvwriter.writerow([i,h])

    # delicious pickles, until I implment some db solution
    def save_chat(self,filename='saved_chat.pkl'):
        with open(filename, 'wb') as f:
            pickle.dump(self.messages, f)

    def load_chat(self,filename='saved_chat.pkl'):
        with open(filename, 'wb') as f:
            self.messages=pickle.load(f)

    # Make the model we use for encoding overridable because that sounds
    # cool to do. Not going to support get_encoding at this time because
    # I don't want or need it for anything
    def count_tokens(self, msg, model=None):
        encoding=self.encoding
        if model != None:
            encoding=tiktoken.encoding_for_model(model)
        else:
            model=self.model #headache saver
            
        # borrowed from the openai cookbook github page, may not actually work
        # testing against api token counts shows this works alright though

        if model == "gpt-3.5-turbo":  # note: future models may deviate from this
            num_tokens = 0
            messages_count=self.messages.copy()
            messages_count.append({"role": "user", "content": msg})
            for message in messages_count:
                num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
                for key, value in message.items():
                    num_tokens += len(encoding.encode(value))
                    if key == "name":  # if there's a name, the role is omitted
                        num_tokens += -1  # role is always required and always 1 token
            num_tokens += 2  # every reply is primed with <im_start>assistant
            return num_tokens
        else:
            raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
    See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
