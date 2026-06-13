import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Load dataset
df = pd.read_csv(
    r"D:\pyvharm_Projects\customerchurnproject\Data\WA_Fn-UseC_-Telco-Customer-Churn.csv"
)

# Cleaning
df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)

df.dropna(inplace=True)

df.drop("customerID", axis=1, inplace=True)

# Convert target
df["Churn"] = df["Churn"].map({
    "No": 0,
    "Yes": 1
})

# Encode categorical columns
df = pd.get_dummies(
    df,
    drop_first=True
)

# Features and target
X = df.drop("Churn", axis=1)
y = df["Churn"]

# Train model
model = RandomForestClassifier(
    random_state=42
)

model.fit(X, y)

# Feature importance
importance_df = pd.DataFrame({
    "Feature": X.columns,
    "Importance": model.feature_importances_
})

# Top 10 features
top_10 = importance_df.sort_values(
    by="Importance",
    ascending=False
).head(10)

# Plot
plt.figure(figsize=(10,6))

plt.barh(
    top_10["Feature"],
    top_10["Importance"]
)

plt.title("Top 10 Customer Churn Drivers")
plt.xlabel("Importance Score")

plt.tight_layout()

plt.savefig(
    r"D:\pyvharm_Projects\customerchurnproject\reports\feature_importance.png"
)

plt.show()