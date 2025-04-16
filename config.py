import os

# Load GPT4All with Qwen2-1.5B-Instruct
MODEL_PATH = r"C:\Users\Dannyboi\AppData\Local\nomic.ai\GPT4All\qwen2-1_5b-instruct-q4_0.gguf"
clips_dir = r"C:\Users\Dannyboi\Desktop\mclovin_Ai\voices"

mclovin_triggers = {
    "what is your name": ["COPSIAMMCCLOVIN-voice_12[1]-vocals-Emajor-97bpm-440hz.m4a.wav", "myname.wav", "myname2.wav", "iammclovin.wav"],
    "are you sure": ["yay-voice1.mp3.wav", "yeayea-yeayea-voice1.mp3.wav.wav"],
    "you are boring": ["you'rewrong-voice1.mp3.wav", "youalwayscallmepus-voice1.mp3.wav", "dontipromiseyou-voice3.mp3.wav"],
    "yo": ["yooguyssup-voice2.mp3.wav"],
    "i am bored": ["wydtonight-voice1.mp3.wav"],
    "how is the black thong": ["time.wav"],
    "am i sweet": ["sosweet-voice1.mp3.wav"],
    "how old are you": ["oldenough-voice_7[1]-vocals-Dmajor-63bpm-440hz.m4a.wav", "theysay21-theysay21-voice2.mp3.wav.wav", "imtrynalookolder-voice3.mp3.wav"],
    "i did not get you": ["listenup-voice2.mp3.wav"],
    "i want to party": ["letsparty-voice1.mp3.wav"],
    "do you like water": ["ilovethatstuffdrinkingitforyears-voice_5[1]-D-94bpm-440hz.m4a.wav"],
    "do you know how my friend looks": ["IDONTREALLYKNOWHOWHELOOKSLIKE-voice_7[1]-vocals-Dmajor-63bpm-440hz.m4a.wav"],
    "hello": ["hellomindy.wav"],
    "greet my people": ["greetings-voice1.mp3.wav"],
    "how is your giggle": ["nonsense-voice_5[1]-D-94bpm-440hz.m4a.wav"],
    "say no": ["nono-voice2.mp3.wav", "nowayman-voice3.mp3.wav"],
    "you so good": ["sosweet-voice1.mp3.wav"],
    "codes": ["ahole-voice1.mp3.wav", "atlunchimgoingtothesameplace.wav"]
    }
