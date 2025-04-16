import datetime
import time
import threading
from core.responder import respond, stop_response
import pygame
import os
import re
from random import choice
from core.memory_manager import load_memory, save_memory, add_reminder, pop_due_reminders

alarms = []
def get_time():
    now = datetime.datetime.now()
    return choice([now.strftime("It’s %I:%M %p"), now.strftime("It's %H:%M hours")])

def get_date():
    today = datetime.date.today()
    return f"Today is {today.strftime('%A, %d %B, %Y')}"
def get_day():
    day = datetime.datetime.now()
    return f"It's {day.strftime('%A')}"

def set_alarm(alarm_time_str):
    try:
        alarm_time = datetime.datetime.strptime(alarm_time_str, "%H:%M")
        now = datetime.datetime.now()
        today_alarm = datetime.datetime.combine(now.date(), alarm_time.time())

        if today_alarm < now:
            today_alarm += datetime.timedelta(days=1)

        alarms.append(today_alarm)

        threading.Thread(target=wait_for_alarm, args=(today_alarm,), daemon=True).start()

        return f"Alarm set for {today_alarm.strftime('%I:%M %p')}."
    except ValueError:
        return "Sorry, I didn't understand the time format. Please say it like 'set alarm for 06:30'."

def parse_relative_alarm(command):
    try:
        # Extract duration using regex
        match = re.search(r"wake me up in (\d+)\s*(minute|minutes|hour|hours)", command)
        if not match:
            return "I couldn't understand the duration. Try 'wake me up in 10 minutes'."

        number = int(match.group(1))
        unit = match.group(2)

        now = datetime.datetime.now()
        if "hour" in unit:
            target_time = now + datetime.timedelta(hours=number)
        else:
            target_time = now + datetime.timedelta(minutes=number)

        alarms.append(target_time)
        threading.Thread(target=wait_for_alarm, args=(target_time,), daemon=True).start()

        return f"Alarm set for {target_time.strftime('%I:%M %p')}."
    except Exception as e:
        print(f"[Alarm Parse Error]: {e}")
        return "Something went wrong while setting the alarm."

def parse_named_reminder(command):
    try:
        command = command.lower()
        memory = load_memory()

        # Absolute
        abs_match = re.search(r"remind me to (.+?) at (\d{1,2}(:\d{2})?\s*(am|pm)?)", command)
        if abs_match:
            message = abs_match.group(1).strip().capitalize()
            time_str = abs_match.group(2).strip()

            reminder_time = parse_time_string(time_str)
            if not reminder_time:
                return "I couldn't understand the time format."

            add_reminder(memory, message, reminder_time)
            threading.Thread(target=wait_for_named_alarm, args=(reminder_time, message), daemon=True).start()
            return f"Reminder set to {message} at {reminder_time.strftime('%I:%M %p')}."

        # Relative
        rel_match = re.search(r"remind me in (\d+)\s*(minutes|minute|hours|hour) to (.+)", command)
        if rel_match:
            amount = int(rel_match.group(1))
            unit = rel_match.group(2)
            message = rel_match.group(3).strip().capitalize()

            now = datetime.datetime.now()
            delta = datetime.timedelta(minutes=amount) if "minute" in unit else datetime.timedelta(hours=amount)
            target_time = now + delta

            add_reminder(memory, message, target_time)
            threading.Thread(target=wait_for_named_alarm, args=(target_time, message), daemon=True).start()
            return f"Reminder to {message} in {amount} {unit}."

        return None
    except Exception as e:
        print(f"[Reminder Error]: {e}")
        return "I couldn't set the reminder."
    
def parse_time_string(time_input):
    try:
        time_input = time_input.lower().replace(".", "")
        now = datetime.datetime.now()

        try:
            parsed = datetime.datetime.strptime(time_input, "%I:%M %p")
        except:
            parsed = datetime.datetime.strptime(time_input, "%I %p")

        result = datetime.datetime.combine(now.date(), parsed.time())
        if result < now:
            result += datetime.timedelta(days=1)
        return result
    except:
        return None

def start_due_reminders_on_boot():
    memory = load_memory()
    now = datetime.datetime.now()
    reminders = memory.get("reminders", [])
    updated_reminders = []

    for rem in reminders:
        try:
            rem_time = datetime.datetime.strptime(rem["time"], "%Y-%m-%d %H:%M:%S")
            message = rem["message"]

            if rem_time > now:
                # Future reminder - restart thread
                threading.Thread(target=wait_for_named_alarm, args=(rem_time, message), daemon=True).start()
                updated_reminders.append(rem)
            else:
                # Missed reminder - say 2 times, then discard
                for _ in range(2):
                    respond(f"You missed a reminder: {message}")
                    time.sleep(3)

        except Exception as e:
            print(f"[Reminder Resume Error]: {e}")

    # Save only upcoming ones
    memory["reminders"] = updated_reminders
    save_memory(memory)

def wait_for_named_alarm(reminder_time, message):
    time.sleep(1.5)
    while datetime.datetime.now() < reminder_time:
        time.sleep(5)
    memory = load_memory()  
    pop_due_reminders(memory)
    time.sleep(0.5)
    print(f"Reminder: {message} at {reminder_time}")
    return True

def wait_for_alarm(alarm_time):
    while datetime.datetime.now() < alarm_time:
        time.sleep(5)

    pygame.mixer.init()
    pygame.mixer.music.load(r"C:\Users\Dannyboi\Downloads\alarm_music.mp3")
    pygame.mixer.music.play()
    

def control_calendar(command):
    lowered = command.lower()
    if lowered.startswith("what time") or lowered.startswith("current time"):        
        return get_time()
    elif lowered.startswith("what date") or "today's date" in lowered:
        return get_date()
    elif lowered.startswith("what day") or "today's day" in lowered:
        return get_day()
    elif lowered.startswith("remind me"):
        return parse_named_reminder(command)
    elif "set alarm for" in lowered or lowered.startswith("wake me up"):
        if "wake me up" in lowered:
            return parse_relative_alarm(lowered)
        time_str = lowered.split("set alarm for")[-1].strip()
        return set_alarm(time_str)
    return None
