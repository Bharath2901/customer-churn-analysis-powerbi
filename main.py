import pandas as pd

df = pd.read_csv(
    r"D:\pyvharm_Projects\customerchurnproject\Data\WA_Fn-UseC_-Telco-Customer-Churn.csv"
)

print("\nDataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nDataset Info:")
df.info()

print("\nMissing Values:")
print(df.isnull().sum())