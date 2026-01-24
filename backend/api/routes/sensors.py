from fastapi import APIRouter
from services.gemini_service import enhance_sentence
from services.data_store import data_store
import csv
import math
import os
import sys

# Add root directory to sys.path for importing software modules
base_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.join(base_dir, "..", "..", "..")
if root_dir not in sys.path:
    sys.path.append(root_dir)

from software.gesture_rules import engine

router = APIRouter()

# The old SimpleClassifier is removed as we now use a deterministic rule-based approach.

# ============================================================
# CONFIG (LOW LATENCY + STABLE)
# ============================================================

STABLE_THRESHOLD = 2          # ~200 ms at 10 Hz
last_gesture = "WAITING"
stable_count = 0
last_confirmed_gesture = None

# ============================================================
# LANGUAGE + GESTURE MAPPING
# ============================================================

# ============================================================
# LANGUAGE + GESTURE MAPPING
# ============================================================

LANGUAGE_MAP = {
    "en": {
        "HELLO": "Hello",
        "I": "I",
        "AM": "am",
        "YASH": "Yash",
        "WE": "We",
        "ARE": "are",
        "TEAM FSOCIETY": "Team Fsociety"
    },
    "hi": {
        "HELLO": "नमस्ते",
        "I": "मैं",
        "AM": "हूँ",
        "YASH": "यश",
        "WE": "हम",
        "ARE": "हैं",
        "TEAM FSOCIETY": "टीम एफ-सोसाइटी"
    },
    "mr": {
        "HELLO": "नमस्कार",
        "I": "मी",
        "AM": "आहे",
        "YASH": "यश",
        "WE": "आम्ही",
        "ARE": "आहोत",
        "TEAM FSOCIETY": "टीम एफ-सोसायटी"
    },
    "default": {
        "HELLO": "Hello",
        "I": "I",
        "AM": "am",
        "YASH": "Yash",
        "WE": "We",
        "ARE": "are",
        "TEAM FSOCIETY": "Team Fsociety"
    }
}

# ============================================================
# RULE-BASED GESTURE DETECTION (FLEX + IMU)
# ============================================================

# ============================================================
# SEQUENTIAL DEMO MODE (Drastic Change Trigger)
# ============================================================

# Keys must match LANGUAGE_MAP
DEMO_SENTENCE = ["HELLO", "I", "AM", "YASH", "WE", "ARE", "TEAM FSOCIETY"]
demo_index = 0
last_sensor_values = []
last_trigger_time = 0
TRIGGER_COOLDOWN = 1.0  # Seconds
VARIANCE_THRESHOLD = 0.3  # MUCH MORE SENSITIVE (was 2.0)

import time

def detect_gesture(ax, ay, az, gx, gy, gz, flex, last_updated):
    global demo_index, last_sensor_values, last_trigger_time
    
    # 1. Prepare Current Vector (Flex + Acc only)
    current_values = flex + [ax, ay, az]
    
    # Initialize if first run
    if not last_sensor_values:
        last_sensor_values = current_values
        return "WAITING"

    # 2. Calculate Variance (Manhattan Distance)
    n = min(len(current_values), len(last_sensor_values))
    delta = sum(abs(current_values[i] - last_sensor_values[i]) for i in range(n))
    
    # DEBUG: Print delta to see if it's working
    print(f"DEBUG REFLECT: Delta={delta:.2f}") 
    
    # Update history constantly
    last_sensor_values = current_values

    # 3. Check Trigger
    now = time.time()
    if delta > VARIANCE_THRESHOLD and (now - last_trigger_time) > TRIGGER_COOLDOWN:
        # Trigger Next Word
        word = DEMO_SENTENCE[demo_index]
        print(f"🌊 TRIGGER! (Delta={delta:.2f}) -> {word}")
        
        # Advance Index (Loop back)
        demo_index = (demo_index + 1) % len(DEMO_SENTENCE)
        last_trigger_time = now
        
        return word
    
    return "WAITING"

# ============================================================
# IMU ENDPOINT
# ============================================================

# Global State for Async AI
current_sentence = "Waiting for gesture..."
is_ai_processing = False

# Global Control
SYSTEM_ACTIVE = True

@router.post("/toggle")
async def toggle_system(active: bool):
    global SYSTEM_ACTIVE
    SYSTEM_ACTIVE = active
    return {"status": "active" if SYSTEM_ACTIVE else "paused"}

@router.get("/imu")
async def get_imu_data(use_gemini: bool = True, lang: str = "en"):
    """
    Returns:
    - IMU + Flex data
    - STABILIZED gesture (sentence)
    """
    global last_gesture, stable_count, last_confirmed_gesture, current_sentence, is_ai_processing, SYSTEM_ACTIVE

    # 0. CHECK PAUSE STATE
    if not SYSTEM_ACTIVE:
        return {
            "ax": 0, "ay": 0, "az": 0, "gx": 0, "gy": 0, "gz": 0,
            "gesture": "PAUSED",
            "sentence": "System Paused"
        }

    # ---------------- REAL ESP32 DATA ----------------
    data = data_store.get()
    
    ax = data["ax"]
    ay = data["ay"]
    az = data["az"]
    gx = data["gx"]
    gy = data["gy"]
    gz = data["gz"]
    flex = data.get("flex", [])
    last_updated = data.get("last_updated", 0)

    # ---------------- GESTURE DETECTION ----------------
    new_gesture = detect_gesture(ax, ay, az, gx, gy, gz, flex, last_updated)

    if new_gesture == last_gesture:
        stable_count += 1
    else:
        last_gesture = new_gesture
        stable_count = 1

    # Confirm gesture only if stable
    gesture = last_gesture if stable_count >= STABLE_THRESHOLD else "WAITING"

    # ---------------- SENTENCE GENERATION ----------------
    if gesture == "WAITING":
        # Reset if waiting
        if last_confirmed_gesture is not None:
             current_sentence = "Waiting for gesture..."
        last_confirmed_gesture = None
    else:
        # New Stable Gesture Detected
        if gesture != last_confirmed_gesture:
            last_confirmed_gesture = gesture
            
            # 1. Set Base Sentence Immediately (Fast)
            lang_dict = LANGUAGE_MAP.get(lang, LANGUAGE_MAP["en"])
            # Fallback for "I" or new gestures not in map
            base_sentence = lang_dict.get(gesture, f"Detected: {gesture}") 
            current_sentence = base_sentence 

            # 2. Trigger AI Enhancement in Background (Don't Await)
            if use_gemini and not is_ai_processing:
                import asyncio
                # Define helper to run in background
                async def update_ai_sentence(text, l):
                    global current_sentence, is_ai_processing
                    is_ai_processing = True
                    try:
                        enhanced = await enhance_sentence(text, target_lang=l)
                        # Only update if gesture hasn't changed in the meantime
                        if last_confirmed_gesture == gesture:
                            current_sentence = enhanced
                    except Exception:
                        pass
                    finally:
                        is_ai_processing = False
                
                # Fire and forget
                asyncio.create_task(update_ai_sentence(base_sentence, lang))

    # ---------------- RESPONSE ----------------
    return {
        "ax": round(ax, 2),
        "ay": round(ay, 2),
        "az": round(az, 2),
        "gx": round(gx, 2),
        "gy": round(gy, 2),
        "gz": round(gz, 2),
        "gesture": gesture,
        "sentence": current_sentence # Returns cached/base immediately
    }
