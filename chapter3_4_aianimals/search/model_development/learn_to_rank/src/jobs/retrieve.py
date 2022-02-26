from src.dataset.data_manager import AbstractDBClient, AccessLogRepository
from src.dataset.schema import Action, RawData
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


def retrieve_access_logs(
    db_client: AbstractDBClient,
) -> RawData:
    access_log_repository = AccessLogRepository(db_client=db_client)
    records = access_log_repository.select_all()
    logger.info(f"retrieved: {len(records)} like {records[0]}")
    data = []
    target = []
    for record in records:
        d = dict(
            animal_id=record.animal_id,
            query_phrases=".".join(sorted(record.query_phrases)),
            query_animal_category_id=record.query_animal_category_id,
            query_animal_subcategory_id=record.query_animal_subcategory_id,
            likes=record.likes,
            animal_category_id=record.animal_category_id,
            animal_subcategory_id=record.animal_subcategory_id,
        )
        for i, v in enumerate(record.name_vector):
            d[f"name_vector_{i}"] = v
        for i, v in enumerate(record.description_vector):
            d[f"description_vector_{i}"] = v

        data.append(d)
        if record.action == Action.SELECT.value:
            target.append([1])
        elif record.action == Action.SEE_LONG.value:
            target.append([3])
        elif record.action == Action.LIKE.value:
            target.append([4])
    logger.info(
        f"""
retrieved data
data: {data[0]}
target: {target[0]}
    """
    )
    return RawData(
        data=data,
        target=target,
        keys=list(data[0].keys()),
    )
