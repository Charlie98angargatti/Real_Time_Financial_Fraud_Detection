def apply_fraud_rules(df):
    print("🔹 Applying fraud detection rules...")

    # Rule 1: High transaction amount
    df["high_amount_flag"] = df["amount"] > 200000

    # Rule 2: Transfer or Cash Out (common fraud types)
    df["type_flag"] = df["type"].isin(["TRANSFER", "CASH_OUT"])

    # Rule 3: Destination balance anomaly
    df["balance_mismatch"] = (
        df["oldbalanceDest"] == 0
    ) & (df["newbalanceDest"] > 0)

    # Rule 4: Sender balance drops to zero
    df["sender_empty"] = df["newbalanceOrig"] == 0

    # Rule 5: Empty sender account after transaction
    df["empty_balance_flag"] = df["newbalanceOrig"] == 0

    #Rule 6 balance differenceing
    df["balance_diff"] = df["oldbalanceOrg"] - df["newbalanceOrig"]

    df["sudden_drop_flag"] = df["balance_diff"] > 200000

    # Combine rules
    df["rule_fraud"] = (
        df["high_amount_flag"] &
        df["type_flag"] &
        df["balance_mismatch"] & 
        df["sender_empty"] &
        df["empty_balance_flag"] &
        df["sudden_drop_flag"] 
    )

    print("✅ Improved Fraud rules applied")

    return df

