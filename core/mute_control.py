mute_listening = False  # Global mute flag

def mute_assistant():
    global mute_listening
    mute_listening = True

def unmute_assistant():
    global mute_listening
    mute_listening = False

def is_muted():
    return mute_listening
