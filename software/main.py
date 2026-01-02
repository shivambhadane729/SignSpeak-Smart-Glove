"""
SignSpeak - Main Application
Real-time sign language to speech translation pipeline
"""

import serial
import time
import os
import sys
from typing import Optional

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sys
import os

# Add software directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gesture_classifier import GestureClassifier
from gemini_language_engine import GeminiLanguageEngine
from text_to_speech import TextToSpeech

# Import configuration
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config.config import (
    SERIAL_PORT, BAUD_RATE, WINDOW_SIZE, CONFIDENCE_THRESHOLD,
    COOLDOWN_SECONDS, USE_GEMINI, USE_TTS
)

class SignSpeakPipeline:
    """Main pipeline for sign language to speech translation"""
    
    def __init__(self, serial_port: str = SERIAL_PORT, use_gemini: bool = USE_GEMINI):
        """
        Initialize SignSpeak pipeline
        
        Args:
            serial_port: Serial port for ESP32 communication
            use_gemini: Whether to use Gemini for contextual sentences
        """
        self.serial_port = serial_port
        self.use_gemini = use_gemini
        
        # Initialize components
        print("🔧 Initializing SignSpeak pipeline...")
        
        # Gesture classifier
        print("📦 Loading gesture classifier...")
        self.classifier = GestureClassifier()
        
        # Gemini language engine (optional)
        if use_gemini:
            try:
                print("🤖 Initializing Gemini language engine...")
                self.gemini = GeminiLanguageEngine()
                print("✅ Gemini initialized")
            except Exception as e:
                print(f"⚠️ Gemini initialization failed: {e}")
                print("💡 Continuing without contextual processing...")
                self.use_gemini = False
        else:
            self.gemini = None
        
        # Text-to-speech
        if USE_TTS:
            print("🔊 Initializing text-to-speech...")
            self.tts = TextToSpeech(use_offline=True)
            print("✅ TTS initialized")
        else:
            self.tts = None
        
        # State variables
        self.last_prediction = None
        self.last_spoken_time = 0
        self.data_buffer = []
        
        print("\n✅ SignSpeak pipeline ready!\n")
    
    def connect_serial(self):
        """Connect to ESP32 via serial"""
        try:
            self.ser = serial.Serial(self.serial_port, BAUD_RATE, timeout=1)
            time.sleep(2)  # Wait for connection
            print(f"📡 Connected to {self.serial_port}")
            
            # Flush initial junk data
            for _ in range(10):
                self.ser.readline()
            
            return True
        except Exception as e:
            print(f"❌ Failed to connect to {self.serial_port}: {e}")
            return False
    
    def process_gesture(self, gesture: str):
        """
        Process detected gesture through the pipeline
        
        Args:
            gesture: Raw gesture label
        """
        now = time.time()
        
        # Check cooldown and duplicate prevention
        if (now - self.last_spoken_time < COOLDOWN_SECONDS or 
            gesture == self.last_prediction):
            return
        
        print(f"👋 Detected Gesture: {gesture}")
        
        # Generate natural sentence
        if self.use_gemini and self.gemini:
            try:
                sentence = self.gemini.generate_sentence(gesture)
                print(f"💬 Generated: {sentence}")
            except Exception as e:
                print(f"⚠️ Gemini error: {e}. Using raw gesture.")
                sentence = gesture
        else:
            sentence = gesture
        
        # Convert to speech
        if self.tts:
            try:
                self.tts.speak(sentence)
            except Exception as e:
                print(f"⚠️ TTS error: {e}")
        
        # Update state
        self.last_prediction = gesture
        self.last_spoken_time = now
    
    def run(self):
        """Main application loop"""
        if not self.connect_serial():
            return
        
        print("🧤 SignSpeak active! Start signing...\n")
        
        try:
            window = []
            
            while True:
                # Read serial data
                line = self.ser.readline().decode("utf-8", errors="ignore").strip()
                
                if not line or "," not in line:
                    continue
                
                # Parse sensor data (11 values: 5 flex + 3 accel + 3 gyro)
                values = line.split(",")
                if len(values) != 11:
                    continue
                
                try:
                    sensor_data = [float(v) for v in values]
                    window.append(sensor_data)
                except ValueError:
                    continue
                
                # When window is full, predict gesture
                if len(window) >= WINDOW_SIZE:
                    try:
                        gesture, confidence = self.classifier.predict_with_confidence(window)
                        
                        if confidence >= CONFIDENCE_THRESHOLD:
                            self.process_gesture(gesture)
                        
                        # Reset window for next gesture
                        window = []
                        
                    except Exception as e:
                        print(f"⚠️ Prediction error: {e}")
                        window = []
        
        except KeyboardInterrupt:
            print("\n\n🛑 SignSpeak stopped by user")
        except Exception as e:
            print(f"\n❌ Error: {e}")
        finally:
            if hasattr(self, 'ser'):
                self.ser.close()
            print("👋 Goodbye!")

def main():
    """Entry point"""
    print("=" * 50)
    print("  SignSpeak - Smart Glove Translation System")
    print("=" * 50)
    print()
    
    # Check for API key if using Gemini
    if USE_GEMINI and not os.getenv("GEMINI_API_KEY"):
        print("⚠️ Warning: GEMINI_API_KEY not set.")
        print("💡 Set it as environment variable or edit software/main.py")
        print("   Continuing without contextual processing...\n")
    
    # Initialize and run pipeline
    pipeline = SignSpeakPipeline(use_gemini=USE_GEMINI)
    pipeline.run()

if __name__ == "__main__":
    main()

