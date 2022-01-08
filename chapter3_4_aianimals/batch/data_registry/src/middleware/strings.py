import random
import string
import uuid


def random_str(n: int = 10):
    randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
    return "".join(randlst)


def get_uuid() -> str:
    return str(uuid.uuid4()).replace("-", "")
