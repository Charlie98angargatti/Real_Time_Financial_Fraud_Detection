#read_iceberg.py

from pyspark.sql import SparkSession

# Create Spark session with Iceberg configs
spark = SparkSession.builder \
    .appName("Read Iceberg Table") \
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

# Optional: reduce log noise
spark.sparkContext.setLogLevel("ERROR")

# ----------------------------------------
# Read Iceberg table (CORRECT WAY)
# ----------------------------------------

# Option 1: Using DataFrame API
df = spark.read.format("iceberg").load("local.db.fraud_transactions")

# Option 2: Using SQL (recommended)
# df = spark.sql("SELECT * FROM local.db.fraud_transactions")

# Show data
df.show(truncate=False)

# Print schema
df.printSchema()

# Count rows
print("Row count:", df.count())

# Stop Spark session
spark.stop()


# from pyspark.sql import SparkSession

# spark = SparkSession.builder \
#     .appName("Read Iceberg") \
#     .config(
#         "spark.jars.packages",
#         "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.5.0"
#     ) \
#     .config(
#         "spark.sql.extensions",
#         "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions"
#     ) \
#     .config(
#         "spark.sql.catalog.local",
#         "org.apache.iceberg.spark.SparkCatalog"
#     ) \
#     .config(
#         "spark.sql.catalog.local.type",
#         "hadoop"
#     ) \
#     .config(    
#         "spark.sql.catalog.local.warehouse",
#         "file:///D:/Finance_Fraud_Detection/iceberg_warehouse"
#     ) \
#     .getOrCreate()

# df = spark.read.parquet("iceberg_warehouse/db/fraud_transactions")

# df.show(truncate=False)

# from pyspark.sql import SparkSession

# spark = SparkSession.builder \
#     .appName("Read Iceberg") \
#     .config("spark.jars.packages",
#             "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.4.2") \
#     .config("spark.sql.extensions",
#             "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
#     .config("spark.sql.catalog.local",
#             "org.apache.iceberg.spark.SparkCatalog") \
#     .config("spark.sql.catalog.local.type", "hadoop") \
#     .config("spark.sql.catalog.local.warehouse",
#             "file:///D:/Finance_Fraud_Detection/iceberg_warehouse") \
#     .getOrCreate()

# df = spark.read.format("iceberg").load("local.db.fraud_transactions")

# df.show()

# from pyspark.sql import SparkSession

# spark = SparkSession.builder \
#     .appName("Read Iceberg") \
#     .config("spark.sql.extensions",
#             "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
#     .config("spark.sql.catalog.local",
#             "org.apache.iceberg.spark.SparkCatalog") \
#     .config("spark.sql.catalog.local.type", "hadoop") \
#     .config("spark.sql.catalog.local.warehouse",
#             "file:///D:/Finance_Fraud_Detection/iceberg_warehouse") \
#     .getOrCreate()

# df = spark.read.format("iceberg").load("local.db.fraud_transactions")

# df.show()

