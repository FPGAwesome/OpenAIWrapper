# Using this for reference: https://www.geeksforgeeks.org/create-a-voice-recorder-using-python/

import sounddevice as sd
from scipy.io.wavfile import write
import os



class AudioProcess:
    def __init__(self):
        self.freq = 44100
        self.duration = 10
        self.channels = 1

    def record_sample(self,duration=None):
        print("Beginning record..")
        # Start recorder with the given values of 
        # duration and sample frequency
        if duration==None:
            recording = sd.rec(int(self.duration * self.freq), 
                        samplerate=self.freq, channels=self.channels)
        else:
            recording = sd.rec(int(duration * self.freq), 
                        samplerate=self.freq, channels=self.channels)

        # Record audio for the given number of seconds
        sd.wait()
        print("Recording finished!")

        if not os.path.exists('temp'):
            os.makedirs('temp')

        # for now simply dump a recording to this file, over-writing it
        write("temp/recording_sample.wav", self.freq, recording)

        return recording