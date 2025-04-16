from core.memory_manager import (load_memory, save_memory, reset_memory, summarize_memory, update_long_term)
from core.personality import switch_personality, PERSONALITIES
from core.prompt_builder import build_prompt
from core.smart_trigger import check_for_smart_mode
from core.smart_config import get_smart_mode_state, set_smart_mode_state
from core.llm_model import model
import re

def remove_emojis(text):
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE,
    )
    return emoji_pattern.sub(r"", text)

def process_smart_mode(text):
    trigger = check_for_smart_mode(text)
    memory = load_memory()

    if trigger == "activate":
        set_smart_mode_state(True)
        return "Smart Mode Activated"

    elif trigger == "deactivate":
        set_smart_mode_state(False)
        return "Smart Mode Deactivated"

    elif trigger == "reset":
        reset_memory()
        return "Memory reset complete"

    elif get_smart_mode_state():        
        lowered = text.lower()
        if lowered.startswith("my name is"):            #can add my partner's name
            name = text.split("my name is")[-1].strip().split()
            update_long_term(memory, "name", name)
            return f"Got it! I'll remember your name is {name}."
        elif lowered.startswith("partner name is"):            #can add my partner's name
            name = text.split("partner name is")[-1].strip().split()
            update_long_term(memory, "partner", name)
            return f"Got it! I'll call your partner as {name}."
        elif lowered.startswith("remember call me")or lowered.startswith("remember my nickname is"):
            nickname = text.split("call me")[-1].strip().split() if "call me" in lowered else text.split("nickname is")[-1].strip().split()[0]
            update_long_term(memory, "nickname", nickname)
            return f"Alright! I’ll call you {nickname} from now on."

        elif lowered.startswith("remember i like"):
            pref = text.split("i like")[-1].strip()
            update_long_term(memory, "preferences", pref)
            return f"Cool! I'll remember that you like {pref}."

        elif "what's my name" == lowered or "what is my name" == lowered:
            name = memory.get("long_term", {}).get("name")
            nickname = memory.get("long_term", {}).get("nickname")
            if nickname:
                return f"You told me to call you {nickname}."
            return f"Your name is {name}." if name else "I don't know your name yet. Tell me!"
        elif "i'm feeling" in lowered or "i am feeling" in lowered:
            mood = lowered.split("feeling")[-1].strip().split()[0]
            update_long_term(memory, "mood", mood)
            return f"I'll remember that you're feeling {mood}."

        elif lowered.startswith("set my mood to"):
            mood = lowered.split("set my mood to")[-1].strip().split()[0]
            update_long_term(memory, "mood", mood)
            return f"Mood set to {mood}."

        elif "delete last context" == lowered:
            if memory.get("context"):
                popped = memory["context"].pop()  # Remove last (user, assistant) pair
                save_memory(memory)
                return f"Removed last context: '{popped['user']}'"
            return "There's nothing to remove from memory."
        elif "what do i like" == lowered:
            prefs = memory.get("long_term", {}).get("preferences")
            return f"You said you like {prefs}." if prefs else "You haven't told me your preferences yet!"

        elif "add" in lowered and "to my preference" in lowered:
            new_pref = text.split("add")[-1].split("to my preference")[0].strip()
            current = memory.get("long_term", {}).get("preferences", "")
            updated = f"{current}, {new_pref}" if current else new_pref
            update_long_term(memory, "preferences", updated)
            return f"Added {new_pref} to your preferences."
        
        # Main smart response logic
        elif lowered.startswith("switch to") and lowered.endswith("mode"):
            mode = lowered.replace("switch to", "").strip()
            mode_words = mode.split() 
            if mode_words:
                return switch_personality(mode_words[0], memory) 
        # Build context-rich prompt
        try:
            prompt_text = build_prompt(memory, text.strip())
            #personality = memory.get("personality", "default").capitalize()
            #personality_instruction = PERSONALITIES.get(personality.lower(), PERSONALITIES["default"]) #personality check but confusing for offline llm models
            formatted_prompt = f"{prompt_text}"
            print("McLovin Thinking...")

                # Generate response
            response = model.generate(
                prompt=formatted_prompt,
                max_tokens=180,
                temp=0.6,
                top_p=0.9,
                repeat_penalty=1.2
            )
            reply = response.strip()
            reply = remove_emojis(reply)
            cleaned_lines = []
            for line in reply.splitlines():
                line = line.strip()
                if not line.lower().startswith(("user:", "assistant:", "system:", "*", "<", "[")):
                    cleaned_lines.append(line)
            reply = "\n".join(cleaned_lines).strip()
            return reply  # Ensure the processed reply is returned

    # Save context to memory
            memory["context"].append({"user": text.strip(), "assistant": reply})
            save_memory(summarize_memory(memory))
        except Exception as e:
            print(f"Smart mode generation error: {e}")
            return "I encountered an issue processing that. Could you try again?"
    
