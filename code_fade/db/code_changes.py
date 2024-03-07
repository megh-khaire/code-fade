from code_fade.db.collections import Collections
from code_fade.db.core import bulk_push


def bulk_push_code_changes(data, chunk_size=100):
    """
    Pushes data in bulk to the 'code_changes' collection.

    :param data: List of dictionaries, where each dictionary represents an author.
    """
    bulk_push(Collections.CODE_CHANGES, data, chunk_size)
