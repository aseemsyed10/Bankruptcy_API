# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, f1_score, log_loss
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import uvicorn
import numpy as np
import joblib

# Load dataset
df = pd.read_csv(r"C:\Users\Kratos\Downloads\data.csv")
df.columns = df.columns.str.strip()

# Prepare features and target
X = df.drop(columns=["Bankrupt?"])
y = df["Bankrupt?"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Standardize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train logistic regression model
model = LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42)
model.fit(X_train_scaled, y_train)

# Save model and scaler
joblib.dump(model, "model.joblib")
joblib.dump(scaler, "scaler.joblib")

# Predictions for evaluation
y_pred = model.predict(X_test_scaled)
y_proba = model.predict_proba(X_test_scaled)[:, 1]

# Evaluation
f1 = f1_score(y_test, y_pred)
logloss = log_loss(y_test, y_proba)
report = classification_report(y_test, y_pred)

print("F1 Score:", f1)
print("Log Loss:", logloss)
print("Classification Report:\n", report)

# --- FastAPI Part ---
class InputData(BaseModel):
    features: List[float]

class Prediction(BaseModel):
    probability: float
    prediction: int

app = FastAPI()

model = joblib.load("model.joblib")
scaler = joblib.load("scaler.joblib")

@app.post("/predict", response_model=Prediction)
def predict(data: InputData):
    X_input = np.array(data.features).reshape(1, -1)
    X_scaled = scaler.transform(X_input)
    probability = model.predict_proba(X_scaled)[0][1]
    prediction = model.predict(X_scaled)[0]
    return Prediction(probability=round(probability, 4), prediction=int(prediction))

# Uncomment to run the API directly (optional)
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

@app.post("/explain")
def explain(data: InputData):
    try:
        # Prepare input
        X = np.array(data.features).reshape(1, -1)
        X_scaled = scaler.transform(X)

        # Compute SHAP values
        shap_values = explainer(X_scaled)
        shap_list = shap_values.values[0].tolist()
        feature_names = [f"Feature {i+1}" for i in range(len(shap_list))]
        feature_values = X[0].tolist()

        return {
            "shap_values": shap_list,
            "feature_names": feature_names,
            "feature_values": feature_values
        }

    except Exception as e:
        return {"error": str(e)}

