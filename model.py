import pickle
import pandas as pd
from career_resources import CAREER_RESOURCES

# Load trained model
with open("model.pkl", "rb") as f:
    data = pickle.load(f)

model = data["model"]
encoders = data["encoders"]
feature_cols = data["features"]

def predict_career(input_data):
    df = pd.DataFrame([input_data])

    # Convert Yes/No → 1/0
    for col in ["Python", "SQL", "Java", "Azure", "ML"]:
        df[col] = df[col].map({"Yes": 1, "No": 0})

    # Encode categorical values
    df["Education"] = encoders["Education"].transform(df["Education"])
    df["Interest"] = encoders["Interest"].transform(df["Interest"])

    # Predict career
    pred = model.predict(df[feature_cols])[0]
    career = encoders["Career"].inverse_transform([pred])[0]

    # Get description & links
    resource = CAREER_RESOURCES.get(career, {})
    description = resource.get("description", "No description available")
    links = resource.get("links", [])

    return career, description, links
