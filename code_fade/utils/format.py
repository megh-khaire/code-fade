from datetime import datetime


def convert_to_iso(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj
