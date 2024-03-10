import os
from urllib.parse import quote_plus

import certifi
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


class MongoDBConnection:
    CLIENT = None

    @staticmethod
    def get_client():
        if MongoDBConnection.CLIENT is None:
            username = quote_plus(os.getenv("USERNAME"))
            password = quote_plus(os.getenv("PASSWORD"))
            cluster = os.getenv("CLUSTER")
            database = os.getenv("DATABASE")
            uri = (
                "mongodb+srv://"
                + username
                + ":"
                + password
                + "@"
                + cluster
                + ".wljazff.mongodb.net/?retryWrites=true&w=majority&appName="
                + database
            )
            MongoDBConnection.CLIENT = MongoClient(uri, tlsCAFile=certifi.where())
        return MongoDBConnection.CLIENT
