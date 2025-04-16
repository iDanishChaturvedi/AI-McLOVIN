from core.responder import respond
from controls.open_app import openApp

def control_app(command):
    command = command.lower()
    if "open app" in command:
        query = command.replace("open app","").strip()
        if query:
            openApp(query)
            respond(f"opening {query}")
            return True
    return False
