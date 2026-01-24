"""
SignSpeak - Gesture Rules Module (FINAL INVERTED MAPPING)
Calibration: MAX=STRAIGHT (High), MIN=BENT (Low)
Logic: Raw -> Normalize(0-1) -> Word
"""

class FingerState:
    MIN = "MIN" # BENT (Curled)
    MAX = "MAX" # STRAIGHT (Open)
    MID = "MID" # Transition

class PalmOrientation:
    PALM_UP = "PALM_UP"
    PALM_DOWN = "PALM_DOWN"
    TILTED = "TILTED"

class GestureRules:
    def __init__(self):
        # 1. Calibration Ranges (User Provided)
        # MIN (Bent) -> MAX (Straight)
        self.CALIBRATION = [
            {"min": 0.29, "max": 0.45}, # F1 Index
            {"min": 0.01, "max": 1.00}, # F2 Middle
            {"min": 0.25, "max": 0.60}, # F3 Ring
            {"min": 0.15, "max": 1.00}  # F4 Pinky
        ]

        # 2. State Thresholds (Normalized 0.0-1.0)
        # 1.0 = MAX = STRAIGHT
        # 0.0 = MIN = BENT
        self.TH_STRAIGHT = 0.65 # > 65% = Straight
        self.TH_BENT     = 0.35 # < 35% = Bent
        
        # 3. Motiom
        self.MOTION_THRESHOLD = 0.15
        self.ACC_UP_LIMIT = 0.5
        self.ACC_DOWN_LIMIT = -0.5

    def normalize(self, val, idx):
        cal = self.CALIBRATION[idx]
        val = max(cal["min"], min(val, cal["max"]))
        return (val - cal["min"]) / (cal["max"] - cal["min"])

    def get_finger_state(self, norm_val):
        if norm_val >= self.TH_STRAIGHT:
            return FingerState.MAX  # STRAIGHT
        elif norm_val <= self.TH_BENT:
            return FingerState.MIN  # BENT
        else:
            return FingerState.MID

    def get_palm_orientation(self, az):
        if az > self.ACC_UP_LIMIT:
            return PalmOrientation.PALM_UP
        elif az < self.ACC_DOWN_LIMIT:
            return PalmOrientation.PALM_DOWN
        else:
            return PalmOrientation.TILTED

    def process_frame(self, flex_vals, acc_vals, gyr_vals):
        # 1. Motion Gate
        if sum(abs(x) for x in gyr_vals) >= self.MOTION_THRESHOLD:
            return None

        # 2. Map States
        states = []
        num_sensors = min(len(flex_vals), 4)
        for i in range(num_sensors):
            norm = self.normalize(flex_vals[i], i)
            states.append(self.get_finger_state(norm))
        while len(states) < 4: states.append(FingerState.MIN)
        
        f1, f2, f3, f4 = states
        palm = self.get_palm_orientation(acc_vals[2])

        # DEBUG: Print Normalized States
        print(f"NORM: F1={self.normalize(flex_vals[0],0):.2f} F2={self.normalize(flex_vals[1],1):.2f} F3={self.normalize(flex_vals[2],2):.2f} F4={self.normalize(flex_vals[3],3):.2f}")
        print(f"STATE: F1={f1} F2={f2} F3={f3} F4={f4} Palm={palm}")

        # 3. MAPPING RULES (DISABLED - DEBUG MODE)
        """
        # 1️⃣ HELLO: All Straight (MIN), Palm UP
        if (f1 == FingerState.MIN and f2 == FingerState.MIN and 
            f3 == FingerState.MIN and f4 == FingerState.MIN and 
            palm == PalmOrientation.PALM_UP):
            return "Hello"

        # 2️⃣ I: Index Straight (MIN), Others Bent (MAX), Palm DOWN
        if (f1 == FingerState.MIN and 
            f2 == FingerState.MAX and 
            f3 == FingerState.MAX and 
            f4 == FingerState.MAX and 
            palm != PalmOrientation.PALM_UP):
            return "I"

        # 3️⃣ YASH: Index+Mid Straight (MIN), Others Bent (MAX), Palm UP
        if (f1 == FingerState.MIN and f2 == FingerState.MIN and 
            f3 == FingerState.MAX and f4 == FingerState.MAX and 
            palm == PalmOrientation.PALM_UP):
            return "Yash"

        # 4️⃣ WE: I+M+R Straight (MIN), Pinky Bent (MAX), Palm UP
        if (f1 == FingerState.MIN and f2 == FingerState.MIN and 
            f3 == FingerState.MIN and f4 == FingerState.MAX and 
            palm == PalmOrientation.PALM_UP):
            return "We"

        # 5️⃣ TEAM FSOCIETY: All Bent (MAX), Palm ANY
        if (f1 == FingerState.MAX and f2 == FingerState.MAX and 
            f3 == FingerState.MAX and f4 == FingerState.MAX):
            return "Team Fsociety"
        """

        return None

# Singleton
engine = GestureRules()
