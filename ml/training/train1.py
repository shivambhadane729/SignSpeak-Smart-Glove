import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# =====================================================
# DATASET PATHS
# =====================================================
HELLO_CSV_PATH = r"C:\Users\shiva\OneDrive - Vishwakarma Institute of Technology\Desktop\Project_fsociety\ml\dataset\hello\hello.csv"
THANKYOU_CSV_PATH = r"C:\Users\shiva\OneDrive - Vishwakarma Institute of Technology\Desktop\Project_fsociety\ml\dataset\thankyou\thankyou.csv"
IDLE_CSV_PATH = r"C:\Users\shiva\OneDrive - Vishwakarma Institute of Technology\Desktop\Project_fsociety\ml\dataset\idle\idle.csv"

MODEL_SAVE_PATH = "gesture_model.pkl"   # saved in current directory

FRAMES_PER_GESTURE = 50
FEATURE_COLUMNS = ["ax", "ay", "az", "gx", "gy", "gz"]

# =====================================================
# LOAD DATA
# =====================================================
hello_df = pd.read_csv(HELLO_CSV_PATH)
thank_df = pd.read_csv(THANKYOU_CSV_PATH)
idle_df  = pd.read_csv(IDLE_CSV_PATH)

hello_df["label_id"] = 0       # HELLO
thank_df["label_id"] = 1       # THANK_YOU
idle_df["label_id"]  = 2       # IDLE

# =====================================================
# MAKE gesture_id GLOBALLY UNIQUE
# =====================================================
offset = 0
hello_df["gesture_id"] += offset
offset = hello_df["gesture_id"].max() + 1

thank_df["gesture_id"] += offset
offset = thank_df["gesture_id"].max() + 1

idle_df["gesture_id"] += offset

df = pd.concat([hello_df, thank_df, idle_df], ignore_index=True)

print("✅ Data loaded")
print("Total rows:", len(df))

# =====================================================
# BUILD FEATURES
# =====================================================
X, y = [], []

for gid in df["gesture_id"].unique():
    g = df[df["gesture_id"] == gid]

    if len(g) < FRAMES_PER_GESTURE:
        continue

    g = g.iloc[:FRAMES_PER_GESTURE]
    X.append(g[FEATURE_COLUMNS].values.flatten())
    y.append(g["label_id"].iloc[0])

X = np.array(X)
y = np.array(y)

print("X shape:", X.shape)
print("y shape:", y.shape)

print("HELLO:", np.sum(y == 0))
print("THANK_YOU:", np.sum(y == 1))
print("IDLE:", np.sum(y == 2))

# =====================================================
# TRAIN / TEST SPLIT
# =====================================================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

# =====================================================
# TRAIN MODEL
# =====================================================
model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# =====================================================
# EVALUATION
# =====================================================
y_pred = model.predict(X_test)

print("\n🎯 Accuracy:", accuracy_score(y_test, y_pred))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nReport:")
print(classification_report(
    y_test,
    y_pred,
    target_names=["HELLO", "THANK_YOU", "IDLE"]
))

# =====================================================
# SAVE MODEL (🔥 THIS IS THE IMPORTANT PART)
# =====================================================
joblib.dump(model, MODEL_SAVE_PATH)
print(f"\n✅ Model saved successfully as: {MODEL_SAVE_PATH}")
