import pandas as pd
from processing import preprocess_data ,save_data
from fraud_rules import apply_fraud_rules

def load_data(path):
    df = pd.read_csv(path)

    print("✅ Data Loaded Successfully\n")

    print("🔹 Shape of data:")
    print(df.shape)

    # print("\n🔹 Column names:")
    # print(df.columns)

    # print("\n🔹 Data types:")
    # print(df.dtypes)

    # print("\n🔹 Missing values:")
    # print(df.isnull().sum())

    print("\n🔹 First 5 rows:")
    print(df.head())

    return df


if __name__ == "__main__":
    df = load_data("D:/Finance_Fraud_Detection/data/raw/PS_20174392719_1491204439457_log.csv")

    df = preprocess_data(df)

    df = apply_fraud_rules(df)

    save_data(df)

    print("\n🔹 After applying fraud rules:")
    print(df[["amount", "type", "isFraud", "rule_fraud"]].head())

    print("\n🔹 Actual Fraud Cases:", df["isFraud"].sum())
    print("🔹 Total Rule Detected Frauds:", df["rule_fraud"].sum())

    print("\n🔹 Sample Results:")
    print(df[["amount", "type", "isFraud", "rule_fraud"]].head(10));