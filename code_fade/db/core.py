import os

from dotenv import load_dotenv
from pymongo import MongoClient

from code_fade.db.collections import Collections

load_dotenv()


def get_database():
    CONNECTION_STRING = os.getenv("MONGO_URI")
    return MongoClient(CONNECTION_STRING)


def create_indexes():
    db = get_database()
    authors_collection = db[Collections.AUTHORS]
    authors_collection.create_index([("email", 1)], unique=True)


def bulk_push(collection, data, chunk_size=100):
    """
    Pushes data in bulk to the 'authors' collection.

    :param data: List of dictionaries, where each dictionary represents an author.
    """
    try:
        db = get_database()
        db_collection = db[collection]
        for i in range(0, len(data), chunk_size):
            chunk = data[i : i + chunk_size]
            db_collection.insert_many(chunk)
    except Exception as e:
        print(f"An error occurred: {e}")
