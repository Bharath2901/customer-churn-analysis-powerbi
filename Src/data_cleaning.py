import pandas as pd

# Load dataset
df = pd.read_csv(
    r"D:\pyvharm_Projects\customerchurnproject\Data\WA_Fn-UseC_-Telco-Customer-Churn.csv"
)

print("Before Cleaning:")
print(df.shape)

# Convert TotalCharges to numeric
df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)

print("\nMissing values after conversion:")
print(df["TotalCharges"].isnull().sum())

# Remove rows with missing TotalCharges
df.dropna(inplace=True)

print("\nAfter Cleaning:")
print(df.shape)

# Remove customerID (not useful for prediction)
df.drop("customerID", axis=1, inplace=True)

print("\nFinal Shape:")
print(df.shape)