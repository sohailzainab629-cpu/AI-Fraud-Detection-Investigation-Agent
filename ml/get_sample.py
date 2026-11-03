
import pandas as pd
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "dataset", "cleaned_creditcard.csv")

df = pd.read_csv(DATA_PATH)

# Get one real fraud transaction
sample = df[df["Class"] == 1].iloc[0]

# Remove target column
transaction = sample.drop("Class").to_dict()

print("REAL FRAUD TRANSACTION:")
print(json.dumps({"transaction": transaction}, indent=2))
