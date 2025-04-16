import pyautogui as gui
import subprocess
import time

def openApp(text):
    try:
        subprocess.run(text)
    except Exception as e:
        gui.press("win")
        time.sleep(3)
        gui.write(text)
        time.sleep(3)
        gui.press("enter")
