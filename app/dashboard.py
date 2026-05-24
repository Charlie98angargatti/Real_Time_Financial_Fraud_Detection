


import streamlit as st
import pandas as pd

@st.cache_data
def load_data(path):
    return pd.read_csv(path)

# Load full dataset once
df = load_data("D:/Finance_Fraud_Detection/data/processed/processed_data.csv")

# Sample for charts
df_sample = df.sample(10000, random_state=42)

st.title("💳 Fraud Detection Dashboard")

# Metrics
st.subheader("Key Metrics")
st.write("Total Transactions:", len(df))
st.write("Actual Fraud Cases:", df["isFraud"].sum())
st.write("Rule Detected Frauds:", df["rule_fraud"].sum())

# Charts using sample
st.subheader("Transaction Amount Distribution")
st.line_chart(df_sample["amount"])

st.subheader("Fraud vs Normal")
st.bar_chart(df_sample["isFraud"].value_counts())

# Suspicious transactions (limited table)
st.subheader("🚨 Suspicious Transactions")
st.dataframe(df[df["rule_fraud"] == True].head(100))



import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/processed_data.csv")

df = load_data()
df_sample = df.sample(10000)


st.title("💳 Fraud Detection Dashboard")

df = pd.read_csv("D:/Finance_Fraud_Detection/data/processed/processed_data.csv")

# Take small sample for visualization
df_sample = df.sample(10000)

# Metrics
st.subheader("Key Metrics")
st.write("Total Transactions:", len(df))
st.write("Actual Fraud Cases:", df["isFraud"].sum())
st.write("Rule Detected Frauds:", df["rule_fraud"].sum())

# Charts
st.subheader("Transaction Amount Distribution")
# st.line_chart(df["amount"])
st.line_chart(df_sample["amount"])

st.subheader("Fraud vs Normal")
# st.bar_chart(df["isFraud"].value_counts())
st.bar_chart(df["isFraud"].value_counts())

# Suspicious transactions
st.subheader("🚨 Suspicious Transactions")
st.dataframe(df[df["rule_fraud"] == True].head(100))



