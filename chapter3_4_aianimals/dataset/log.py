import json
import random
from datetime import date, datetime, time, timedelta
from time import sleep
from typing import List, Optional

import httpx
from numpy import sort


def json_serialize(obj):
    if isinstance(obj, (datetime, date, time)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def get_token(
    user: str,
    password: str,
):
    data = {
        "handle_name": user,
        "password": password,
    }
    print(f"data: {data}")
    with httpx.Client(
        timeout=30.0,
        transport=httpx.HTTPTransport(retries=3),
    ) as c:
        r = c.post(
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
            },
            data=json.dumps(data, default=json_serialize),
            url="http://localhost:8000/v0/user/login",
        )
    if r.status_code != 200:
        return None
    token = r.json()
    return token["token"]


def get_metadata(token: str):
    with httpx.Client(
        timeout=30.0,
        transport=httpx.HTTPTransport(retries=3),
    ) as c:
        r = c.get(
            headers={
                "accept": "application/json",
                "token": token,
            },
            url="http://localhost:8000/v0/metadata",
        )
    if r.status_code != 200:
        return None
    return r.json()


def get_search(
    token: str,
    phrases: List[str],
    animal_category_name_ja: Optional[str],
    animal_subcategory_name_ja: Optional[str],
    sort_by: str = "score",
):
    data = {
        "phrases": phrases,
        "sort_by": sort_by,
    }
    if animal_category_name_ja is not None:
        data["animal_category_name_ja"] = animal_category_name_ja
    if animal_subcategory_name_ja is not None:
        data["animal_subcategory_name_ja"] = animal_subcategory_name_ja
    with httpx.Client(
        timeout=30.0,
        transport=httpx.HTTPTransport(retries=3),
    ) as c:
        r = c.post(
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
                "token": token,
            },
            data=json.dumps(data, default=json_serialize),
            params={
                "limit": 200,
                "offset": 0,
            },
            url="http://localhost:8000/v0/animal/search",
        )
    if r.status_code != 200:
        return None
    return r.json()


def make_access(
    animal_id: str,
    token: str,
    phrases: List[str],
    action: str,
    created_at: datetime,
    animal_category_id: Optional[str] = None,
    animal_subcategory_id: Optional[str] = None,
):
    data = dict(
        phrases=phrases,
        action=action,
        created_at=created_at,
        animal_id=animal_id,
    )
    if animal_category_id is not None:
        data["animal_category_id"] = animal_category_id
    if animal_subcategory_id is not None:
        data["animal_subcategory_id"] = animal_subcategory_id
    with httpx.Client(
        timeout=30.0,
        transport=httpx.HTTPTransport(retries=3),
    ) as c:
        c.post(
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
                "token": token,
            },
            data=json.dumps(data, default=json_serialize),
            url="http://localhost:8000/v0/access_log",
        )


def make_like(
    animal_id: str,
    token: str,
    phrases: List[str],
    created_at: datetime,
    animal_category_id: Optional[str] = None,
    animal_subcategory_id: Optional[str] = None,
):
    data = {"animal_id": animal_id}
    with httpx.Client(
        timeout=30.0,
        transport=httpx.HTTPTransport(retries=3),
    ) as c:
        r = c.post(
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
                "token": token,
            },
            data=json.dumps(data, default=json_serialize),
            url="http://localhost:8000/v0/like",
        )
        if r.status_code != 200:
            return None
        make_access(
            animal_id=animal_id,
            token=token,
            phrases=phrases,
            action="like",
            created_at=created_at,
            animal_category_id=animal_category_id,
            animal_subcategory_id=animal_subcategory_id,
        )


