from fastapi import APIRouter
from services.gemini_service import enhance_sentence
from services.data_store import data_store

router = APIRouter()

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

LANGUAGE_MAP = {
    "en": {
        "HELLO": "Hello, I am Yash, this is my team, and today we are demonstrating our SignSpeak project.",
        "YES": "This is Shivam.",
        "NO": "And we are Team Fsociety.",
        "STOP": "Thank you!"
    },
    "hi": {
        "HELLO": "नमस्ते, मैं यश हूँ।",
        "YES": "यह शिवम है।",
        "NO": "और हम टीम एफ-सोसाइटी हैं।",
        "STOP": "धन्यवाद!"
    },
    "mr": {
        "HELLO": "नमस्कार, मी यश आहे.",
        "YES": "हा शिवम आहे.",
        "NO": "आणि आम्ही टीम एफ-सोसायटी आहोत.",
        "STOP": "धन्यवाद!"
    },
    # Fallbacks for others (Gemini will handle specific translation better)
    "default": {
        "HELLO": "Hello, I am Yash.",
        "YES": "This is Shivam.",
        "NO": "And we are Team Fsociety.",
        "STOP": "Thank you!"
    }
}

# ============================================================
# RULE-BASED GESTURE DETECTION (NO ML)
# ============================================================

# ============================================================
# RULE-BASED GESTURE DETECTION (FLEX + IMU)
# ============================================================

import time

def detect_gesture(ax, ay, az, gx, gy, gz, flex, last_updated):
    # Debug: Print values to terminal to help calibration
    is_stale = (time.time() - last_updated) > 1.0
    status = "🔴 STALE/FROZEN" if is_stale else "🟢 LIVE"
    
    print(f"[{status}] Flex: {flex} (Raw)")
    
    # Debug Logic
    # CALIBRATED THRESHOLDS (Based on User Logs)
    # Flex 1: Open ~475, Bent ~430 -> Thresh 460
    # Flex 2: Open ~575, Bent ~530 -> Thresh 560
    # Flex 3: Dead (0) -> Ignore

    THRESH_MID = 460
    THRESH_RING = 560
    
    MIN_VALID = 50 

    f_mid = flex[0] if len(flex) > 0 else 0
    f_ring = flex[1] if len(flex) > 1 else 0
    f_pinky = flex[2] if len(flex) > 2 else 0

    print(f"    -> Mid(f0):{int(f_mid)} Ring(f1):{int(f_ring)} Pinky(f2):{int(f_pinky)}")
    
    is_mid_bent = f_mid > MIN_VALID and f_mid < THRESH_MID
    is_ring_bent = f_ring > MIN_VALID and f_ring < THRESH_RING

    if f_mid > MIN_VALID:
        print(f"    -> Mid Status: {'BENT' if is_mid_bent else 'OPEN'} (Val: {int(f_mid)} < {THRESH_MID}?)")
    if f_ring > MIN_VALID:
        print(f"    -> Ring Status: {'BENT' if is_ring_bent else 'OPEN'} (Val: {int(f_ring)} < {THRESH_RING}?)")

    # 1. FLEX SENSOR GESTURES (Priority)
    if is_mid_bent and not is_ring_bent: 
        return "HELLO"
    if is_ring_bent and not is_mid_bent:
        return "YES"
    if is_mid_bent and is_ring_bent: # Both bent
        return "NO"

    # 2. IMU GESTURES (Backup)
    # Tilt Up/Down (Ay)
    if ay > 0.6:
        return "HELLO"
    
    # Tilt Left/Right (Ax)
    if abs(ax) > 0.6:
        return "YES"

    # Shake (High Gyro)
    if abs(gx) > 150 or abs(gy) > 150 or abs(gz) > 150:
        return "NO"

    return "WAITING"

# ============================================================
# IMU ENDPOINT
# ============================================================

@router.get("/imu")
def get_imu_data(use_gemini: bool = True, lang: str = "en"):
    """
    Returns:
    - IMU + Flex data
    - STABILIZED gesture (sentence)
    """

    global last_gesture, stable_count, last_confirmed_gesture

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
    if gesture != "WAITING":
        # Get language-specific base sentence, fallback to English/Default
        lang_dict = LANGUAGE_MAP.get(lang, LANGUAGE_MAP["en"])
        base_sentence = lang_dict.get(gesture, LANGUAGE_MAP["en"][gesture])

        sentence = base_sentence

        # Gemini enhances ONLY once per confirmed gesture
        if use_gemini and gesture != last_confirmed_gesture:
            sentence = enhance_sentence(base_sentence, target_lang=lang)
            last_confirmed_gesture = gesture
    else:
        sentence = "Waiting for gesture..."
        last_confirmed_gesture = None

    # ---------------- RESPONSE ----------------
    return {
        "ax": round(ax, 2),
        "ay": round(ay, 2),
        "az": round(az, 2),
        "gx": round(gx, 2),
        "gy": round(gy, 2),
        "gz": round(gz, 2),
        "gesture": gesture,
        "sentence": sentence
    }
