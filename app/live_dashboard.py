#live_dashboard.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pyspark.sql import SparkSession

st.set_page_config(page_title="Fraud Dashboard", layout="wide")

st.title("🚨 Fraud Detection Dashboard")

# -------------------------------
# Spark Session
# -------------------------------
@st.cache_resource
def get_spark():
    return SparkSession.builder \
        .appName("Dashboard") \
        .config(
            "spark.jars.packages",
            "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.5.0"
        ) \
        .config(
            "spark.sql.extensions",
            "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions"
        ) \
        .config(
            "spark.sql.catalog.local",
            "org.apache.iceberg.spark.SparkCatalog"
        ) \
        .config(
            "spark.sql.catalog.local.type",
            "hadoop"
        ) \
        .config(
            "spark.sql.catalog.local.warehouse",
            "file:///D:/Finance_Fraud_Detection/iceberg_warehouse"
        ) \
        .getOrCreate()

spark = get_spark()

# -------------------------------
# Load Data
# -------------------------------
try:
    df = spark.read.format("iceberg").load("local.db.fraud_transactions")
    pdf = df.toPandas()

    # -------------------------------
    # KPIs
    # -------------------------------
    total_txn = len(pdf)
    fraud_txn = int(pdf["isFraud"].sum())
    rule_fraud = int(pdf["rule_fraud"].sum())
    fraud_rate = (fraud_txn / total_txn) * 100 if total_txn > 0 else 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Transactions", total_txn)
    col2.metric("Fraud Cases", fraud_txn)
    col3.metric("Fraud Rate (%)", f"{fraud_rate:.2f}")
    col4.metric("Rule-based Fraud", rule_fraud)

    st.divider()

    # -------------------------------
    # Graph 1: Fraud vs Non-Fraud
    # -------------------------------
    st.subheader("Fraud vs Non-Fraud Distribution")

    fig1, ax1 = plt.subplots()
    sns.countplot(x="isFraud", data=pdf, ax=ax1)

    ax1.set_xticks([0, 1])
    ax1.set_xticklabels(["Non-Fraud", "Fraud"])

    st.pyplot(fig1)

    # -------------------------------
    # Graph 2: Transaction Amount Distribution
    # -------------------------------
    if "amount" in pdf.columns:
        st.subheader("Transaction Amount Distribution")

        fig2, ax2 = plt.subplots()
        sns.histplot(pdf["amount"], bins=50, kde=True, ax=ax2)
        st.pyplot(fig2)

    # -------------------------------
    # Graph 3: Fraud by Transaction Type
    # -------------------------------
    if "type" in pdf.columns:
        st.subheader("Fraud by Transaction Type")

        fraud_by_type = pdf.groupby("type")["isFraud"].sum().reset_index()

        fig3, ax3 = plt.subplots()
        sns.barplot(x="type", y="isFraud", data=fraud_by_type, ax=ax3)
        plt.xticks(rotation=45)
        st.pyplot(fig3)

    # -------------------------------
    # Recent Data
    # -------------------------------
    st.subheader("Recent Transactions")
    st.dataframe(pdf.tail(20), width="stretch")

except Exception as e:
    st.warning(f"Waiting for data... {e}")



# import streamlit as st
# from pyspark.sql import SparkSession

# st.title("🚨 Fraud Detection Dashboard")

# @st.cache_resource
# def get_spark():
#     return SparkSession.builder \
#         .appName("Dashboard") \
#         .getOrCreate()

# spark = get_spark()

# try:
#     df = spark.read.parquet("D:/Finance_Fraud_Detection/output")

#     pdf = df.toPandas()

#     st.metric("Total Transactions", len(pdf))
#     st.metric("Fraud Cases", int(pdf["isFraud"].sum()))
#     st.metric("Rule Fraud", int(pdf["rule_fraud"].sum()))

#     st.dataframe(pdf.tail(20))

# except Exception as e:
#     st.warning(f"Waiting for data... {e}")


# import streamlit as st
# from pyspark.sql import SparkSession
# import time

# st.title("🚨 Fraud Detection Dashboard")

