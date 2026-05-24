# #kafka_producer.py

import pandas as pd
from kafka import KafkaProducer
import json
import time

# -----------------------------
# CONFIG
# -----------------------------
CSV_PATH = "data/raw/PS_20174392719_1491204439457_log.csv"
TOPIC = "transactions"

# 👉 how much data you want to stream
SAMPLE_SIZE = 2000  # change to 10000 / 20000 / 50000

# -----------------------------
# LOAD DATA (SAMPLE ONLY)
# -----------------------------
df = pd.read_csv(CSV_PATH)

# shuffle + sample to simulate real randomness
df = df.sample(n=SAMPLE_SIZE, random_state=42).reset_index(drop=True)

print(f"📦 Streaming {len(df)} records to Kafka...")

# -----------------------------
# KAFKA PRODUCER
# -----------------------------
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    linger_ms=10,        # improves throughput
    batch_size=16384     # faster batching
)

# -----------------------------
# STREAM DATA
# -----------------------------
for i, row in df.iterrows():

    message = {
        "step": int(row["step"]),
        "type": row["type"],
        "amount": float(row["amount"]),
        "nameOrig": row["nameOrig"],
        "oldbalanceOrg": float(row["oldbalanceOrg"]),
        "newbalanceOrig": float(row["newbalanceOrig"]),
        "nameDest": row["nameDest"],
        "oldbalanceDest": float(row["oldbalanceDest"]),
        "newbalanceDest": float(row["newbalanceDest"]),
        "isFraud": int(row["isFraud"])
    }

    producer.send(TOPIC, value=message)

    if i % 5000 == 0:
        print(f"✅ Sent {i}/{len(df)}")

# -----------------------------
# FLUSH & DONE
# -----------------------------
producer.flush()
print("🚀 Finished streaming sampled data to Kafka")

# from kafka import KafkaProducer
# import json
# import time
# import random
# import pandas as pd

# # Load REAL dataset
# df = pd.read_csv("data/processed/spark_sample1.csv")

# producer = KafkaProducer(
#     bootstrap_servers='localhost:9092',
#     value_serializer=lambda v: json.dumps(v).encode('utf-8')
# )

# transaction_types = ["PAYMENT", "TRANSFER", "CASH_OUT", "DEBIT"]

# # 👉 Set how many transactions you want
# NUM_TRANSACTIONS = 20   # change to 100, 500, etc.

# for i , row in range(NUM_TRANSACTIONS):
#     data = {

#         "step": int(row["step"]),
#         "type": row["type"],
#         "amount": float(row["amount"]),
#         "nameOrig": row["nameOrig"],
#         "oldbalanceOrg": float(row["oldbalanceOrg"]),
#         "newbalanceOrig": float(row["newbalanceOrig"]),
#         "nameDest": row["nameDest"],
#         "oldbalanceDest": float(row["oldbalanceDest"]),
#         "newbalanceDest": float(row["newbalanceDest"]),
#         "isFraud": int(row["isFraud"])
#     }
#         # "amount": round(random.uniform(100, 300000), 2),
#         # "type": random.choice(transaction_types),
#         # "oldbalanceOrg": random.uniform(0, 500000),
#         # "newbalanceOrig": random.uniform(0, 500000),
#         # "oldbalanceDest": random.uniform(0, 500000),
#         # "newbalanceDest": random.uniform(0, 500000),
#         # "isFraud": random.choice([0, 1])
#     # }

#     producer.send("transactions", value=data)
#     print(f"Sent {i+1}/{NUM_TRANSACTIONS}:", data)

#     time.sleep(1)

# print("✅ Finished sending transactions")




# from kafka import KafkaProducer
# import json
# import time
# import random

# producer = KafkaProducer(
#     bootstrap_servers='localhost:9092',
#     value_serializer=lambda v: json.dumps(v).encode('utf-8')
# )

# transaction_types = ["PAYMENT", "TRANSFER", "CASH_OUT", "DEBIT"]

# while True:
#     data = {
#         "amount": round(random.uniform(100, 300000), 2),
#         "type": random.choice(transaction_types),
#         "oldbalanceOrig": random.uniform(0, 500000),
#         "newbalanceOrig": random.uniform(0, 500000),
#         "oldbalanceDest": random.uniform(0, 500000),
#         "newbalanceDest": random.uniform(0, 500000),
#         "isFraud": random.choice([0, 1])
#     }

#     producer.send("transactions", value=data)
#     print("Sent:", data)

#     time.sleep(1)




# from kafka import KafkaProducer
# import json
# import time
# import pandas as pd

# # Load sample data
# df = pd.read_csv("data/processed/spark_sample1.csv")

# producer = KafkaProducer(
#     bootstrap_servers='localhost:9092',
#     value_serializer=lambda v: json.dumps(v).encode('utf-8')
# )

# print("🚀 Sending transactions to Kafka...")

# for _, row in df.head(20).iterrows():
#     data = row.to_dict()
#     producer.send("transactions", data)
#     print("Sent:", data["amount"])
#     time.sleep(1)

# producer.close()


# to start kafka server 
# PS C:\WINDOWS\System32> cd "C:\Users\rsanj\Downloads\kafka"
# PS C:\Users\rsanj\Downloads\kafka> .\bin\windows\kafka-server-start.bat config\kraft\server.properties

# Now that the storage is formatted, you can start the Kafka broker with:
# .\bin\windows\kafka-server-start.bat .\config\kraft\server.properties

# .\bin\windows\kafka-server-start.bat .\config\kraft\server.properties

# Open a new terminal and create your topic:
# .\bin\windows\kafka-topics.bat --create --topic test-topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

# Open two separate terminals for producer and consumer:
# # Producer
# .\bin\windows\kafka-console-producer.bat --topic test-topic --bootstrap-server localhost:9092

# # Consumer
# .\bin\windows\kafka-console-consumer.bat --topic test-topic --from-beginning --bootstrap-server localhost:9092

# List existing topics to confirm:
# .\bin\windows\kafka-topics.bat --list --bootstrap-server localhost:9092

# Use the topic with producer and consumer:
# # Producer
# .\bin\windows\kafka-console-producer.bat --topic test-topic --bootstrap-server localhost:9092

# # Consumer
# .\bin\windows\kafka-console-consumer.bat --topic test-topic --from-beginning --bootstrap-server localhost:9092

# If you want to recreate the topic, first delete it:
# .\bin\windows\kafka-topics.bat --delete --topic test-topic --bootstrap-server localhost:9092 

