import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import pickle

print("Loading dataset...")

# Load CSV directly (already clean)
df = pd.read_csv("gesture_data.csv", header=None)

print("Dataset shape:", df.shape)
print(df.head())

# Split features & labels
X = df.iloc[:, :-1].astype(float).values
y = df.iloc[:, -1].values

# Encode labels
le = LabelEncoder()
y = le.fit_transform(y)

with open("label_encoder.pkl", "wb") as f:
    pickle.dump(le, f)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Training the Brain 🧠 ...")

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print(f"Accuracy: {acc * 100:.2f}%")

# Save model
with open("glove_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model saved as glove_model.pkl")
print("✅ Training complete")
