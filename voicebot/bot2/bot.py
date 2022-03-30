import speech_recognition as sr                                                    # importing speech recognition API
from chatterbot import ChatBot                                                     # Importing ChatterBot API
from chatterbot.trainers import ListTrainer                                        # importing list Trainer from chatter-bot trainers
from chatterbot.trainers import ChatterBotCorpusTrainer
import os                                                                          
import speak                                                                       # speak is an instance of gTTS API for bot responses
import speak2                                                                      # speak2 is for storing the name of the user 
bot = ChatBot('Chatbot', logic_adapters=[                                          #creating a chatter-bot instances
 {
  'import_path': 'chatterbot.logic.BestMatch'                                      # logic adapters to get the best match response with highest confidence
 },
 
 {
  'import_path': 'chatterbot.logic.MathematicalEvaluation'                         # logic adapter for mathematical calculation (arithmetic operation)
 },

 { 
  'import_path': 'chatterbot.logic.LowConfidenceAdapter',                          # confidence adapter compare input with the trainer and pass response
  'threshold': 0.40,                                                               # depending on threshold value 
  'default_response': 'I am Sorry, but I do not understand.'                       # default response for input with lowest confidence response
 }
  ]
   )
bot.set_trainer(ListTrainer)                                                       # a trainer module for chatbot, initiating a listtrainer with bot.set 

conv = open('./voicebot/bot2/chats.txt','r').readlines()                                           # 'conv' is a list trainer,.readlines() reading the input and response  
                                                                                   #  from this listtrainer
bot.train(conv)                                                                    #  bot.train() is a module to train the bot to pass response to user input

print('Friday:Hi I am Friday, Who is on the other side?')

reply1 = str('Hi I am Friday, Who is on the other side?')                          # here the string statement is stored in reply1 which will be pass through   
                                                                                   # speak module for speech conversion
lang = 'en-uk'                                                                     # language for the API to reply
speak.speak_text(reply1)
speak.tts(reply1, lang)                                                            # text to speech conversion 

r = sr.Recognizer()    
                                                            # recognizer module from speech recognition (.Recognizer())
while True:

 with sr.Microphone() as source:                                              # Microphone module from pyaudio (.Microphone())
  print("Silence please, calibrating bckground noise")
  r.adjust_for_ambient_noise(source)
  r.pause_threshold = 0.7
  print('Listening')  
  audio1 = r.listen(source)                                                    # recognizing user audio input with r.listen() and storing in audio1
  with open("./tmp/audio1.wav", "wb") as file:
    file.write(audio1.get_wav_data())
  try:
   print('Recognizing')
   name1 = r.recognize_google(audio1)                                              # .recognize_google() recognizes the audio with google database and 
   name1 = name1.lower()                                                           #  stores the response in name1
   print("Did you say "+name1)
   speak.speak_text(name1)
  #  print("Say")                                                                               # convert it to text
  #  name= input ("you: " + str(name1))                                              # collecting input from recognized audio
  #  print("Done")   
  except  sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
  except  sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
  except sr.HTTPError as e: 
    print(f"HTTP error: {e}")
   
  name1 = 'Jie'
  print ("Friday:Hi", name1,"how may I help? ")  
  reply2 = "Hi " + name1 +  " how may I help?"   
  lang = 'en-uk'
  speak.speak_text(reply2)
  # speak2.tts(reply2, lang)                                                        # text to speech conversion 
  
  while True:

   with sr.Microphone() as source:

    r.adjust_for_ambient_noise(source)
    audio = r.listen(source)
    try:
    #  text = r.recognize_google(audio)                                             # speech to text conversion
     text = 'what is the weather today'
    #  print ("Say")
     request = input ("you: " + str(text))
    #  print("Done")  
    except  sr.UnknownValueError:
     print("Google Speech Recognition could not understand audio")
    except  sr.RequestError as e:
     print("Could not request results from Google Speech Recognition service; {0}".format(e))
    
   if request.strip() != 'Bye':                                                  # if statement to check for user input if its not bye the get response from trainer
  
    reply = str(bot.get_response(text))                                          # bot.get_response() check for the responses from the list trainer and reply back 
    print ("Friday: ", reply)    
    lang = 'en-uk'
    speak.speak_text(reply)
    # speak.tts(reply, lang)                                                       # text to speech conversion
    
   if request.strip() == 'Bye':
    print('Friday : Bye')
    break
 
