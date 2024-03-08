import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from pymongo import MongoClient

from code_fade.db.collections import Collections

load_dotenv()

DATABASE = os.getenv("DATABASE")


class MongoDBConnection:
    def __init__(self):
        self.username = quote_plus(os.getenv("USERNAME"))
        self.password = quote_plus(os.getenv("PASSWORD"))
        self.cluster = os.getenv("CLUSTER")
        self.uri = (
            "mongodb+srv://"
            + self.username
            + ":"
            + self.password
            + "@"
            + self.cluster
            + ".wljazff.mongodb.net/?retryWrites=true&w=majority&appName="
            + DATABASE
        )
        self.client = None

    def __enter__(self):
        self.client = MongoClient(self.uri)
        return self.client

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()


def create_indexes():
    with MongoDBConnection() as client:
        db = client[DATABASE]
        authors_collection = db[Collections.AUTHORS]
        authors_collection.create_index([("emails", 1), ("repo", 1)])
        lines_collection = db[Collections.LINES]
        lines_collection.create_index([("added_by", 1), ("repo", 1)])


def bulk_push(collection, data, chunk_size=100):
    with MongoDBConnection() as client:
        db = client[DATABASE]
        db_collection = db[collection]
        for i in range(0, len(data), chunk_size):
            chunk = data[i : i + chunk_size]
            db_collection.insert_many(chunk)


def find_one(collection, query):
    with MongoDBConnection() as client:
        db = client[DATABASE]
        db_collection = db[collection]
        return db_collection.find_one(query)


def delete_many(collection, query):
    with MongoDBConnection() as client:
        db = client[DATABASE]
        db_collection = db[collection]
        db_collection.delete_many(query)
