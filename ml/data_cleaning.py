
import pandas as pd
import os

# Project paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "dataset", "creditcard.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "dataset", "cleaned_creditcard.csv")

# Load dataset
df = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully!")
print("Original Shape:", df.shape)

# Check missing values
print("\nMissing Values:")
print(df.isnull().sum().sum())

# Check duplicate records
print("\nDuplicate Records:")
print(df.duplicated().sum())

# Remove duplicate records
df = df.drop_duplicates()

# Check missing values again
if df.isnull().sum().sum() > 0:
    df = df.dropna()

# Save cleaned dataset
df.to_csv(OUTPUT_PATH, index=False)

print("\nData Cleaning Completed!")
print("Cleaned Shape:", df.shape)
print("Cleaned Dataset Saved:", OUTPUT_PATH)

print("\nClass Distribution:")
print(df["Class"].value_counts())
