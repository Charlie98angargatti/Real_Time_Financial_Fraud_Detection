# spark_processing.py



from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Step 1: Create Spark Session
def create_spark_session():
    spark = SparkSession.builder \
        .appName("Fraud Detection") \
        .getOrCreate()
    
    return spark


def load_data_spark(spark):
    df = spark.read.csv("D:/Finance_Fraud_Detection/data/raw/PS_20174392719_1491204439457_log.csv", header=True, inferSchema=True)
    
    print("✅ Data loaded in Spark")
    df.show(5)

    return df


def apply_fraud_rules_spark(df):

    df = df.withColumn("high_amount_flag", col("amount") > 200000)

    df = df.withColumn("type_flag",
        col("type").isin("TRANSFER", "CASH_OUT")
    )

    df = df.withColumn("balance_mismatch",
        (col("oldbalanceDest") == 0) & (col("newbalanceDest") > 0)
    )

    df = df.withColumn("sender_empty",
        col("newbalanceOrig") == 0
    )

    df = df.withColumn("rule_fraud",
        col("high_amount_flag") &
        col("type_flag") &
        col("balance_mismatch") &
        col("sender_empty")
    )

    return df

# Step 4: Save Output
def save_spark_data(df):
    print("🔹 Saving sample data...")

    df_sample = df.limit(100000)  # only 100k rows

    pandas_df = df_sample.toPandas()

    pandas_df.to_csv("data/processed/spark_sample1.csv", index=False)

    print("✅ Sample data saved")

    # df.write.mode("overwrite").option("header", True).parquet("data/processed/spark_output_parquet")
    # print("✅ Spark data saved")

# Step 5: Main
if __name__ == "__main__":
    spark = create_spark_session()

    df = load_data_spark(spark)

    df = apply_fraud_rules_spark(df)

    save_spark_data(df)

