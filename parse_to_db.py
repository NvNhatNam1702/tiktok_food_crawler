from numpy._core import records
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()


client = MongoClient(os.environ["MONGODB"])
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client["text_db"]
collection = db["text"]
def parse_to_mongo(input_dir):
    len_data = len(os.listdir(input_dir))
    if len_data == 0:
        print(f"no data in {input_dir}")
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            file_path = os.path.join(input_dir, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    element = {"filename": file_path, "text": content}
                    collection.insert_one(element)
            except Exception as e:
                print(f"error during parse to mongo:{e}")
    print("done inserting")


parse_to_mongo("/home/nampc/code/personal/tiktok/cleaned_text/")
