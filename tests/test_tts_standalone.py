import asyncio
import edge_tts
import os

# Full List of Supported Languages for SignSpeak
TEST_CASES = {
    "English":  {"code": "en", "voice": "en-US-ChristopherNeural", "text": "Hello, testing the SignSpeak smart glove system."},
    "Hindi":    {"code": "hi", "voice": "hi-IN-MadhurNeural",      "text": "नमस्ते, यह साइनस्पीक स्मार्ट ग्लव सिस्टम का परीक्षण है।"},
    "Marathi":  {"code": "mr", "voice": "mr-IN-ManoharNeural",     "text": "नमस्कार, ही साइनस्पीक स्मार्ट ग्लोव्ह सिस्टमची चाचणी आहे."},
    "Bengali":  {"code": "bn", "voice": "bn-IN-BashkarNeural",     "text": "হ্যালো, এটি সাইনসপিক স্মার্ট গ্লাভ সিস্টেমের একটি পরীক্ষা।"},
    "Gujarati": {"code": "gu", "voice": "gu-IN-NiranjanNeural",    "text": "નમસ્તે, આ સાઈનસ્પીક સ્માર્ટ ગ્લોવ સિસ્ટમનું પરીક્ષણ છે."},
    "Tamil":    {"code": "ta", "voice": "ta-IN-ValluvarNeural",    "text": "வணக்கம், இது சைன்ஸ்பீக் ஸ்மார்ட் க்ளோவ் சிஸ்டத்தின் சோதனை."},
    "Telugu":   {"code": "te", "voice": "te-IN-MohanNeural",       "text": "నమస్కారం, ఇది సైన్‌స్పీక్ స్మార్ట్ గ్లోవ్ సిస్టమ్ యొక్క పరీక్ష."},
    "Kannada":  {"code": "kn", "voice": "kn-IN-GaganNeural",       "text": "ನಮಸ್ಕಾರ, ಇದು ಸೈನ್‌ಸ್ಪೀಕ್ ಸ್ಮಾರ್ಟ್ ಗ್ಲೋವ್ ಸಿಸ್ಟಂನ ಪರೀಕ್ಷೆಯಾಗಿದೆ."},
    "Malayalam":{"code": "ml", "voice": "ml-IN-MidhunNeural",      "text": "നമസ്കാരം, ഇത് സൈൻസ്പീക്ക് സ്മാർട്ട് ഗ്ലോവ് സിസ്റ്റത്തിന്റെ പരീക്ഷണമാണ്."},
    "Punjabi":  {"code": "pa", "voice": "pa-IN-OjasNeural",        "text": "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ, ਇਹ ਸਾਈਨਸਪੀਕ ਸਮਾਰਟ ਗਲੋਵ ਸਿਸਟਮ ਦਾ ਟੈਸਟ ਹੈ।"}
}

async def generate_complete_test():
    print("🌍 STARTING FULL INDIAN LANGUAGE TTS TEST")
    print("=========================================")
    
    if not os.path.exists("test_audio_full"):
        os.makedirs("test_audio_full")

    for lang, data in TEST_CASES.items():
        filename = f"test_audio_full/{lang.lower()}.mp3"
        print(f"🎙️ Generating {lang} ({data['voice']})...")
        
        try:
            communicate = edge_tts.Communicate(data['text'], data['voice'])
            await communicate.save(filename)
            print(f"   ✅ Success! Saved to {filename}")
        except Exception as e:
            print(f"   ❌ Failed: {e}")

    print("\n✨ ALL DONE! Please check the 'test_audio_full' folder.")

if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    try:
        loop.run_until_complete(generate_complete_test())
    finally:
        loop.close()
