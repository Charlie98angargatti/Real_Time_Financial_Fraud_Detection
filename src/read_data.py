# import pandas as pd

# df = pd.read_parquet(
#     "D:/Finance_Fraud_Detection/iceberg_warehouse/db/fraud_transactions/data/00001.parquet"
# )

# print(df.head())

# import os

# folder = "D:/Finance_Fraud_Detection/iceberg_warehouse/db/fraud_transactions/data"
# print(os.listdir(folder))

# import pandas as pd
# import os

# folder =r"D:\Finance_Fraud_Detection\iceberg_warehouse\db\fraud_transactions\data"

# files = [f for f in os.listdir(folder) if f.endswith(".parquet")]

# df = pd.read_parquet(os.path.join(folder, files[0]))

# print(df.head())

import pandas as pd
import os

folder = "D:/Finance_Fraud_Detection/iceberg_warehouse/db/fraud_transactions/data"

files = [f for f in os.listdir(folder) if f.endswith(".parquet")]

df = pd.read_parquet(os.path.join(folder, files[0]))

print(df.head())