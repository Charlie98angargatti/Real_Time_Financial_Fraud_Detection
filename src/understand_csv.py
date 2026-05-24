# 1. step
# 👉 Time unit (like hour/day block)
# Example:
# step = 1
# Means:
# First time period in simulation


# 2. type

# Type of transaction:

# Type	Meaning
# PAYMENT	paying merchants/services
# TRANSFER	moving money to another account
# CASH_OUT	withdrawing cash
# DEBIT	bank deduction

# 3. amount

# 👉 Money involved in transaction

# Example:

# amount = 9839.64

# Means:

# ₹9839.64 transferred

# 5. 🏦 Account balance columns

# These are VERY important for fraud detection

# 4. nameOrig

# 👉 Sender account ID

# Example:

# C1231006815

# Means:

# Customer account sending money

# 5. oldbalanceOrg

# 👉 Sender balance BEFORE transaction

# 6. newbalanceOrig

# 👉 Sender balance AFTER transaction

# 🧠 Example:
# oldbalanceOrg = 170136
# amount = 9839.64
# newbalanceOrig =  160296.36 

# ✔ Correct behavior

# 6. 🏦 Receiver side
# 7. nameDest
# 👉 Receiver accoun
# C = customer
# M = merchant

# 8. oldbalanceDest
# 👉 Receiver balance BEFORE transaction

# 9. newbalanceDest
# 👉 Receiver balance AFTER transaction

# 10. isFraud

# 👉 REAL fraud label (from dataset)

# Value	Meaning
# 0	Not fraud
# 1	Fraud
# 💡 This is what machine learning tries to predict.

# 11. isFlaggedFraud

# 👉 Bank’s internal rule-based flag
# Usually:
# 1 = suspicious transaction
# 0 = normal

# 12. high_amount_flag

# 👉 Amount is unusually high

# Example logic:

# if amount > threshold → TRUE
# 13. type_flag

# 👉 Some transaction types are risky

# Example:

# TRANSFER = risky
# CASH_OUT = risky
# 14. balance_mismatch

# 👉 Money doesn’t match expected math

# Example:
# oldbalanceOrg - amount ≠ newbalanceOrig

# If mismatch → suspicious

# 15. sender_empty

# 👉 Sender balance became zero

# Often fraud happens when:

# account emptied suddenly
# 16. empty_balance_flag

# 👉 Extra check for zero balance cases

# 17. balance_diff

# 👉 Difference check:

# oldbalanceOrg - newbalanceOrig

# 18. sudden_drop_flag

# 👉 Detects sudden big drop in balance

# 19. rule_fraud (VERY IMPORTANT)

# 👉 FINAL DECISION from your logic

# This is NOT real bank label.
# This is YOUR system’s prediction:
# TRUE = suspicious transaction
# FALSE = normal

# 9. 🧠 How fraud detection works (simple flow)

# Your system is doing this:

# Transaction comes in
#         ↓
# Check amount
#         ↓
# Check balance mismatch
#         ↓
# Check transaction type
#         ↓
# Apply rules
#         ↓
# rule_fraud = TRUE / FALSE


# 2. How to read a CSV mentally (pro mindset)

# Think like this:

# Column	Meaning
# step	time / sequence of transaction
# type	what kind of transaction
# amount	money involved
# nameOrig	sender
# nameDest	receiver
# isFraud	actual fraud or not (label)
# isFlaggedFraud	system suspected it