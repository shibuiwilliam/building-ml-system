import json
import random
from enum import Enum
from typing import List
from uuid import uuid4


class AnimalSearchSortKey(Enum):
    SCORE = "score"
    LIKE = "like"
    CREATED_AT = "created_at"
    RANDOM = "random"
    LEARN_TO_RANK = "learn_to_rank"
    IMAGE_SIMILARITY = "image_similarity"

    @staticmethod
    def get_list() -> List[str]:
        return [v.value for v in AnimalSearchSortKey.__members__.values()]


def get_uuid() -> str:
    return str(uuid4()).replace("-", "")


def main():
    with open("data/access_logs.json", "r") as f:
        access_logs = json.load(f)

    similar_model_name = get_uuid()
    learn_to_rank_reg = get_uuid()
    learn_to_rank_rank = get_uuid()
    for a in access_logs["access_logs"]:
        search_id = get_uuid()
        model_name = None
        r = random.random()
        if r < 0.3:
            sort_by = AnimalSearchSortKey.SCORE.value
        elif r < 0.4:
            sort_by = AnimalSearchSortKey.LIKE.value
        elif r < 0.7:
            sort_by = AnimalSearchSortKey.CREATED_AT.value
        elif r < 0.75:
            sort_by = AnimalSearchSortKey.RANDOM.value
        elif r < 0.88:
            sort_by = AnimalSearchSortKey.LEARN_TO_RANK.value
            if random.random() < 0.7:
                model_name = learn_to_rank_reg
            else:
                model_name = learn_to_rank_rank
        else:
            sort_by = AnimalSearchSortKey.IMAGE_SIMILARITY.value
            model_name = similar_model_name
        a["search_id"] = search_id
        a["sort_by"] = sort_by
        a["model_name"] = model_name
    with open("data/access_logs.json", "w") as f:
        json.dump(access_logs, f)


if __name__ == "__main__":
    main()
