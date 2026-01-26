import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os

# --- 1. SETTINGS ---
FILENAME = 'training_data.csv'
MODEL_NAME = 'signspeak.pkl'
# 4 flex sensors + 3 accelerometer axes = 7 feature columns
COLUMNS = ['f1', 'f2', 'f3', 'f4', 'ax', 'ay', 'az', 'label']

print("--- Starting Training Process ---")

# --- 2. CHECK IF FILE EXISTS ---
if not os.path.exists(FILENAME):
    print(f"CRITICAL ERROR: The file '{FILENAME}' was not found in this folder!")
    print("Files currently in this folder:", os.listdir())
    exit()

# --- 3. LOAD DATA ---
try:
    print(f"Loading {FILENAME}...")
    # Use header=None if your CSV doesn't have names at the top
    df = pd.read_csv(FILENAME, header=None, names=COLUMNS)
    
    # Remove any empty or corrupt rows
    df = df.dropna()
    
    print(f"Successfully loaded {len(df)} rows of data.")
    print(f"Labels found: {df['label'].unique()}")
    
    # --- 4. PREPARE AI ---
    X = df.drop('label', axis=1) # Features
    y = df['label']              # Target (The word)

    # Split into 80% training and 20% testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # --- 5. TRAIN ---
    print("Training the Random Forest model... (Please wait)")
    model = RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42)
    model.fit(X_train, y_train)

    # --- 6. TEST & SAVE ---
    accuracy = model.score(X_test, y_test)
    print(f"Training Complete! Accuracy: {accuracy * 100:.2f}%")
    
    joblib.dump(model, MODEL_NAME)
    print(f"Brain saved successfully as '{MODEL_NAME}'")
    print("You can now run your detect.py script.")

except Exception as e:
    print(f"AN ERROR OCCURRED DURING TRAINING: {e}")

print("--- Script Finished ---")