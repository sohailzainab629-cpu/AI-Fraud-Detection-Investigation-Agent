
import pandas as pd
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE

# Project paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "dataset", "engineered_creditcard.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")

os.makedirs(MODEL_DIR, exist_ok=True)

MODEL_PATH = os.path.join(MODEL_DIR, "fraud_model.pkl")

# Load dataset
df = pd.read_csv(DATA_PATH)

print("Dataset Loaded Successfully!")
print("Dataset Shape:", df.shape)

# Separate features and target
X = df.drop("Class", axis=1)
y = df["Class"]

# Train Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTraining Data:", X_train.shape)
print("Testing Data:", X_test.shape)

# Handle imbalanced data using SMOTE
print("\nApplying SMOTE...")

smote = SMOTE(
    sampling_strategy=0.2,
    random_state=42
)

X_train_resampled, y_train_resampled = smote.fit_resample(
    X_train,
    y_train
)

print("Before SMOTE:", y_train.value_counts().to_dict())
print("After SMOTE:", y_train_resampled.value_counts().to_dict())

# Train Random Forest Model
print("\nTraining Random Forest Model...")

model = RandomForestClassifier(
    n_estimators=150,
    max_depth=20,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train_resampled, y_train_resampled)

print("\nModel Training Completed!")

# Save model and feature information
model_bundle = {
    "model": model,
    "feature_columns": list(X.columns)
}

joblib.dump(model_bundle, MODEL_PATH)

print("\nModel Saved Successfully!")
print("Model Path:", MODEL_PATH)
