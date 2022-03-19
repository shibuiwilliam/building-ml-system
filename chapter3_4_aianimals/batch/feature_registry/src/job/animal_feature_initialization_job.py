import mlflow
from src.job.abstract_job import AbstractJob
from src.middleware.logger import configure_logger
from src.usecase.animal_feature_usecase import AbstractAnimalFeatureUsecase
from src.request_object.animal_feature import AnimalFeatureInitializeRequest

logger = configure_logger(__name__)


class AnimalFeatureInitializationJob(AbstractJob):
    def __init__(
        self,
        animal_feature_usecase: AbstractAnimalFeatureUsecase,
    ):
        super().__init__()
        self.animal_feature_usecase = animal_feature_usecase

    def run(
        self,
        mlflow_experiment_id: int,
        mlflow_run_id: str,
    ):
        logger.info("run animal feature initialization job")
        response = self.animal_feature_usecase.fit_register_animal_feature(
            request=AnimalFeatureInitializeRequest(
                mlflow_experiment_id=mlflow_experiment_id,
                mlflow_run_id=mlflow_run_id,
            )
        )
        if response is not None:
            mlflow.log_artifact(response.animal_category_vectorizer_file, "animal_category_vectorizer")
            mlflow.log_artifact(response.animal_subcategory_vectorizer_file, "animal_subcategory_vectorizer")
            mlflow.log_artifact(response.description_vectorizer_file, "description_vectorizer")
            mlflow.log_artifact(response.name_vectorizer_file, "name_vectorizer")
