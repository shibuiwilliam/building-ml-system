import hashlib


def get_md5_hash(string: str) -> str:
    return hashlib.md5(string.encode()).hexdigest()
