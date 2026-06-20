# Customer Churn Prediction & Business Intelligence Dashboard

## Overview

Customer churn is a critical business challenge that directly impacts revenue and customer lifetime value. This project combines Machine Learning and Business Intelligence techniques to identify key drivers of customer churn and provide actionable insights through an interactive Power BI dashboard.

The project uses the Telco Customer Churn dataset to analyze customer behaviour, build predictive models, and visualize churn patterns across contracts, internet services, payment methods, and billing characteristics.

---

## Business Problem

Customer acquisition is significantly more expensive than customer retention. Understanding why customers leave enables organizations to:

* Reduce customer attrition
* Improve customer satisfaction
* Increase revenue retention
* Design targeted retention strategies
* Improve long-term customer lifetime value

---

## Dataset

**Source:** Telco Customer Churn Dataset

### Dataset Summary

* 7,043 customer records
* 21 customer-related attributes
* Binary churn target variable (Yes/No)

### Features Include

* Customer demographics
* Contract information
* Internet service details
* Billing and payment information
* Monthly and total charges
* Customer tenure

---

## Technologies Used

### Data Analysis & Machine Learning

* Python
* Pandas
* NumPy
* Scikit-Learn

### Data Visualization

* Matplotlib
* Seaborn
* Power BI

### Development Tools

* Git
* GitHub
* PyCharm

---

## Project Workflow

### 1. Data Cleaning

* Handled missing values
* Converted TotalCharges to numeric format
* Removed invalid records
* Prepared dataset for analysis

### 2. Exploratory Data Analysis (EDA)

* Churn distribution analysis
* Customer tenure analysis
* Monthly charges analysis
* Contract type analysis
* Service subscription analysis

### 3. Feature Engineering

* One-hot encoding of categorical variables
* Feature preparation for machine learning
* Dataset transformation and preprocessing

### 4. Machine Learning Model Development

#### Logistic Regression

* Accuracy: 78.5%

#### Random Forest Classifier

* Accuracy: 78.5%

### 5. Feature Importance Analysis

Top drivers of customer churn:

1. Total Charges
2. Monthly Charges
3. Customer Tenure
4. Fiber Optic Internet Service
5. Electronic Check Payment Method
6. Online Security
7. Contract Type

### 6. Power BI Dashboard

Developed an interactive dashboard to support business decision-making.

Dashboard Features:

* Total Customers KPI
* Churn Rate KPI
* Churned Customers KPI
* Retained Customers KPI
* Contract Type Analysis
* Internet Service Analysis
* Payment Method Analysis
* Monthly Charges Analysis
* Interactive Filtering using Slicers

---

## Model Performance

| Model               | Accuracy |
| ------------------- | -------- |
| Logistic Regression | 78.5%    |
| Random Forest       | 78.5%    |

### Classification Performance

* Strong prediction of retained customers
* Reasonable churn detection capability
* Suitable baseline model for churn prediction tasks

---

## Key Business Insights

### Contract Type

Customers on month-to-month contracts exhibit significantly higher churn rates compared to one-year and two-year contract customers.

### Internet Service

Fiber optic customers demonstrate higher churn behaviour than DSL users.

### Payment Method

Customers using electronic check payment methods are more likely to churn.

### Monthly Charges

Higher monthly charges are associated with increased churn probability.

### Customer Tenure

Longer-tenured customers are considerably less likely to leave.

---

## Repository Structure

```text
customer-churn-analysis-powerbi
│
├── Data
├── Src
├── reports
├── screenshots
├── Customer_Churn_Dashboard.pbix
├── README.md
└── main.py
```

---

## Dashboard Screenshots

### Dashboard Overview

(Add dashboard_overview.png)

### Contract Analysis

(Add contract_analysis.png)

### Internet Service Analysis

(Add internet_service_analysis.png)

### Payment Method Analysis

(Add payment_method_analysis.png)

---

## Future Improvements

* Hyperparameter tuning
* Cross-validation
* Advanced ensemble models
* Streamlit deployment
* Real-time dashboard integration
* Customer retention recommendation engine

---

## Author

**Bharath M.J.**

MSc Data Science | University of the West of England

Aspiring Data Scientist | Data Analyst | Machine Learning Enthusiast
