import pickle
import pandas as pd

# Load the trained model
with open("model.pkl", "rb") as f:
    data = pickle.load(f)

model = data["model"]
encoders = data["encoders"]
feature_cols = data["features"]

def predict_career(input_data):
    df = pd.DataFrame([input_data])
    
    # Convert binary fields to 0/1
    for col in ["Python", "SQL", "Java", "Azure", "ML"]:
        if col in df:
            df[col] = df[col].map({"Yes": 1, "No": 0})

    # Encode categorical fields
    df["Education"] = encoders["Education"].transform(df["Education"])
    df["Interest"] = encoders["Interest"].transform(df["Interest"])

    # Predict
    pred = model.predict(df[feature_cols])[0]
    return encoders["Career"].inverse_transform([pred])[0]