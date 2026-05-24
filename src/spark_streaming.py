#spark_streaming.py

import os

os.environ["HADOOP_HOME"] = "C:\\hadoop"
os.environ["PATH"] += ";C:\\hadoop\\bin"

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import *

# Spark Session with Kafka + Iceberg
spark = SparkSession.builder \
    .appName("Kafka Fraud Streaming Iceberg") \
    .config(
        "spark.jars.packages",
        ",".join([
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0",
            "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.5.0"
        ])
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

spark.sparkContext.setLogLevel("ERROR")

# Create database
spark.sql("CREATE DATABASE IF NOT EXISTS local.db")

# Create Iceberg table
spark.sql("""
CREATE TABLE IF NOT EXISTS local.db.fraud_transactions (        
    step INT,
    type STRING,
    amount DOUBLE,
    nameOrig STRING,
    oldbalanceOrg DOUBLE,
    newbalanceOrig DOUBLE,
    nameDest STRING,
    oldbalanceDest DOUBLE,
    newbalanceDest DOUBLE,
    isFraud INT,
    rule_fraud BOOLEAN
 )
          
USING iceberg
""")

schema = StructType([
    StructField("step", IntegerType()),
    StructField("type", StringType()),
    StructField("amount", DoubleType()),
    StructField("nameOrig", StringType()),
    StructField("oldbalanceOrg", DoubleType()),
    StructField("newbalanceOrig", DoubleType()),
    StructField("nameDest", StringType()),
    StructField("oldbalanceDest", DoubleType()),
    StructField("newbalanceDest", DoubleType()),
    StructField("isFraud", IntegerType())
])

# Read Kafka stream
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "transactions") \
    .option("startingOffsets", "earliest") \
    .load()

# Parse Kafka JSON
json_df = df.selectExpr("CAST(value AS STRING)")

parsed_df = json_df.select(
    from_json(col("value"), schema).alias("data")
).select("data.*")

# Fraud rule
fraud_df = parsed_df.withColumn(
    "rule_fraud",
    (col("amount") > 200000) &
    (col("type").isin("TRANSFER", "CASH_OUT")) &
    (col("oldbalanceDest") == 0) &
    (col("newbalanceDest") > 0) &
    (col("newbalanceOrig") == 0)
)

query = fraud_df.writeStream \
    .outputMode("append") \
    .format("iceberg") \
    .option("checkpointLocation", "D:/Finance_Fraud_Detection/checkpoint") \
    .toTable("local.db.fraud_transactions")

query.awaitTermination()

