import os

from dotenv import load_dotenv

from code_fade.db.collections import Collections
from code_fade.db.connection import MongoDBConnection

load_dotenv()

DATABASE = os.getenv("DATABASE")


def create_indexes():
    client = MongoDBConnection.get_client()
    db = client[DATABASE]
    authors_collection = db[Collections.AUTHORS]
    authors_collection.create_index([("emails", 1), ("repo", 1)])
    lines_collection = db[Collections.LINES]
    lines_collection.create_index([("added_by", 1), ("repo", 1)])


def bulk_push(collection, data, chunk_size=100):
    client = MongoDBConnection.get_client()
    db = client[DATABASE]
    db_collection = db[collection]
    for i in range(0, len(data), chunk_size):
        chunk = data[i : i + chunk_size]
        db_collection.insert_many(chunk)


def find_one(collection, query):
    client = MongoDBConnection.get_client()
    db = client[DATABASE]
    db_collection = db[collection]
    return db_collection.find_one(query)


def delete_many(collection, query):
    client = MongoDBConnection.get_client()
    db = client[DATABASE]
    db_collection = db[collection]
    db_collection.delete_many(query)
