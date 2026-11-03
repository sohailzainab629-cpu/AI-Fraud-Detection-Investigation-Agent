
import pandas as pd
import numpy as np
import os

# Project paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "dataset", "cleaned_creditcard.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "dataset", "engineered_creditcard.csv")

# Load cleaned dataset
df = pd.read_csv(DATA_PATH)

print("Feature Engineering Started!")

# Feature 1: Extract estimated hour from elapsed transaction time
df["Hour"] = (df["Time"] / 3600) % 24

# Feature 2: Log transformation of transaction amount
df["Amount_log"] = np.log1p(df["Amount"])

# Check new features
print("\nNew Features:")
print(df[["Time", "Hour", "Amount", "Amount_log"]].head())

# Save engineered dataset
df.to_csv(OUTPUT_PATH, index=False)

print("\nFeature Engineering Completed!")
print("Final Dataset Shape:", df.shape)
print("Saved at:", OUTPUT_PATH)
