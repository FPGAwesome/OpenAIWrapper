from whisper import whisper
from chatgpt import chatgpt

class Talk2GPT:
    def __init__(self,prompt="You are an assistant.",verbose=0) -> None:
        self.chatter = chatgpt.ChatGPT(system=prompt,verbose=verbose)
        self.speaker = whisper.Whisper(verbose=verbose)

        self.verbose=verbose

    def speak_to(self,duration=5):
        message=self.speaker.talk_to(duration=duration)
        reply=self.chatter(message.text)
        if self.verbose>0:
            print(reply)
        return reply
