import pandas as pd
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


# Load data
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

# Convert target variable
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

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train models
model = LogisticRegression(max_iter=1000)

model.fit(X_train, y_train)

# Predictions
predictions = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, predictions)

print("Accuracy:", accuracy)

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        predictions
    )
)

print("\nConfusion Matrix:")

print(
    confusion_matrix(
        y_test,
        predictions
    )
)