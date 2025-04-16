import speech_recognition as sr

recognizer = sr.Recognizer()
def thread_listen():
    with sr.Microphone() as source:
        try:
            print("listening..")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)
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
