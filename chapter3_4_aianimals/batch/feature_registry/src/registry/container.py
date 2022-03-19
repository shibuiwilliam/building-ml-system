from src.configurations import Configurations
from src.infrastructure.cache import AbstractCache
from src.infrastructure.client.rabbitmq_messaging import RabbitmqMessaging
from src.infrastructure.database import AbstractDatabase
from src.job.animal_feature_initialization_job import AnimalFeatureInitializationJob
from src.job.animal_feature_registration_job import AnimalFeatureRegistrationJob
from src.middleware.logger import configure_logger
from src.repository.animal_feature_repository import AbstractAnimalFeatureRepository, AnimalFeatureRepository
from src.repository.animal_repository import AbstractAnimalRepository, AnimalRepository
from src.service.feature_processing import (
    CategoricalVectorizer,
    DescriptionTokenizer,
    DescriptionVectorizer,
    NameTokenizer,
    NameVectorizer,
)
from src.usecase.animal_feature_usecase import AbstractAnimalFeatureUsecase, AnimalFeatureUsecase

logger = configure_logger(__name__)


class Container(object):
    def __init__(
        self,
        database: AbstractDatabase,
        messaging: RabbitmqMessaging,
        cache: AbstractCache,
        animal_category_vectorizer: CategoricalVectorizer,
        animal_subcategory_vectorizer: CategoricalVectorizer,
        description_tokenizer: DescriptionTokenizer,
        name_tokenizer: NameTokenizer,
        description_vectorizer: DescriptionVectorizer,
        name_vectorizer: NameVectorizer,
    ):
        self.database = database
        self.cache = cache
        self.messaging = messaging
        self.messaging.init_channel()
        self.messaging.create_queue(queue_name=Configurations.animal_feature_registry_queue)

        self.animal_category_vectorizer = animal_category_vectorizer
        self.animal_subcategory_vectorizer = animal_subcategory_vectorizer
        self.description_tokenizer = description_tokenizer
        self.name_tokenizer = name_tokenizer
        self.description_vectorizer = description_vectorizer
        self.name_vectorizer = name_vectorizer

        self.animal_repository: AbstractAnimalRepository = AnimalRepository(database=self.database)
        self.animal_feature_repository: AbstractAnimalFeatureRepository = AnimalFeatureRepository(
            database=self.database
        )

        self.animal_feature_usecase: AbstractAnimalFeatureUsecase = AnimalFeatureUsecase(
            animal_repository=self.animal_repository,
            animal_feature_repository=self.animal_feature_repository,
            messaging=self.messaging,
            cache=self.cache,
            animal_category_vectorizer=self.animal_category_vectorizer,
            animal_subcategory_vectorizer=self.animal_subcategory_vectorizer,
            description_tokenizer=self.description_tokenizer,
            name_tokenizer=self.name_tokenizer,
            description_vectorizer=self.description_vectorizer,
            name_vectorizer=self.name_vectorizer,
        )

        self.animal_feature_initialization_job: AnimalFeatureInitializationJob = AnimalFeatureInitializationJob(
            animal_feature_usecase=self.animal_feature_usecase,
        )
        self.animal_feature_registration_job: AnimalFeatureRegistrationJob = AnimalFeatureRegistrationJob(
            animal_feature_usecase=self.animal_feature_usecase,
            messaging=self.messaging,
        )
