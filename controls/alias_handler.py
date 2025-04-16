import json
import os

ALIAS_PATH = r"C:\Users\Dannyboi\Desktop\mclovin_Ai\controls\aliases.json"

def load_alias_file():
    if os.path.exists(ALIAS_PATH):
        with open(ALIAS_PATH, "r") as file:
            return json.load(file)
    return {}

def resolve_alias(name):
    aliases = load_alias_file()
    return aliases.get(name, name)                 
