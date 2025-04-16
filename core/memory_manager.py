import json
import os
import datetime

MEMORY_PATH = r"C:\Users\Dannyboi\Desktop\mclovin_Ai\data\smart_memory.json"
CONTEXT_LIMIT = 8
SUMMARY_LIMIT = 5

def load_memory():
    if os.path.exists(MEMORY_PATH):
        with open(MEMORY_PATH, "r") as file:
            return json.load(file)
    return {
        "context": [],
        "summaries": [],
        "personality": "default",
        "long_term": {"name": "", "preferences": ""}
    }

def save_memory(memory):
    with open(MEMORY_PATH, "w") as file:
        json.dump(memory, file, indent=4)

def reset_memory():
    save_memory({
        "context": [],
        "summaries": [],
        "personality": "default",
        "long_term": {"name": "", "preferences": ""}
    })

def summarize_memory(memory):
    context = memory.get("context", [])

    # Summarize only if enough conversation has built up
    if len(context) >= CONTEXT_LIMIT:
        batch = context[:CONTEXT_LIMIT]

        # Topic guess
        last_user_msg = batch[-1].get("user", "") if batch else ""
        topic_guess = last_user_msg.strip().capitalize() or "General Topic"

        summary = f"# Summary Topic: {topic_guess}\n---\n"

        for pair in batch:
            user_input = pair.get("user", "").strip()
            assistant_reply = pair.get("assistant", "").strip()

            # Discard overly short responses 
            if len(assistant_reply) < 5:
                continue

            # Trim long replies
            if len(assistant_reply) > 250:
                assistant_reply = assistant_reply[:250].rsplit(".", 1)[0] + "..."

            summary += f"User said: {user_input}\nAI replied: {assistant_reply}\n\n"

        summary = summary.strip()

        # Save & manage summaries
        memory.setdefault("summaries", []).append(summary)

        # Keep only the last 5 summaries
        if len(memory["summaries"]) > 5:
            memory["summaries"] = memory["summaries"][-5:]

        # Remove summarized part from context
        memory["context"] = context[CONTEXT_LIMIT:]

    return memory

def update_long_term(memory, key, value):
    memory["long_term"][key] = value
    save_memory(memory)

def get_long_term_fact(memory, key):
    return memory["long_term"].get(key)

def add_reminder(memory, message, remind_time):
    reminder = {
        "message": message,
        "time": remind_time.strftime("%Y-%m-%d %H:%M:%S")
    }
    memory.setdefault("reminders", []).append(reminder)
    save_memory(memory)

def pop_due_reminders(memory):
    now = datetime.datetime.now()
    reminders = memory.get("reminders", [])
    remaining = []

    for rem in reminders:
        rem_time = datetime.datetime.strptime(rem["time"], "%Y-%m-%d %H:%M:%S")
        if rem_time > now:
            remaining.append(rem)

    memory["reminders"] = remaining
    save_memory(memory)

