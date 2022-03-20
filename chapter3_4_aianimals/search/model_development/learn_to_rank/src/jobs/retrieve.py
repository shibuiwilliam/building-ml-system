from src.dataset.data_manager import AbstractCache, AbstractDBClient, AccessLogRepository, FeatureCacheRepository
from src.dataset.schema import Action, Data, FeatureVector, RawData
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


def make_cache_key(
    animal_id: str,
    feature_mlflow_experiment_id: int,
    feature_mlflow_run_id: str,
) -> str:
    return f"animal_feature_{animal_id}_{feature_mlflow_experiment_id}_{feature_mlflow_run_id}"


def retrieve_access_logs(
    feature_mlflow_experiment_id: int,
    feature_mlflow_run_id: str,
    db_client: AbstractDBClient,
    cache: AbstractCache,
) -> RawData:
    access_log_repository = AccessLogRepository(db_client=db_client)
    records = access_log_repository.select_all()
    ids = list(
        set(
            [
                make_cache_key(
                    animal_id=r.animal_id,
                    feature_mlflow_experiment_id=feature_mlflow_experiment_id,
                    feature_mlflow_run_id=feature_mlflow_run_id,
                )
                for r in records
            ]
        )
    )
    logger.info(f"retrieved: {len(records)} like {records[0]}")
    feature_cache_repository = FeatureCacheRepository(cache=cache)
    features = feature_cache_repository.get_features_by_keys(keys=ids)
    data = []
    target = []
    i = 1000
    for record in records:
        cache_key = make_cache_key(
            animal_id=record.animal_id,
            feature_mlflow_experiment_id=feature_mlflow_experiment_id,
            feature_mlflow_run_id=feature_mlflow_run_id,
        )
        feature_vector = features.get(cache_key, None)
        if feature_vector is None:
            logger.info(f"skip {record.id} for lack of cache: {cache_key}")
            continue
        d = Data(
            animal_id=record.animal_id,
            query_phrases=".".join(sorted(record.query_phrases)),
            query_animal_category_id=record.query_animal_category_id,
            query_animal_subcategory_id=record.query_animal_subcategory_id,
            likes=record.likes,
            feature_vector=FeatureVector(
                animal_category_vector=feature_vector["animal_category_vector"],
                animal_subcategory_vector=feature_vector["animal_subcategory_vector"],
                name_vector=feature_vector["name_vector"],
                description_vector=feature_vector["description_vector"],
            ),
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