# @st.cache_resource
# def get_spark():
#     spark = SparkSession.builder \
#         .appName("IcebergDashboard") \
#         .config(
#             "spark.jars.packages",
#             "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.5.0"
#         ) \
#         .config(
#             "spark.sql.extensions",
#             "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions"
#         ) \
#         .config(
#             "spark.sql.catalog.local",
#             "org.apache.iceberg.spark.SparkCatalog"
#         ) \
#         .config(
#             "spark.sql.catalog.local.type",
#             "hadoop"
#         ) \
#         .config(
#             "spark.sql.catalog.local.warehouse",
#             "file:///D:/Finance_Fraud_Detection/iceberg_warehouse"
#         ) \
#         .config(
#             "spark.sql.parquet.enableVectorizedReader",
#             "false"
#         ) \
#         .getOrCreate()

#     spark.sparkContext.setLogLevel("ERROR")
#     return spark

# spark = get_spark()

# placeholder = st.empty()

# while True:
#     try:
#         df = spark.sql("""
#             SELECT * FROM local.db.fraud_transactions
#             ORDER BY amount DESC
#         """)

#         pdf = df.toPandas()

#         with placeholder.container():
#             st.metric("Total Transactions", len(pdf))
#             st.metric("Fraud Cases", int(pdf["isFraud"].sum()))
#             st.metric("Rule Fraud", int(pdf["rule_fraud"].sum()))

#             st.subheader("Latest Transactions")
#             st.dataframe(pdf.tail(20))

#     except Exception as e:
#         with placeholder.container():
#             st.warning(f"Waiting for data... {e}")

#     time.sleep(5)

# import streamlit as st
# from pyspark.sql import SparkSession
# import time

# st.title("🚨 Fraud Detection Dashboard")

# # 🔥 CREATE SPARK ONLY ONCE
# @st.cache_resource
# def get_spark():
#     return SparkSession.builder \
#         .appName("IcebergReader") \
#         .config("spark.jars.packages",
#                 "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.5.0") \
#         .config("spark.sql.extensions",
#                 "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
#         .config("spark.sql.catalog.local", "org.apache.iceberg.spark.SparkCatalog") \
#         .config("spark.sql.catalog.local.type", "hadoop") \
#         .config("spark.sql.catalog.local.warehouse",
#                 "file:///D:/Finance_Fraud_Detection/iceberg_warehouse") \
#         .getOrCreate()

# spark = get_spark()

# placeholder = st.empty()

# while True:
#     try:
#         df = spark.read.format("iceberg").load("local.db.fraud_transactions")

#         pdf = df.toPandas()

#         with placeholder.container():
#             st.metric("Total Transactions", len(pdf))
#             st.metric("Fraud Cases", int(pdf["isFraud"].sum()))
#             st.metric("Rule Fraud", int(pdf["rule_fraud"].sum()))

#             st.subheader("Fraud Data")
#             st.dataframe(pdf.tail(20))

#     except Exception as e:
#         st.warning(f"Waiting for Spark data... {e}")

#     time.sleep(5)


# import streamlit as st
# from pyspark.sql import SparkSession
# import pandas as pd
# import time

# st.title("🚨 Real-Time Fraud Detection Dashboard")

# # Create Spark session (read-only)
# spark = SparkSession.builder \
#     .appName("Read Iceberg Dashboard") \
#     .config(
#         "spark.jars.packages",
#         "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.5.0"
#     ) \
#     .config(
#         "spark.sql.extensions",
#         "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions"
#     ) \
#     .config("spark.sql.catalog.local", "org.apache.iceberg.spark.SparkCatalog") \
#     .config("spark.sql.catalog.local.type", "hadoop") \
#     .config(
#         "spark.sql.catalog.local.warehouse",
#         "file:///D:/Finance_Fraud_Detection/iceberg_warehouse"
#     ) \
#     .getOrCreate()

# placeholder = st.empty()

# while True:
#     try:
#         df = spark.read.format("iceberg").load("local.db.fraud_transactions")
#         pdf = df.toPandas()

#         with placeholder.container():   # ✅ KEY FIX

#             st.subheader("📊 Metrics")

#             col1, col2, col3 = st.columns(3)

#             col1.metric("Total Transactions", len(pdf))
#             col2.metric("Actual Fraud", int(pdf["isFraud"].sum()))
#             col3.metric("Rule Fraud", int(pdf["rule_fraud"].sum()))

