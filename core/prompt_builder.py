from core.memory_manager import CONTEXT_LIMIT
from core.personality import PERSONALITIES

def build_prompt(memory, current_user_input):
    personality = memory.get("personality", "default")
    personality_instruction = PERSONALITIES.get(personality.lower(), PERSONALITIES["default"])
    summaries = "\n".join(memory.get("summaries", [])[-2:])
    context = memory.get("context", [])[-CONTEXT_LIMIT:]
    long_term = memory.get("long_term", {})

    # Build relevant long-term memory facts string for this turn
    long_term_facts = ""
    if long_term.get("name"):
        long_term_facts += f"The user's name is {long_term['name']}. You can refer to them by this name.\n"
    if long_term.get("nickname"):
        long_term_facts += f"You can call the user {long_term['nickname']} in conversation.\n"

    # Include preferences and mood only if they seem relevant to the current input
    if long_term.get("preferences") and any(pref.lower() in current_user_input.lower() for pref in long_term["preferences"].split(", ")):
        long_term_facts += f"The user enjoys {long_term['preferences']}.\n"
    elif long_term.get("preferences") and ("you like" in current_user_input.lower() or "you enjoy" in current_user_input.lower()):
        long_term_facts += f"The user enjoys {long_term['preferences']}.\n" # If the user is asking about preferences

    if long_term.get("mood"):
        long_term_facts += f"The user is currently in a {long_term['mood']} mood. Take this into account in your response.\n"

    prompt = f"""You are acting as a person with the following personality: {personality_instruction}

Your goal is to respond to the user in a way that is consistent with this personality, sounds natural and human-like, directly addresses their current statement, and provides a complete thought. Avoid unnecessary meta-commentary about your abilities.

Here are some things you know about the user:
{long_term_facts.strip()}

Here's a summary of recent parts of the conversation:
{summaries.strip()}

Here is the recent conversation history:
"""
    for pair in context:
        prompt += f"User: {pair['user']}\nAI: {pair['assistant']}\n"

    prompt += f"User: {current_user_input}\nAI: "

    return prompt.strip()
