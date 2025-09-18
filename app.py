import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("employee_salaries_india.csv")  # Updated file
    return df

df = load_data()

# Features & target
X = df.drop("salary_in_inr", axis=1)
y = df["salary_in_inr"]

# Separate categorical & numerical columns
categorical_cols = X.select_dtypes(include=["object"]).columns
numerical_cols = X.select_dtypes(include=["int64", "float64"]).columns

# Preprocessing
categorical_transformer = OneHotEncoder(handle_unknown="ignore")
numerical_transformer = StandardScaler()

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numerical_transformer, numerical_cols),
        ("cat", categorical_transformer, categorical_cols)
    ]
)

# Model
model = RandomForestRegressor(n_estimators=200, random_state=42)

# Pipeline
pipeline = Pipeline(steps=[("preprocessor", preprocessor),
                           ("model", model)])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
pipeline.fit(X_train, y_train)

# Streamlit UI
st.title("🇮🇳 Employee Salary Prediction App (India)")

st.write("Enter employee details to predict **salary in INR (₹)**:")

# Collect user input
experience = st.slider("Years of Experience", 0, 40, 3)
education = st.selectbox("Education Level", df["education"].unique())
location = st.selectbox("Location", df["location"].unique())
company_size = st.selectbox("Company Size", df["company_size"].unique())
industry = st.selectbox("Industry", df["industry"].unique())
job_role = st.selectbox("Job Role", df["job_role"].unique())
remote = st.radio("Remote Work?", ["Yes", "No"])

# Prepare input data
input_data = pd.DataFrame({
    "experience": [experience],
    "education": [education],
    "location": [location],
    "company_size": [company_size],
    "industry": [industry],
    "job_role": [job_role],
    "remote": [remote]
})

# Predict
if st.button("Predict Salary"):
    prediction = pipeline.predict(input_data)[0]
    st.success(f"💰 Estimated Salary: ₹{prediction:,.0f}")
