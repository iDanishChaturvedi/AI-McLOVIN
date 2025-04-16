def check_for_smart_mode(text):
    triggers = {
        "activate smart mode": "activate",
        "deactivate smart mode": "deactivate",
        "reset smart memory": "reset"
    }
    for key, value in triggers.items():
        if key==text.lower():
            return value
    return None
