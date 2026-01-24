
import asyncio
import edge_tts
import os
import sys

# Add parent directory to path to import backend modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend"))

from backend.services.gemini_service import enhance_sentence

INPUT_SENTENCE = "Hello, I am Yash. This is are team Fsociety."

LANGUAGES = {
    "English":   {"code": "en", "voice": "en-US-ChristopherNeural"},
    "Hindi":     {"code": "hi", "voice": "hi-IN-MadhurNeural"},
    "Marathi":   {"code": "mr", "voice": "mr-IN-ManoharNeural"},
    "Bengali":   {"code": "bn", "voice": "bn-IN-BashkarNeural"},
    "Gujarati":  {"code": "gu", "voice": "gu-IN-NiranjanNeural"},
    "Tamil":     {"code": "ta", "voice": "ta-IN-ValluvarNeural"},
    "Telugu":    {"code": "te", "voice": "te-IN-MohanNeural"},
    "Kannada":   {"code": "kn", "voice": "kn-IN-GaganNeural"},
    "Malayalam": {"code": "ml", "voice": "ml-IN-MidhunNeural"}
}

async def run_pipeline():
    print(f"🚀 STARTING TRANSLATION + TTS PIPELINE")
    print(f"📖 Input: '{INPUT_SENTENCE}'")
    print("========================================")
    
    if not os.path.exists("test_pipeline_audio"):
        os.makedirs("test_pipeline_audio")

    for lang_name, data in LANGUAGES.items():
        lang_code = data["code"]
        voice = data["voice"]
        
        print(f"\n🌐 Processing {lang_name} ({lang_code})...")
        
        # 1. TRANSLATE via Gemini
        try:
            if lang_code == "en":
                translated_text = INPUT_SENTENCE
            else:
                translated_text = enhance_sentence(INPUT_SENTENCE, target_lang=lang_code)
            
            print(f"   📝 Translated: {translated_text}")
            
            # 2. GENERATE AUDIO via Edge-TTS
            filename = f"test_pipeline_audio/{lang_name.lower()}.mp3"
            communicate = edge_tts.Communicate(translated_text, voice)
            await communicate.save(filename)
            print(f"   ✅ Audio Saved: {filename}")
            
        except Exception as e:
            print(f"   ❌ Pipeline Failed: {e}")

    print("\n✨ PIPELINE COMPLETE! Check 'test_pipeline_audio' folder.")

if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    try:
        loop.run_until_complete(run_pipeline())
    finally:
        loop.close()
