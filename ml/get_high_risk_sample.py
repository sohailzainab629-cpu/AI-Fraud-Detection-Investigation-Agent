
import pandas as pd
import joblib
import json

print("Loading dataset and trained model...")

# Load engineered dataset
df = pd.read_csv("dataset/engineered_creditcard.csv")

# Load trained model
bundle = joblib.load("models/fraud_model.pkl")

model = bundle["model"]
feature_columns = bundle["feature_columns"]

# Prepare features
X = df[feature_columns]

# Predict fraud probabilities
probabilities = model.predict_proba(X)[:, 1]
predictions = model.predict(X)

# Find actual high-risk fraud transactions
mask = (
    (df["Class"] == 1)
    & (predictions == 1)
    & (probabilities >= 0.80)
)

candidates = df.loc[mask].copy()

if candidates.empty:
    print("\nNo high-risk transaction found!")
else:
    candidates["Fraud_Probability"] = probabilities[mask]

    # Select highest probability transaction
    sample = candidates.sort_values(
        "Fraud_Probability",
        ascending=False
    ).iloc[0]

    # Required API features
    required_features = (
        ["Time"]
        + [f"V{i}" for i in range(1, 29)]
        + ["Amount"]
    )

    transaction = {
        feature: float(sample[feature])
        for feature in required_features
    }

    print("\n========== HIGH RISK TRANSACTION ==========")
    print(json.dumps({"transaction": transaction}, indent=2))

    print("\nFraud Probability:",
          round(float(sample["Fraud_Probability"]), 4))

    print("\nSample generated successfully!")
