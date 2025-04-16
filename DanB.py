import os
import sys
import time
from features.app_opener import control_app
from features.browser import control_browser
from features.system_control import control_system
from features.calendar_alarm import (control_calendar, start_due_reminders_on_boot)
from features.screen_control import control_screen
from core.mute_control import mute_assistant, is_muted, unmute_assistant
from core.listener import listen_for_command
from core.responder import respond
from core.pre_recorded import play_clip
from core.smart_mode import process_smart_mode
from core.memory_manager import load_memory
from core.threader import thread_listen
import datetime
from config import mclovin_triggers
from ai.chat import generate_response

inactivity_limit = 180
last_command_time = datetime.datetime.now()
sleep_words = ["hibernate", "sleep mode"]
wake_word = "wake up"

def process_command(command):
    #no command detect
    if not command or len(command.strip()) < 3:
        return

    if command == "timeout":
        return
        
    # Feature-based controls
    if control_system(command) or control_app(command) or control_browser(command) or control_screen(command):
        return

    calendar_response = control_calendar(command)
    if calendar_response:
        respond(calendar_response)
        return
    
    # Smart Mode takes priority
    smart_response = process_smart_mode(command)
    if smart_response:
        respond(smart_response)
        return

    # Pre-recorded response check
    for keyword in mclovin_triggers:
        if command.lower() == keyword:
            play_clip(keyword)
            return
    if command == wake_word:
        respond("I'm awake and listening already")
        return
    for w in sleep_words:
        if command.lower() == w:
            respond("Sleep mode on")
            mute_assistant()
            return
        
    # Exit commands
    if command.lower() in ["go sleep", "quit", "stop"]:
        respond("Goodbye!")
        sys.exit(0)

    # if control_spotify(command): return (optional)

    # Default AI Response (only when not in Smart Mode)
    response = generate_response(command)
    print("AI:", response)
    respond(response)

def sleep_mode(command):
    if not command or command == "timeout":
        return 
    elif command.lower() == wake_word:
        if is_muted():
            unmute_assistant()
            respond("I'm awake, listening..")
    else:
        respond("I'm sleeping, waiting for wake word")
        return 

#️ Main loop to keep listening
def main():
    global last_command_time
    start_due_reminders_on_boot()
    while True:
        now = datetime.datetime.now()

        if not is_muted() and (now - last_command_time).total_seconds() > inactivity_limit:
            print("No interaction for a while. Going to sleep...")
            mute_assistant()
            continue
        if is_muted():
            print("sleep mode on")
            com = thread_listen()
            sleep_mode(com)
            time.sleep(1)
            continue
        command = listen_for_command()
        if command:
            last_command_time = now
        process_command(command)
        time.sleep(1)

if __name__ == "__main__":
    main()
