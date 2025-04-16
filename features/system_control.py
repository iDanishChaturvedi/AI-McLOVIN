import os
from core.responder import respond
import pyautogui as gui
import time
from controls.cursor_handler import move_cursor
from controls.volume_control import set_volume, mute_unmute
import wmi

def set_brightness(level):
    c = wmi.WMI(namespace='wmi')
    methods = c.WmiMonitorBrightnessMethods()[0]
    methods.WmiSetBrightness(level, 0)
    
def control_system(command):
    command = command.lower()

    if "system shutdown" in command:
        gui.hotkey('win','x')
        respond("Shutting down. ahh dont do this to me")
        time.sleep(3)
        gui.press('u')
        gui.press('u')
        return True
    elif "system restart" in command:
        gui.hotkey('win','x') 
        respond("Coming Back boys")
        time.sleep(3)
        gui.press('u')
        gui.press('r')
        return True
    elif "system sleep" in command:
        gui.hotkey('win','x')
        respond("System going sleep, see ya gangstas")
        time.sleep(3)
        gui.press('u')
        gui.press('s')
        return True
    elif "system lock" in command:
        respond("Locking screen")
        time.sleep(2)
        gui.hotkey('win','l')
        return True
    elif "take screenshot" in command:
        screenshot = gui.screenshot()
        respond("Screenshot taken")
        return True
    elif "volume" in command and any(char.isdigit() for char in command):
        try:
            parts = command.split()
            #finds the first number in the string.
            volume_number = int(next(filter(str.isdigit, parts)))
            if 0 <= volume_number <= 100:
                set_volume(volume_number)  # use the module
                print(f"Volume set to {volume_number}%")
            else:
                print("Volume must be between 0 and 100.")
        except ValueError:
            print("Invalid volume number.")
        return True
    elif "volume up to" in command or "volume down to" in command:
        try:
            parts = command.split()
            volume_number = int(next(filter(str.isdigit, parts)))
            if 0 <= volume_number <= 100:
                set_volume(volume_number)
                print(f"Volume set to {volume_number}%")
            else:
                print("Volume must be between 0 and 100.")
        except ValueError:
            print("Invalid volume number.")
        return True
    elif "mute system" in command:
        mute_unmute(1)
        return True
     # Window controls
    elif "maximize window" in command or "maximise window" == command:
        gui.hotkey('win', 'up')
        #respond("Window maximized")
        return True

    elif "minimize window" in command or "minimise window" == command:
        gui.hotkey('win', 'down')
        #respond("Window minimized")
        return True

    elif "restore window" == command:
        gui.hotkey('win', 'shift', 'up')
        #respond("Window restored")
        return True

    elif "close window" == command:
        gui.hotkey('alt', 'f4')
        #respond("Window closed")
        return True

    elif "new tab" == command:
        gui.hotkey('ctrl', 't')
        #respond("Opened new tab")
        return True

    elif "close tab" == command:
        gui.hotkey('ctrl', 'w')
        #respond("Closed tab")
        return True

    elif "new window" == command:
        gui.hotkey('ctrl', 'n')
        #respond("Opened new window")
        return True

    elif "switch window" == command:
        gui.keyDown('alt')
        gui.press('tab')
        gui.keyUp('alt')
        #respond("Switched window")
        return True
    elif "switch back window" == command:
        gui.keyDown('alt')
        gui.press('tab')
        return True
    elif "show desktop" == command:
        gui.keyDown('win')
        gui.press('d')
        return True
    elif "press escape" == command:
        gui.press('esc')
        return True
    elif "press enter" == command:
        gui.press('enter')
        return True
    elif "press tab" == command:
        gui.press('tab')
        return True
    elif "next tab" == command:
        gui.hotkey('ctrl', 'tab')
        return True
    elif "back tab" == command:
        gui.hotkey('ctrl', 'shift', 'tab')
        return True
    elif "open task view" == command:
        gui.hotkey('win', 'tab')
        return True
    elif "move right" == command:
        gui.press('right')
        return True
    elif "move left" == command:
        gui.press('left')
        return True
    # Scrolling
    elif "go back" == command:
        gui.keyDown('alt')
        gui.press('left')
        return True
    elif "go forward" == command:
        gui.keyDown('alt')
        gui.press('right')
        return True
    elif "scroll down" == command:
        gui.press('pagedown')
        #respond("Scrolling down")
        return True
    elif "scroll up" == command:
        gui.press('pageup')
        #respond("Scrolling up")
        return True
    elif "click" == command:
        gui.click()
        return True
    elif "double click" == command:
        gui.doubleClick()
        return True
    elif command.startswith("move"):
        res = command.replace("move", "").strip()
        speed = res.split()[0]
        if "up" in res:
            move_cursor("up", speed)
        elif "down" in res:
            move_cursor("down", speed)
        elif "left" in res:
            move_cursor("left", speed)
        elif "right" in res:
            move_cursor("right", speed)

        return True
    elif command.startswith("set brightness"):
        res = command.replace("set brightness","").strip()
        set_brightness(res)
        return True
    return False
