import pyttsx3

engine = pyttsx3.init()

def respond(text):
    engine.say(text)
    engine.runAndWait()

def stop_response():
    engine.stop()