def main():
    print("START!!!!!!!")
    vocabs = {
        5: [
            "ねこ",
            "猫",
            "ネコ",
            "犬",
            "いぬ",
            "イヌ",
        ],
        4: [
            "かわいい",
            "可愛い",
            "かっこいい",
            "カッコいい",
            "癒やし",
            "萌え",
        ],
        3: [
            "キュート",
            "キャワイイ",
            "カワイイ",
            "クール",
            "カッコイイ",
            "イケメン",
            "めろめろ",
            "もふもふ",
            "ドキドキ",
            "ニャーニャー",
            "わんわん",
            "好き",
        ],
        2: [
            "外",
            "散歩",
            "寝る",
            "美しい",
            "猫缶",
            "ごはん",
            "こたつ",
            "大好き",
            "家族",
            "ラブリー",
            "ペット",
            "最高",
            "公園",
            "近所",
            "キュンキュン",
            "名前",
            "ふみふみ",
            "モフモフ",
        ],
        1: [
            "らんらん",
            "てくてく",
            "偉そう",
            "一番",
            "ワイルド",
            "気分",
            "みーみー",
            "ミーミー",
            "にーにー",
            "バフバフ",
            "わうわう",
            "鳴く",
            "カリカリ",
            "ボール",
            "キャットフード",
            "ドッグフード",
            "ダンボール",
            "ペットショップ",
            "魚",
            "肉",
            "ごはん",
            "散歩",
            "山",
            "川",
            "午前",
            "午後",
            "朝",
            "夜",
            "遊び",
            "寝る",
            "天使",
            "可愛すぎ",
            "かわいすぎ",
            "アイドル",
            "推し",
            "家族",
            "職場",
            "学校",
            "道端",
            "春",
            "夏",
            "秋",
            "冬",
            "アビシニアン",
            "チワワ",
            "ブリティッシュショートヘア",
            "メインクーン",
            "ポメラニアン",
            "ラグドール",
            "ロシアンブルー",
            "セントバーナード",
            "シバイヌ",
            "ヨークシャーテリア",
            "シャム",
            "パグ",
            "ペルシャ",
            "ブルドッグ",
        ],
    }

    with open("user.json", "r") as f:
        users = json.load(f)

    metadata = None
    i = 0
    for u, (_, user) in enumerate(users.items()):
        j = 0
        if random.random() < 0.1:
            continue
        z = random.choice([0.85, 0.9, 0.95, 0.99])
        y = random.choice([0.6, 0.5, 0.3, 0.1])
        print(f"USER: {u} / {len(users)}: {user} {z} {y}")
        token = get_token(
            user=user["handle_name"],
            password=user["password"],
        )
        if metadata is None:
            metadata = get_metadata(token=token)
            animal_categories = metadata["animal_category"]
            animal_subcategories = metadata["animal_subcategory"]
            animal_categories.pop(0)
            animal_subcategories.pop(0)
        date = datetime.strptime(user["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
        while random.random() < z:
            print(f"j: {j}")
            if j >= 100:
                break
            j += 1
            if j > 3:
                z *= z
            phrases = []
            animal_category = None
            animal_subcategory = None
            if random.random() < 0.3:
                animal_category = random.choice(animal_categories)
            if random.random() < 0.2:
                animal_subcategory = random.choice(animal_subcategories)
                if animal_category is not None and animal_subcategory["animal_category_id"] != animal_category["id"]:
                    if random.random() < 0.5:
                        animal_category = None
                    else:
                        animal_subcategory = None
            length = 0
            lr = random.random()
            if lr < 0.02:
                length = 4
            elif lr < 0.05:
                length = 3
            elif lr < 0.2:
                length = 2
            elif lr < 0.5:
                length = 1
            for _ in range(length):
                lr = random.random()
                if lr < 0.05:
                    phrases.append(random.choice(vocabs[1]))
                elif lr < 0.1:
                    phrases.append(random.choice(vocabs[2]))
                elif lr < 0.25:
                    phrases.append(random.choice(vocabs[3]))
                elif lr < 0.5:
                    phrases.append(random.choice(vocabs[4]))
                else:
                    if animal_category is None and animal_subcategory is None:
                        phrases.append(random.choice(vocabs[5]))

            sr = random.random()
            if sr < 0.3:
                sort_by = "score"
            elif sr < 0.4:
                sort_by = "like"
            elif sr < 0.6:
                sort_by = "created_at"
            else:
                sort_by = "random"
            animals = get_search(
                token=token,
                phrases=phrases,
                animal_category_name_ja=animal_category["name_ja"] if animal_category is not None else None,
                animal_subcategory_name_ja=animal_subcategory["name_ja"] if animal_subcategory is not None else None,
                sort_by=sort_by,
            )
            k = 0
            for a in animals["results"]:
                if k >= random.choice([5, 10, 20]):
                    break
                k += 1
                animal_date = datetime.strptime(a["created_at"].replace("+00:00", ""), "%Y-%m-%dT%H:%M:%S.%f")
                if date < animal_date:
                    x = y * 1.3
                else:
                    x = y
                ddd = max(animal_date, date)
                sec = random.randrange(100 * 24 * 60 * 60)
                ddd = ddd + timedelta(seconds=sec)
                if a["score"] > 100:
                    if random.random() < 0.5:
                        i += 1
                        make_access(
                            animal_id=a["id"],
                            token=token,
                            phrases=phrases,
                            action="select",
                            created_at=ddd,
                            animal_category_id=animal_category["id"] if animal_category is not None else None,
                            animal_subcategory_id=animal_subcategory["id"] if animal_subcategory is not None else None,
                        )
                        if random.random() < 0.3:
                            i += 1
                            make_access(
                                animal_id=a["id"],
                                token=token,
                                phrases=phrases,
                                action="see_long",
                                created_at=ddd,
                                animal_category_id=animal_category["id"] if animal_category is not None else None,
                                animal_subcategory_id=animal_subcategory["id"]
                                if animal_subcategory is not None
                                else None,
                            )
                    if random.random() < 0.7:
                        i += 1
                        make_like(
                            animal_id=a["id"],
                            token=token,
                            phrases=phrases,
                            created_at=ddd,
                            animal_category_id=animal_category["id"] if animal_category is not None else None,
                            animal_subcategory_id=animal_subcategory["id"] if animal_subcategory is not None else None,
                        )
                else:
                    s = 1.0 + (float(a["score"]) / 100)
                    sx = x * s
                    if sx >= 1.0:
                        sx = 1.0
                    if random.random() < sx:
                        i += 1
                        make_access(
                            animal_id=a["id"],
                            token=token,
                            phrases=phrases,
                            action="select",
                            created_at=ddd,
                            animal_category_id=animal_category["id"] if animal_category is not None else None,
                            animal_subcategory_id=animal_subcategory["id"] if animal_subcategory is not None else None,
                        )
                        if random.random() < sx:
                            i += 1
                            make_access(
                                animal_id=a["id"],
                                token=token,
                                phrases=phrases,
                                action="see_long",
                                created_at=ddd,
                                animal_category_id=animal_category["id"] if animal_category is not None else None,
                                animal_subcategory_id=animal_subcategory["id"]
                                if animal_subcategory is not None
                                else None,
                            )
                    if random.random() < sx:
                        i += 1
                        make_like(
                            animal_id=a["id"],
                            token=token,
                            phrases=phrases,
                            created_at=ddd,
                            animal_category_id=animal_category["id"] if animal_category is not None else None,
                            animal_subcategory_id=animal_subcategory["id"] if animal_subcategory is not None else None,
                        )
                if i % 100 == 0:
                    sleep(10)
                    print(f"REGISTERED: {i}")
    print("DONE!!!!!!!")


if __name__ == "__main__":
    main()
