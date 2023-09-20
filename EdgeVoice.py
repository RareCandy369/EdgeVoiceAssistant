from EdgeGPT.EdgeUtils import Query
import speech_recognition as sr
import openai, pyttsx3
import sys, whisper, warnings, time

# Initialize the OpenAI API
api_key = "[enter API key here, minus brackets]"
openai.api_key = api_key

#Initialize speach recognition module
recognizer = sr.Recognizer()
microphone = sr.Microphone() 

#Function to convert speech to text
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

#Function to listen for wake-up command
def listen_for_wake_word():
    print("Listening for wake-up command...")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        
    try:
        #Convert speech to text
        wake_word = recognizer.recognize_google(audio).lower()
        if "wake up" in wake_word:
            return True
        else:
            return False
    except sr.UnknownValueError:
        return False
    except sr.RequestError as e:
        print("Could not request results: {0}".format(e))
        return False

#Function to listen for a query and generate a response
def listen_for_query():
    print("Listening for query...")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        #Convert query to text
        query = recognizer.recognize_google(audio)
        print("You said: " + query)
              
        #Use Bing to generate response
        print('User: ' + query)
        output = Query(query)
        print('Bing: ' + str(output))
        speak(str(output))
        print('\n Say "Bing" to wake me up. \n')
        bing_engine = True
        listening_for_wake_word = True

    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results: {0}".format(e))

#Main loop
while True:
    if listen_for_wake_word():
        listen_for_query()
