import uuid


def get_uuid() -> str:
    return str(uuid.uuid4()).replace("-", "")


def parse_query(query) -> str:
    while True:
        query = query.replace("\n", " ").strip()
        if "\n" not in query:
            break
    while True:
        query = query.replace("  ", " ")
        if "  " not in query:
            return query
