
import pandas as pd
import numpy as np
import joblib
import os

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

# Project paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "dataset", "engineered_creditcard.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "fraud_model.pkl")
REPORT_DIR = os.path.join(BASE_DIR, "reports")

os.makedirs(REPORT_DIR, exist_ok=True)

# Load dataset and model
df = pd.read_csv(DATA_PATH)
model_bundle = joblib.load(MODEL_PATH)

model = model_bundle["model"]
feature_columns = model_bundle["feature_columns"]

print("Dataset and Model Loaded Successfully!")

# Prepare features and target
X = df[feature_columns]
y = df["Class"]

# Same Train/Test Split used during training
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Predict on original test data
print("\nEvaluating Model...")

y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

# Calculate evaluation metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, zero_division=0)
recall = recall_score(y_test, y_pred, zero_division=0)
f1 = f1_score(y_test, y_pred, zero_division=0)
roc_auc = roc_auc_score(y_test, y_prob)

# Display results
print("\n========== MODEL EVALUATION ==========")

print(f"Accuracy:  {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1 Score:  {f1:.4f}")
print(f"ROC-AUC:   {roc_auc:.4f}")

# Classification Report
print("\nClassification Report:")
report = classification_report(
    y_test,
    y_pred,
    target_names=["Legitimate", "Fraud"],
    zero_division=0
)
print(report)

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(7, 5))
sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=["Legitimate", "Fraud"],
    yticklabels=["Legitimate", "Fraud"]
)

plt.title("Fraud Detection Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()

plt.savefig(
    os.path.join(REPORT_DIR, "confusion_matrix.png")
)
plt.close()

# Feature Importance
importance = pd.Series(
    model.feature_importances_,
    index=feature_columns
).sort_values(ascending=False)

plt.figure(figsize=(10, 7))
importance.head(15).sort_values().plot(
    kind="barh"
)

plt.title("Top 15 Important Features")
plt.xlabel("Importance")
plt.tight_layout()

plt.savefig(
    os.path.join(REPORT_DIR, "feature_importance.png")
)
plt.close()

# Save evaluation report
with open(
    os.path.join(REPORT_DIR, "evaluation_report.txt"),
    "w"
) as file:

    file.write("FRAUD DETECTION MODEL EVALUATION\n\n")
    file.write(f"Accuracy: {accuracy:.4f}\n")
    file.write(f"Precision: {precision:.4f}\n")
    file.write(f"Recall: {recall:.4f}\n")
    file.write(f"F1 Score: {f1:.4f}\n")
    file.write(f"ROC-AUC: {roc_auc:.4f}\n\n")
    file.write(report)

print("\nEvaluation Completed Successfully!")
print("Reports saved in reports folder.")
