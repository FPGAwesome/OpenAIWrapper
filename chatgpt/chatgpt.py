# Adapted (previously taken, but it's going through a bit of tailoring) from https://til.simonwillison.net/gpt3/chatgpt-api
import csv
import openai
import json
import tiktoken

class ChatGPT:

    def __init__(self, system="", verbose=0, model="gpt-3.5-turbo",num_filter=4097):
        self.system = system
        self.messages = []
        self.message_tokens = [] # token usage of given index
        self.num_filter=num_filter

        self.model=model
        # for some token counting utility
        self.tikmodel=self.model
        if model=="gpt-4":
            self.tikmodel="gpt-3.5-turbo" # until tiktoken works for gpt4
                                          # it's probably safe to assume the same tokenizer anyways
        self.encoding=tiktoken.encoding_for_model(self.tikmodel)

        self.verbose=verbose

        if self.system:
            self.messages.append({"role": "system", "content": system})
            self.message_tokens.append(len(self.encoding.encode(system)))


        # Model-related variables

        
    
    def __call__(self, message):
        print(message)
        self.message_tokens.append(len(self.encoding.encode(message)))
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.message_tokens.append(len(self.encoding.encode(result)))
        self.messages.append({"role": "assistant", "content": result})
        if self.verbose > 1:
            print(self.messages)
            print(self.message_tokens)
        return result
    
    # Make sure we're only sending a maximum of 4097 tokens
    # this is a private method unless there's some utility I'm missing?
    # Maybe something for UI's idk at the moment
    def __token_trim(self, messages):
        tot_tokens, msgs_to_use = self.count_tokens(messages)
        print('Sum of tokens: ', tot_tokens)
        return msgs_to_use


    # can call different models, for these purposes it's really only useful
    # to use the two different available chatgpt models
    # gpt-3.5-turbo and gpt-3.5-turbo-0301
    # the latter of which doesn't pay strong attention to system messages in favor of the user prompts
    def execute(self):
        print(self.messages)
        send_message=self.__token_trim(self.messages)
        completion = openai.ChatCompletion.create(model=self.model, messages=send_message)
        # Uncomment this to print out token usage each time, e.g.
        # {"completion_tokens": 86, "prompt_tokens": 26, "total_tokens": 112}
        if self.verbose>0:
            print(completion.usage)
        return completion.choices[0].message.content
    
    # Because why shouldn't you switch mid-prompt?
    def set_model(self,model):
        if self.verbose>0:
            print('Changing model to: ',model)
        self.model=model

    # Avoid accessing instance variables
    def get_model(self):
        return self.model
    
    def clear_messages(self):
        self.messages=[]
        
        if self.system:
            self.messages.append({"role": "system", "content": self.system})
            self.message_tokens.append(len(self.encoding.encode(self.system)))
    
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
    def save_chat(self, filename='saved_chat.json'):
        with open(filename, 'w') as f:
            json.dump(self.messages, f)

    def load_chat(self, filename='saved_chat.json'):
        with open(filename, 'r') as f:
            self.messages = json.load(f)

    # Make the model we use for encoding overridable because that sounds
    # cool to do. Not going to support get_encoding at this time because
    # I don't want or need it for anything
    # num_filter is used for limiting sent tokens
    def count_tokens(self, messages=None, model=None):
        encoding = self.encoding
        if model is not None:
            encoding = tiktoken.encoding_for_model(model)
        else:
            model = self.tikmodel

        if model == "gpt-3.5-turbo":
            if messages is None:
                messages = self.messages

            num_tokens = 2 # there's an off by two error, this is the obvious fix
                           # not like, figuring out why, or anything
            msgs_to_use = []
            for message in messages[::-1]:  # We'll go in reverse to keep the most recent messages
                tokens_length = 4  # <im_start>{role/name}\n{content}<im_end>\n
                for key, value in message.items():
                    tokens_length += len(encoding.encode(value))
                    if key == "name":
                        tokens_length += -1

                # Count tokens limit, with a 100 tokens margin for the assistant's message and request formatting
                if num_tokens + tokens_length <= self.num_filter - 100:
                    num_tokens += tokens_length
                    msgs_to_use.append(message)
                else:
                    break

            return num_tokens, msgs_to_use[::-1]
        else:
            raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
    See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