#             st.subheader("📈 Transaction Amount")
#             st.line_chart(pdf["amount"])

#             st.subheader("⚠️ Fraud Distribution")
#             st.bar_chart(pdf["isFraud"].value_counts())

#             st.subheader("🚨 Suspicious Transactions")
#             st.dataframe(pdf[pdf["rule_fraud"] == True].tail(50))

#     except Exception as e:
#         with placeholder.container():
#             st.warning(f"Waiting for data... {e}")

#     time.sleep(5)


# import streamlit as st
# import pandas as pd

# st.set_page_config(page_title="Fraud Dashboard", layout="wide")

# DATA_PATH = r"D:/Finance_Fraud_Detection/data/processed/processed_data.csv"

# @st.cache_data
# def load_data(path):
#     return pd.read_csv(path)

# df = load_data(DATA_PATH)

# df_sample = df.sample(min(10000, len(df)), random_state=42)

# st.title("💳 Fraud Detection Dashboard")

# # ---------------- METRICS ----------------
# st.subheader("📊 Key Metrics")

# col1, col2, col3 = st.columns(3)

# with col1:
#     st.metric("Total Transactions", len(df))

# with col2:
#     st.metric("Actual Fraud Cases", int(df["isFraud"].sum()))

# with col3:
#     st.metric("Rule Detected Frauds", int(df["rule_fraud"].sum()))

# # ---------------- CHARTS ----------------
# st.subheader("📈 Transaction Analysis")

# st.line_chart(df_sample["amount"])

# st.subheader("⚖️ Fraud Distribution")

# fraud_counts = df["isFraud"].value_counts().sort_index()
# st.bar_chart(fraud_counts)

# # ---------------- SUSPICIOUS ----------------
# st.subheader("🚨 Suspicious Transactions")

# st.dataframe(
#     df[df["rule_fraud"] == True].head(100),
#     use_container_width=True
# )

# import streamlit as st
# import pandas as pd

# st.set_page_config(page_title="Fraud Dashboard", layout="wide")

# st.title("🚨 Real-Time Fraud Detection Dashboard")

# file_path = r"D:\Finance_Fraud_Detection\data\processed\spark_sample1.csv"

# df = pd.read_csv(file_path)

# col1, col2 = st.columns(2)

# with col1:
#     st.metric("Total Transactions", len(df))

# with col2:
#     st.metric("Fraud Cases", df["isFraud"].sum())

# st.dataframe(df)

# st.rerun()



# import streamlit as st
# import pandas as pd
# import time

# st.set_page_config(page_title="Fraud Dashboard", layout="wide")

# st.title("🚨 Real-Time Fraud Detection Dashboard")

# file_path = r"D:\Finance_Fraud_Detection\data\processed\spark_sample1.csv"

# placeholder = st.empty()

# while True:
#     df = pd.read_csv(file_path)

#     col1, col2 = st.columns(2)

#     with col1:
#         st.metric("Total Transactions", len(df))

#     with col2:
#         st.metric("Fraud Cases", df["isFraud"].sum())

#     placeholder.dataframe(df)

#     time.sleep(5)



# import streamlit as st
# import pandas as pd
# import time

# st.title("🚨 Real-Time Fraud Detection Dashboard")

# placeholder = st.empty()

# file_path = r"D:\Finance_Fraud_Detection\data\processed\spark_sample1.csv"

# while True:
#     df = pd.read_csv(file_path)

#     placeholder.dataframe(df)

#     time.sleep(5)


# # import streamlit as st
# # import pandas as pd
# # import os
# # import time

# # st.title("🚨 Real-Time Fraud Detection Dashboard")

# # placeholder = st.empty()

# # while True:
# #     files = os.listdir(r"D:\Finance_Fraud_Detection\data\processed\spark_sample1.csv")

# #     csv_files = [f for f in files if f.endswith(".csv")]

# #     if csv_files:
# #         all_data = []

# #         for file in csv_files:
# #             df = pd.read_csv(r"D:\Finance_Fraud_Detection\data\processed\spark_sample1.csv/{file}")
# #             all_data.append(df)

# #         final_df = pd.concat(all_data)

# #         placeholder.dataframe(final_df)

# #     time.sleep(5)

