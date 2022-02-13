from typing import List, Optional, Tuple

import pandas as pd
from src.dataset.data_manager import AbstractDBClient, AccessLogRepository
from src.dataset.schema import Action
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


def make_query_id(
    phrases: str,
    animal_category_id: Optional[int],
    animal_subcategory_id: Optional[int],
) -> str:
    return f"{phrases}_{animal_category_id}_{animal_subcategory_id}"


def retrieve_access_logs(
    db_client: AbstractDBClient,
) -> Tuple[pd.DataFrame, List[List[int]], List[str]]:
    access_log_repository = AccessLogRepository(db_client=db_client)
    records = access_log_repository.select_all()
    data = []
    target = []
    qids = []
    for record in records:
        qid = make_query_id(
            phrases=".".join(sorted(record.query_phrases)),
            animal_category_id=record.query_animal_category_id,
            animal_subcategory_id=record.query_animal_subcategory_id,
        )
        qids.append(qid)
        d = dict(
            animal_id=record.animal_id,
            query_phrases=".".join(sorted(record.query_phrases)),
            query_animal_category_id=record.query_animal_category_id,
            query_animal_subcategory_id=record.query_animal_subcategory_id,
            likes=record.likes,
            animal_category_id=record.animal_category_id,
            animal_subcategory_id=record.animal_subcategory_id,
            name=record.name,
            description=record.description,
        )
        data.append(d)
        if record.action == Action.SELECT:
            target.append([1])
        elif record.action == Action.SEE_LONG:
            target.append([3])
        elif record.action == Action.LIKE:
            target.append([4])
    df = pd.DataFrame(data)
    return df, target, qids
