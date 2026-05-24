import pandas as pd

def preprocess_data(df):
    # Example: basic cleaning
    df = df.drop_duplicates()
    df = df.fillna(0)
    return df 

def save_data(df):
    print("🔹 Saving processed data...")

    df.to_csv("D:/Finance_Fraud_Detection/data/processed/processed_data.csv", index=False)

    print("✅ Data saved successfully")