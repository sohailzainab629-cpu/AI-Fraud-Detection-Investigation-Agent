
import pandas as pd
import joblib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(
    BASE_DIR, "dataset", "engineered_creditcard.csv"
)

MODEL_PATH = os.path.join(
    BASE_DIR, "models", "fraud_model.pkl"
)

# Load dataset and trained model
df = pd.read_csv(DATA_PATH)
model_bundle = joblib.load(MODEL_PATH)

model = model_bundle["model"]
feature_columns = model_bundle["feature_columns"]

# Select first 10 actual fraud transactions
fraud_samples = df[df["Class"] == 1].head(10).copy()

# Prepare features
X = fraud_samples[feature_columns]

# Predict fraud probabilities
fraud_samples["Predicted"] = model.predict(X)
fraud_samples["Fraud_Probability"] = model.predict_proba(X)[:, 1]

# Display results
print("\n========== HIGH RISK SAMPLE CHECK ==========\n")

print(
    fraud_samples[
        ["Time", "Amount", "Predicted", "Fraud_Probability"]
    ].to_string(index=False)
)

print("\n========== HIGHEST RISK TRANSACTION ==========\n")

highest = fraud_samples.loc[
    fraud_samples["Fraud_Probability"].idxmax()
]

print("Time:", highest["Time"])
print("Amount:", highest["Amount"])
print("Prediction:", highest["Predicted"])
print("Fraud Probability:", highest["Fraud_Probability"])
