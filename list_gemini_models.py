
import google.generativeai as genai
import os
import sys

# Add parent directory to path to import backend modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend"))

from backend.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

print("Listing available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods and 'gemini' in m.name:
            print(f"- {m.name}")
    print("DONE")
except Exception as e:
    print(f"Error listing models: {e}")
