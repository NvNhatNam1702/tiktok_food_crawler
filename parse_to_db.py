from numpy._core import records
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
df = pd.read_csv("/home/nampc/code/personal/tiktok/price.csv")

records = df.to_dict(orient="records")

client = MongoClient(os.environ["MONGODB"])
db = client["price_db"]
collection = db["prices"]

if records:
    collection.insert_many(records)
    print("success")
else:
    print("no data")
