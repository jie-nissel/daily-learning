from gtts import gTTS                                                                 # importing google text-to-speech API
import pyglet                                                                         # importing pyglet for audio playback decoding 
import time, os     
import pyttsx3                                                     
def speak_text(command):
    engine = pyttsx3.init()
    # getter method(gets the current value
    # of engine property)
    voices = engine.getProperty('voices')
      
    # setter method .[0]=male voice and 
    # [1]=female voice in set Property.
    engine.setProperty('voice', voices[0].id)
      
    # Method for the speaking of the the assistant
    engine.say(command)  
      
    # Blocks while processing all the currently
    # queued commands
    engine.runAndWait()

# text to audio
def tts(text, lang):                                                                  # defining variable 'text'  and 'lang'
    file = gTTS(text = text, lang = lang)
    filename = './tmp/temp.mp3'     # Store the converted file into a temporary folder 
    file.save(filename)
    
    # music = pyglet.media.load(filename, streaming = False)                            # its decode the saved file and load it 
    # music.play()   
    # speak_audio(file)                                                                   # music.play() plays the saved audio

    # time.sleep(music.duration)
    # os.remove(filename)                                                               # temporary speech file is removed