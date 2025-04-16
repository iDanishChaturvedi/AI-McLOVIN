from features.whatsapp_handler import send_text_to, send_voice, voice_call, video_call
from core.responder import respond
import speech_recognition as sr
import pyautogui as gui
import time
def control_screen(command):
    command = command.lower()
    if command.startswith("send message"):
        name = command.replace("send message to", "").strip()
        time.sleep(1)
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            respond("ok tell me")
            audio = recognizer.listen(source, timeout = 5)
        message = recognizer.recognize_google(audio)
        send_text_to(name, message)
        return True
    elif command.startswith("voice call"):
        name = command.replace("voice call", "").strip()
        voice_call(name)
        return True
    elif command.startswith("send voice note"):
        name = command.replace("send voice note to", "").strip()
        send_voice(name)
        return True
    elif command.startswith("video call"):
        name = command.replace("video call", "").strip()
        video_call(name)
        return True
    elif command == "skip ad":
        res = gui.locateCenterOnScreen(r"C:\Users\Dannyboi\Desktop\mclovin_Ai\images\skip_Ad.png", confidence = 0.9)
        time.sleep(2)
        if res:
            gui.moveTo(res, duration=1)  
            time.sleep(2)
            gui.click()
            return True
    elif command == "click on search":
        search = [r"C:\Users\Dannyboi\Desktop\mclovin_Ai\images\search1.png",r"C:\Users\Dannyboi\Desktop\mclovin_Ai\images\search2.png"]
        for s in search:
            res = gui.locateCenterOnScreen(s, confidence = 0.9)
            time.sleep(2)
            if res:
                gui.moveTo(res, duration = 1)
                time.sleep(2)
                gui.click()
                return True
    elif command.startswith("type for me"):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            respond("ok tell me")
            recognizer.adjust_for_ambient_noise(source)
            try:
                audio = recognizer.listen(source, timeout=5)
                com = recognizer.recognize_google(audio)
                time.sleep(1)
                gui.write(com)
            except sr.WaitTimeoutError:
                return None
            except sr.UnknownValueError:
                return None
            except sr.RequestError:
                print("Google Speech API is unreachable!")
                return None
        return True
    elif command == "play next":
        search = [r"C:\Users\Dannyboi\Desktop\mclovin_Ai\images\next1.png",r"C:\Users\Dannyboi\Desktop\mclovin_Ai\images\next2.png"]
        for s in search:
            res = gui.locateCenterOnScreen(s, confidence = 0.8)
            time.sleep(2)
            if res:
                gui.moveTo(res, duration = 1)
                time.sleep(2)
                gui.click()
                return True
    elif command == "play previous":
        res = gui.locateCenterOnScreen(r"C:\Users\Dannyboi\Desktop\mclovin_Ai\images\previous.png", confidence = 0.8)
        time.sleep(2)
        if res:
            gui.moveTo(res, duration=1)  
            time.sleep(2)
            gui.click()
            return True         
    return False

