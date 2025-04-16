from core.llm_model import model

def generate_response(command):
    # prompt to make responses natural
    prompt = f"You are a helpful AI assistant. Keep responses concise and natural.\nUser: {command}\nAI:"

    print("McLovin Not Thinking...")
    response = model.generate(
        prompt=prompt,
        max_tokens=100,
        temp=0.7,
        top_p=0.9,
        repeat_penalty=1.2  # Helps prevent repetition
    )
    return response.strip().split("\n")[0]

