import random
import string
import uuid


def random_str(n: int = 10):
    randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
    return "".join(randlst)


def get_uuid() -> str:
    return str(uuid.uuid4()).replace("-", "")


def hiragana_to_katakana(hiragana: str) -> str:
    return "".join(
        [
            chr(n + 96) if (12352 < n and n < 12439) or n == 12445 or n == 12446 else chr(n)
            for n in [ord(c) for c in hiragana]
        ]
    )


def katakana_to_hiragana(katakana: str):
    return "".join(
        [
            chr(n - 96) if (12448 < n and n < 12535) or n == 12541 or n == 12542 else chr(n)
            for n in [ord(c) for c in katakana]
        ]
    )
