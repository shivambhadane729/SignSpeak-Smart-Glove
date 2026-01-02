import pandas as pd
import numpy as np
import os
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.preprocessing import LabelEncoder

# ---------------- SETTINGS ----------------
DATASET_PATH = os.path.join(os.path.dirname(__file__), "..", "dataset")  # ml/dataset/
MODEL_NAME = os.path.join(os.path.dirname(__file__), "..", "models", "gesture_model.pkl")
TEST_SIZE = 0.2
RANDOM_STATE = 42
# ------------------------------------------

# Suppress sklearn warnings for single-class case
warnings.filterwarnings("ignore")

print("📂 Loading dataset...")

# Load only dynamic gesture CSV files
dataframes = []
for file in os.listdir(DATASET_PATH):
    if file.endswith("_dynamic.csv"):
        print(f"  ➜ Loading {file}")
        df = pd.read_csv(os.path.join(DATASET_PATH, file))
        dataframes.append(df)

# Safety check
if len(dataframes) == 0:
    raise FileNotFoundError("❌ No *_dynamic.csv files found in folder!")

# Combine all CSVs
data = pd.concat(dataframes, ignore_index=True)

# Validate dataset
if "label" not in data.columns:
    raise ValueError("❌ 'label' column not found in CSV files!")

print(f"\n✅ Total samples: {len(data)}")
print(f"🖐️ Gestures: {data['label'].unique()}")

# ---------------- DATA PREP ----------------
X = data.drop("label", axis=1)
y = data["label"]

# Encode labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=TEST_SIZE,
    random_state=RANDOM_STATE,
    stratify=y_encoded
)

print("\n🧠 Training Random Forest model...")

# ---------------- MODEL ----------------
model = RandomForestClassifier(
    n_estimators=150,
    max_depth=20,
    random_state=RANDOM_STATE,
    n_jobs=-1
)

model.fit(X_train, y_train)

# ---------------- EVALUATION ----------------
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"\n🎯 Model Accuracy: {accuracy * 100:.2f}%\n")

# Classification report only if >1 class
if len(label_encoder.classes_) > 1:
    print("📊 Classification Report:")
    print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))
else:
    print("📊 Single gesture detected — classification report skipped.")

# ---------------- CONFUSION MATRIX ----------------
if len(label_encoder.classes_) > 1:
    cm = confusion_matrix(y_test, y_pred)

    plt.figure(figsize=(8, 6))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=label_encoder.classes_,
        yticklabels=label_encoder.classes_
    )
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix")
    plt.tight_layout()

    # Non-blocking plot
    plt.show(block=False)
    plt.pause(3)
    plt.close()
else:
    print("⚠️ Confusion matrix skipped (only one class).")

# ---------------- SAVE MODEL ----------------
joblib.dump(model, MODEL_NAME)
encoder_path = os.path.join(os.path.dirname(__file__), "..", "models", "label_encoder.pkl")
joblib.dump(label_encoder, encoder_path)

print(f"\n💾 Model saved as '{MODEL_NAME}'")
print(f"💾 Label encoder saved as '{encoder_path}'")
