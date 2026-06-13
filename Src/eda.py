
import pandas as pd
import seaborn as sns

import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt

# Load data
df = pd.read_csv(
    r"D:\pyvharm_Projects\customerchurnproject\Data\WA_Fn-UseC_-Telco-Customer-Churn.csv"
)

# Clean data
df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)

df.dropna(inplace=True)

# Plot churn distribution

sns.countplot(x="Churn", data=df)

plt.title("Customer Churn Distribution")

plt.savefig(
    r"D:\pyvharm_Projects\customerchurnproject\reports\churn_distribution.png"
)

plt.close()

print("\nChurn Percentage:")

churn_rate = (
    df["Churn"]
    .value_counts(normalize=True)
    * 100
)

print(churn_rate)


plt.figure(figsize=(8,5))

sns.boxplot(
    x="Churn",
    y="MonthlyCharges",
    data=df
)

plt.title("Monthly Charges vs Churn")
plt.show()

plt.figure(figsize=(8,5))

sns.boxplot(
    x="Churn",
    y="tenure",
    data=df
)

plt.title("Tenure vs Churn")
plt.show()


print("EDA completed")