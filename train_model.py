import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load CSV
data = pd.read_csv("data/careers.csv")

# Convert Yes/No to 1/0
binary_cols = ["Python", "SQL", "Java", "Azure", "ML"]
for col in binary_cols:
    data[col] = data[col].map({"Yes": 1, "No": 0})

# Encode categorical columns
le_dict = {}
categorical_cols = ["Education", "Interest", "Career"]

for col in categorical_cols:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])
    le_dict[col] = le

# Features & Labels
feature_cols = ["Education", "Python", "SQL", "Java", "Azure", "ML", "Interest"]
X = data[feature_cols]
y = data["Career"]

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save model
with open("model.pkl", "wb") as f:
    pickle.dump({
        "model": model,
        "encoders": le_dict,
        "features": feature_cols
    }, f)

print("✅ Model trained and saved as model.pkl")
