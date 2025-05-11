import json
from pymongo import MongoClient
from config import DB_URI, DB_NAME, COLLECTION_NAME

def save_to_db():
    client = MongoClient(DB_URI)
    db = client[DB_NAME]
    col = db[COLLECTION_NAME]
    col.drop()  # Clear old data
    with open("data/processed/clustered_threats.json") as f:
        data = json.load(f)
    col.insert_many(data)
    print("[+] Saved clustered threat data to MongoDB.")

if __name__ == "__main__":
    save_to_db()