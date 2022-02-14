from src.dataset.data_manager import AbstractDBClient, AccessLogRepository
from src.dataset.schema import Action, RawData
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


def retrieve_access_logs(
    db_client: AbstractDBClient,
) -> RawData:
    access_log_repository = AccessLogRepository(db_client=db_client)
    records = access_log_repository.select_all()
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
    return RawData(
        data=data,
        target=target,
    )
