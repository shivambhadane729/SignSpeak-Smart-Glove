"""
SignSpeak - Configuration File
Centralized configuration for all components
"""

import os
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# ======================
# Hardware Configuration
# ======================
SERIAL_PORT = os.getenv("SERIAL_PORT", "COM10")  # Change to your port (COM3, COM4, /dev/ttyUSB0, etc.)
BAUD_RATE = 115200
BLUETOOTH_DEVICE_NAME = "SignSpeak_Glove"

# Sensor Configuration
NUM_FLEX_SENSORS = 5
FLEX_SENSOR_PINS = [32, 33, 34, 35, 39]  # ESP32 GPIO pins (ADC1 compatible)
MPU6050_I2C_ADDRESS = 0x68
SAMPLING_RATE_HZ = 20
SAMPLE_INTERVAL_MS = 50  # 1000 / SAMPLING_RATE_HZ

# ======================
# ML Configuration
# ======================
ML_MODELS_PATH = PROJECT_ROOT / "ml" / "models"
ML_DATASET_PATH = PROJECT_ROOT / "ml" / "dataset"
ML_TRAINING_PATH = PROJECT_ROOT / "ml" / "training"

MODEL_NAME = "gesture_model.pkl"
LABEL_ENCODER_NAME = "label_encoder.pkl"

# Training Configuration
WINDOW_SIZE = 20  # Frames per gesture (~1 second at 20Hz)
SAMPLES_PER_GESTURE = 120
TEST_SIZE = 0.2
RANDOM_STATE = 42

# Model Parameters
RANDOM_FOREST_ESTIMATORS = 150
RANDOM_FOREST_MAX_DEPTH = 20

# ======================
# Inference Configuration
# ======================
CONFIDENCE_THRESHOLD = 0.6
COOLDOWN_SECONDS = 0.5  # Prevent duplicate predictions
PREDICT_EVERY_N_FRAMES = 5
MOVEMENT_THRESHOLD = 3.0  # Ignore idle hand

# ======================
# AI/API Configuration
# ======================
# Google Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-pro"
USE_GEMINI = True  # Set to False to skip contextual processing

# Gemini Prompt Template
GEMINI_SYSTEM_PROMPT = """You are a helpful assistant that converts sign language gesture words into natural, polite, and contextually appropriate spoken sentences.

Rules:
1. Convert single gesture words (like "WATER", "HELLO", "THANK_YOU") into natural spoken sentences
2. Make sentences polite and conversational
3. Keep sentences concise (1-2 sentences max)
4. If the gesture is a greeting, respond with a greeting
5. If the gesture is a request, phrase it as a polite request
6. If the gesture is a statement, make it a natural statement

Examples:
- "WATER" → "Could I please have some water?"
- "HELLO" → "Hello, how are you?"
- "THANK_YOU" → "Thank you very much!"
- "YES" → "Yes, that's correct."
- "NO" → "No, thank you."

Now convert this gesture word into a natural sentence:"""

# ======================
# TTS Configuration
# ======================
USE_TTS = True
USE_OFFLINE_TTS = True  # Use pyttsx3 (offline) vs gTTS (online)
TTS_LANGUAGE = "en"
TTS_RATE = 160  # Speech rate (words per minute)
TTS_VOLUME = 1.0  # Volume (0.0 to 1.0)

# ======================
# Logging Configuration
# ======================
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_FILE = PROJECT_ROOT / "logs" / "signspeak.log"
ENABLE_CONSOLE_OUTPUT = True

# ======================
# Performance Configuration
# ======================
TARGET_LATENCY_MS = 500  # Target end-to-end latency
ENABLE_PERFORMANCE_MONITORING = True

# ======================
# Path Helpers
# ======================
def get_model_path(filename: str = MODEL_NAME) -> Path:
    """Get full path to model file"""
    return ML_MODELS_PATH / filename

def get_dataset_path(filename: str = "") -> Path:
    """Get full path to dataset file or directory"""
    if filename:
        return ML_DATASET_PATH / filename
    return ML_DATASET_PATH

def get_training_path(filename: str = "") -> Path:
    """Get full path to training script or directory"""
    if filename:
        return ML_TRAINING_PATH / filename
    return ML_TRAINING_PATH

