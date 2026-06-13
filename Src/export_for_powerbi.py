import pandas as pd

df = pd.read_csv(
    r"D:\pyvharm_Projects\customerchurnproject\Data\WA_Fn-UseC_-Telco-Customer-Churn.csv"
)

df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)

df.dropna(inplace=True)

df.to_csv(
    r"D:\pyvharm_Projects\customerchurnproject\Data\clean_churn_data.csv",
    index=False
)

print("Power BI file created successfully!")