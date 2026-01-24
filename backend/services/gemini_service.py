import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def enhance_sentence(sentence: str, target_lang: str = "en") -> str:
    if not sentence:
        return sentence

    # Strict Mode: If target is English, return exactly what was sent (No AI changes)
    if target_lang == "en":
        return sentence

    prompt = f"""
    You are a strict translation AI for a smart glove system.
    
    Task:
    1. Translate the input sentence EXACTLY to the target language: {target_lang}.
    2. Do NOT add any intro, outro, explanations, or conversational filler.
    3. Keep proper names (like "Yash", "Shivam", "Fsociety") unchanged.
    4. Output ONLY the translated sentence.

    Input: "{sentence}"
    Target Language Code: {target_lang}
    """

    try:
        print(f"✨ Calling Gemini... Input: '{sentence}' -> Lang: {target_lang}")
        response = model.generate_content(prompt)
        text = response.text.strip().split("\n")[0] # Ensure single line
        # Cleanup quotes if Gemini adds them
        text = text.replace('"', '').replace("'", "")
        print(f"✨ Gemini output: {text}")
        return text
    except Exception as e:
        print(f"❌ Gemini Error: {e}")
        return sentence
