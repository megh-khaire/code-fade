import code_fade.db.core as db
from code_fade.db.collections import Collections


def bulk_push_authors(data, chunk_size=100):
    db.bulk_push(Collections.AUTHORS, data, chunk_size)


def fetch_author(repo_name, email):
    return db.find_one(
        Collections.AUTHORS, {"repo": repo_name, "emails": {"$in": [email]}}
    )


def delete_all_repo_authors(repo_name):
    db.delete_many(Collections.AUTHORS, {"repo": repo_name})
