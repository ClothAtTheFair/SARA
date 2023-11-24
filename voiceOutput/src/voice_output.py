import yaml, io, queue, os, threading
from gtts import gTTS
import redit

class VoiceOutput:
    def __init__(self):
        pass

    def save_mp3(self, text):
        language = 'en'
        myobj = gTTS(text=text, lang=language, slow=False)
        myobj.save("output.mp3")

    def play_mp3(self):
        os.system("mpg321 output.mp3")

    def main(self, text):
        pass