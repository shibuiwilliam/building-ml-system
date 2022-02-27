from src.dataset.data_manager import AbstractDBClient, AccessLogRepository, AbstractCache, FeatureCacheRepository
from src.dataset.schema import Action, RawData, Data
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


def retrieve_access_logs(
    db_client: AbstractDBClient,
    cache: AbstractCache,
) -> RawData:
    access_log_repository = AccessLogRepository(db_client=db_client)
    records = access_log_repository.select_all()
    ids = list(set([f"{r.animal_id}_feature" for r in records]))
    logger.info(f"retrieved: {len(records)} like {records[0]}")
    feature_cache_repository = FeatureCacheRepository(cache=cache)
    features = feature_cache_repository.get_features_by_keys(keys=ids)
    data = []
    target = []
    i = 1000
    for record in records:
        d = Data(
            animal_id=record.animal_id,
            query_phrases=".".join(sorted(record.query_phrases)),
            query_animal_category_id=record.query_animal_category_id,
            query_animal_subcategory_id=record.query_animal_subcategory_id,
            likes=record.likes,
            feature_vector=features[f"{record.animal_id}_feature"],
        )

        data.append(d)
        if record.action == Action.SELECT.value:
            target.append(1)
        elif record.action == Action.SEE_LONG.value:
            target.append(3)
        elif record.action == Action.LIKE.value:
            target.append(4)
        i -= 1
        if i == 0:
            logger.info(f"organized {len(data)} data")
            i = 1000

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
    )
