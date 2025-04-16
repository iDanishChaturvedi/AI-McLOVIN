import webbrowser
from core.responder import respond
from controls.play_music import play_music_yt

def control_browser(command):
    command = command.lower()
    if "google search for" in command:
        query = command.replace("google search for", "").strip()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            respond(f"Searching for {query}")
            return True
    elif "on youtube" in command:
        parts = command.split("on youtube")[0].split() 
        song_name = " ".join(parts[1:])
        play_music_yt(song_name)
        respond("playing your video")
        return True
    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        respond("Opening YouTube")
        return True
    return False
