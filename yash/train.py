import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# 1. Load the data
print("Loading training data...")
# We use names based on our ESP32 output: 4 flex sensors + 3 accel axes
cols = ['f1', 'f2', 'f3', 'f4', 'ax', 'ay', 'az', 'label']

try:
    df = pd.read_csv('training_data.csv', names=cols)
    
    # Remove any rows with missing or corrupt data
    df = df.dropna()

    # 2. Split Features (X) and Labels (y)
    X = df.drop('label', axis=1)
    y = df['label']

    # 3. Split into Training and Testing sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 4. Initialize and Train the Random Forest
    print("Training the model (this may take a few seconds)...")
    model = RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42)
    model.fit(X_train, y_train)

    # 5. Evaluate Accuracy
    predictions = model.predict(X_test)
    acc = accuracy_score(y_test, predictions)
    
    print("\n" + "="*30)
    print(f"TRAINING SUCCESSFUL!")
    print(f"Model Accuracy: {acc * 100:.2f}%")
    print("="*30)

    # 6. Save the model to a file
    joblib.dump(model, 'signspeak.pkl')
    print("\nModel saved as 'signspeak.pkl'. You are ready for the Detection step!")

except FileNotFoundError:
    print("ERROR: 'training_data.csv' not found. Did you run the collection script?")
except Exception as e:
    print(f"An error occurred: {e}")