from whisper import whisper

whispy=whisper.Whisper(verbose=1)

output=whispy.talk_to(3) # 3 second clip
print(output["text"])

output=whispy.talk_to(5) # 5 second clip
print(output["text"])

whispy.dump_history()