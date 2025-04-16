import pyautogui as gui
import time
from core.responder import respond
from controls.alias_handler import resolve_alias
import speech_recognition as sr

def open_whatsApp():
    gui.press("win")
    time.sleep(3)
    gui.write("whatsapp")
    time.sleep(3)
    gui.press("enter")

def search_whats(name_alias):
    name = resolve_alias(name_alias)
    time.sleep(2)
    gui.hotkey('ctrl', 'f')
    time.sleep(1)
    gui.write(name)
    time.sleep(3)
    gui.click(x=299,y=233)
    return name
def send_text_to(name, text):
    open_whatsApp()
    contact = search_whats(name)
    time.sleep(3)
    gui.write(text)
    time.sleep(1)
    gui.press('enter')
    respond(f"Message sent to {contact}")
def send_voice(name):
    open_whatsApp()
    contact = search_whats(name)
    time.sleep(1)
    search = gui.locateCenterOnScreen(r"C:\Users\Dannyboi\Desktop\mclovin_Ai\images\voice_Record.png", confidence = 0.9)
    time.sleep(2)
    if search:
        gui.moveTo(search, duration=1)  
        time.sleep(2)
        gui.click()
        respond("Recording")
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            try:
                audio = recognizer.listen(source, timeout = 5)
                gui.click()
                respond("Voice note sent")
            except sr.WaitTimeoutError:
                delete = gui.locateCenterOnScreen(r"C:\Users\Dannyboi\Desktop\mclovin_Ai\images\delete_bin.png", confidence = 0.9)
                time.sleep(2)
                if delete:
                    gui.moveTo(search, duration=1)  
                    time.sleep(2)
                    gui.click()
                    respond("no input detected")
    else:
        respond("Try again")

def voice_call(name):
    open_whatsApp()
    contact = search_whats(name)
    time.sleep(1)
    search =  gui.locateCenterOnScreen(r"C:\Users\Dannyboi\Desktop\mclovin_Ai\images\voice_mic.png", confidence = 0.9)
    time.sleep(2)
    if search:
        gui.moveTo(search, duration=1)  
        time.sleep(2)
        gui.click()

def video_call(name):
    open_whatsApp()
    contact = search_whats(name)
    time.sleep(1)
    search =  gui.locateCenterOnScreen(r"C:\Users\Dannyboi\Desktop\mclovin_Ai\images\video_call.png", confidence = 0.9)
    time.sleep(2)
    if search:
        gui.moveTo(search, duration=1)  
        time.sleep(2)
        gui.click()

        
    
    

