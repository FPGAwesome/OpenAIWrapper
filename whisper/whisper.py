import csv
import openai
from .audioprocess import AudioProcess

class Whisper:
    def __init__(self, verbose=0):
        self.mic = AudioProcess()
        self.verbose=verbose
        self.history=[]

    def talk_to(self,duration=None):
        print('Beginning record for ' + str(duration) + ' seconds')
        if duration != None:
            recording = self.mic.record_sample(duration=duration)
        else:
            recording = self.mic.record_sample()
        audio_file= open("temp/recording_sample.wav", "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)

        if self.verbose > 0:
            print(transcript)

        self.history.append(transcript['text'])

        return transcript
    
    def print_history(self):
        for i,h in enumerate(self.history):
            print(i,h)

    def dump_history(self,filename='whisper_history.csv'):
        with open(filename,'w') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',')
            for i,h in enumerate(self.history):
                csvwriter.writerow([i,h])