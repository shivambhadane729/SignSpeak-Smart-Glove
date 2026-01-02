"""
SignSpeak - Text-to-Speech Handler
Converts text sentences into audible speech using Google TTS
"""

import os
from gtts import gTTS
import pyttsx3
from typing import Optional

class TextToSpeech:
    """Text-to-speech conversion using multiple backends"""
    
    def __init__(self, use_offline: bool = True):
        """
        Initialize TTS handler
        
        Args:
            use_offline: If True, use pyttsx3 (offline). If False, use gTTS (requires internet)
        """
        self.use_offline = use_offline
        
        if use_offline:
            # Initialize offline TTS engine (pyttsx3)
            try:
                self.engine = pyttsx3.init('sapi5')  # Windows
                voices = self.engine.getProperty('voices')
                if voices:
                    self.engine.setProperty('voice', voices[0].id)
                self.engine.setProperty('rate', 160)
                self.engine.setProperty('volume', 1.0)
                print("✅ Offline TTS engine initialized")
            except Exception as e:
                print(f"⚠️ Offline TTS failed: {e}. Falling back to online TTS.")
                self.use_offline = False
        
        if not use_offline:
            print("✅ Using online TTS (gTTS)")
    
    def speak(self, text: str, lang: str = 'en'):
        """
        Convert text to speech and play it
        
        Args:
            text: Text to speak
            lang: Language code (default: 'en')
        """
        if not text or not text.strip():
            return
        
        try:
            if self.use_offline:
                self._speak_offline(text)
            else:
                self._speak_online(text, lang)
        except Exception as e:
            print(f"⚠️ TTS error: {e}")
    
    def _speak_offline(self, text: str):
        """Speak using offline pyttsx3 engine"""
        self.engine.say(text)
        self.engine.runAndWait()
    
    def _speak_online(self, text: str, lang: str = 'en'):
        """Speak using online gTTS"""
        try:
            tts = gTTS(text=text, lang=lang, slow=False)
            
            # Save to temporary file
            temp_file = "temp_speech.mp3"
            tts.save(temp_file)
            
            # Play audio (requires playsound or similar)
            try:
                from playsound import playsound
                playsound(temp_file)
            except ImportError:
                # Fallback: use system command
                import platform
                if platform.system() == 'Windows':
                    os.system(f'start {temp_file}')
                elif platform.system() == 'Darwin':
                    os.system(f'afplay {temp_file}')
                else:
                    os.system(f'mpg123 {temp_file}')
            
            # Clean up
            if os.path.exists(temp_file):
                os.remove(temp_file)
                
        except Exception as e:
            print(f"⚠️ Online TTS failed: {e}. Falling back to offline.")
            self.use_offline = True
            self._speak_offline(text)

