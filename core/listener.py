import speech_recognition as sr
import time
from core.mute_control import is_muted

recognizer = sr.Recognizer()

def listen_for_command(timeout=10, phrase_time_limit=8):
    with sr.Microphone() as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.WaitTimeoutError:
            return "timeout"
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            print("Google Speech API is unreachable!")
            return None
