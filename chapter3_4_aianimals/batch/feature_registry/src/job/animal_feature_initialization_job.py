import mlflow
from src.job.abstract_job import AbstractJob
from src.middleware.logger import configure_logger
from src.usecase.animal_feature_usecase import AbstractAnimalFeatureUsecase

logger = configure_logger(__name__)


class AnimalFeatureInitializationJob(AbstractJob):
    def __init__(
        self,
        animal_feature_usecase: AbstractAnimalFeatureUsecase,
    ):
        super().__init__()
        self.animal_feature_usecase = animal_feature_usecase

    def run(self):
        logger.info("run animal feature initialization job")
        response = self.animal_feature_usecase.fit_register_animal_feature()
        mlflow.log_artifact(response.animal_category_vectorizer_file, "animal_category_vectorizer")
        mlflow.log_artifact(response.animal_subcategory_vectorizer_file, "animal_subcategory_vectorizer")
        mlflow.log_artifact(response.description_vectorizer_file, "description_vectorizer")
        mlflow.log_artifact(response.name_vectorizer_file, "name_vectorizer")
