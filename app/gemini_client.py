import google.generativeai as genai
from app.config import settings

genai.configure(api_key=settings.gemini_api_key)

chat_history = [] 

def get_model():
    return genai.GenerativeModel(settings.gemini_model)

def add_to_history(role: str, text: str):
    chat_history.append((role, text))
    if len(chat_history) > 200:
        chat_history.pop(0)

def build_conversation(system_prompt: str, new_user_text: str):
    contents = []
    contents.append({"role": "user", "parts": [{"text": system_prompt}]})
    for role, text in chat_history:
        contents.append({"role": role, "parts": [{"text": text}]})
    contents.append({"role": "user", "parts": [{"text": new_user_text}]})
    return contents

def generate_json(system_prompt: str, user_text: str):
    model = get_model()
    # geçmişi ekliyoruz
    contents = build_conversation(system_prompt, user_text)
    resp = model.generate_content(contents)
    
    # cevap hafızaya kaydediliyor
    add_to_history("user", user_text)
    add_to_history("model", resp.text)

    return resp.text

def clear_history():
    chat_history.clear()
