from dotenv import load_dotenv
from pymongo import MongoClient
import os
from langchain_core.documents import Document

load_dotenv()

# 1. Connect and Load everything from your collection
connection_string = (os.environ["MONGODB"],)
client = MongoClient(connection_string)
db = client["food_analysis_db_attemp2"]
collection = db["json_result"]

# Parse the raw_documents
documents = []

for doc in collection.find({}):
    food_list = doc.get("foods")
    items = food_list.get("items", [])
    for food in items:
        text = (
            f"{food.get('food_name')} costs {food.get('price')} "
            f"and is located at {food.get('location')}."
        )

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "food_name": food.get("food_name"),
                    "price": food.get("price"),
                    "location": food.get("location"),
                    "filename": doc.get("filename"),
                },
            )
        )


if __name__ == "__main__":
    print(documents)
    print(documents[0])
