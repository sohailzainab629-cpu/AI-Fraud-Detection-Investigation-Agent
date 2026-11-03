
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Project paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "dataset", "cleaned_creditcard.csv")
REPORT_PATH = os.path.join(BASE_DIR, "reports")

os.makedirs(REPORT_PATH, exist_ok=True)

# Load dataset
df = pd.read_csv(DATA_PATH)

print("EDA Started Successfully!")

# 1. Dataset Information
print("\nDataset Shape:")
print(df.shape)

print("\nDataset Columns:")
print(df.columns.tolist())

print("\nDataset Information:")
df.info()

# 2. Statistical Analysis
print("\nStatistical Summary:")
print(df.describe())

# 3. Fraud Distribution
print("\nTransaction Class Distribution:")
print(df["Class"].value_counts())

print("\nPercentage Distribution:")
print(df["Class"].value_counts(normalize=True) * 100)

# 4. Fraud vs Legitimate Graph
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x="Class")

plt.title("Fraud vs Legitimate Transactions")
plt.xlabel("Transaction Class (0=Legitimate, 1=Fraud)")
plt.ylabel("Number of Transactions")

plt.savefig(os.path.join(REPORT_PATH, "fraud_distribution.png"))


# 5. Transaction Amount Distribution
plt.figure(figsize=(8, 5))
sns.histplot(df["Amount"], bins=50, kde=True)

plt.title("Transaction Amount Distribution")
plt.xlabel("Transaction Amount")
plt.ylabel("Frequency")

plt.savefig(os.path.join(REPORT_PATH, "amount_distribution.png"))


# 6. Fraud vs Legitimate Amount
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x="Class", y="Amount")

plt.title("Transaction Amount by Class")
plt.xlabel("Class (0=Legitimate, 1=Fraud)")
plt.ylabel("Amount")

plt.savefig(os.path.join(REPORT_PATH, "amount_by_class.png"))


# 7. Correlation Analysis
plt.figure(figsize=(16, 12))
correlation = df.corr()

sns.heatmap(correlation, cmap="coolwarm", center=0)

plt.title("Feature Correlation Heatmap")
plt.tight_layout()

plt.savefig(os.path.join(REPORT_PATH, "correlation_heatmap.png"))


print("\nEDA Completed Successfully!")
print("All graphs saved in reports folder.")
