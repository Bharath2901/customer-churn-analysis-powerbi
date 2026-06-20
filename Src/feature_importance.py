import pandas as pd

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

# Target variable
df["Churn"] = df["Churn"].map({
    "No": 0,
    "Yes": 1
})

# Convert categorical columns
df = pd.get_dummies(
    df,
    drop_first=True
)

# Features and target
X = df.drop("Churn", axis=1)

y = df["Churn"]

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train models
model = RandomForestClassifier(
    random_state=42
)

model.fit(X_train, y_train)

# Feature Importance
importance_df = pd.DataFrame({
    "Feature": X.columns,
    "Importance": model.feature_importances_
})

importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
)

print(importance_df.head(10))