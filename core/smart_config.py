import json
import os

CONFIG_FILE = r"C:\Users\Dannyboi\Desktop\mclovin_Ai\core\smart_config.json"

def get_smart_mode_state():
    if not os.path.exists(CONFIG_FILE):
        return False
    with open(CONFIG_FILE, "r") as file:
        data = json.load(file)
        return data.get("smart_mode_active", False)

def set_smart_mode_state(state: bool):
    with open(CONFIG_FILE, "w") as file:
        json.dump({"smart_mode_active": state}, file)
