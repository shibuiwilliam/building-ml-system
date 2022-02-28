from typing import List, Optional, Tuple
from pydantic import BaseModel
from src.middleware.logger import configure_logger
from src.dataset.schema import Data
from src.models.preprocess import NumericalMinMaxScaler, CategoricalVectorizer

logger = configure_logger(name=__name__)


class PreprocessedData(BaseModel):
    x_train: List[List[float]]
    y_train: List[int]
    x_test: List[List[float]]
    y_test: List[int]
    q_train: Optional[List[int]]
    q_test: Optional[List[int]]


class PreprocessArtifact(BaseModel):
    likes_scaler_save_file_path: Optional[str]
    query_phrase_encoder_save_file_path: Optional[str]
    query_animal_category_id_encoder_save_file_path: Optional[str]
    query_animal_subcategory_id_encoder_save_file_path: Optional[str]


class Preprocess(object):
    def __init__(self):
        pass

    def run(
        self,
        likes_scaler: NumericalMinMaxScaler,
        query_phrase_encoder: CategoricalVectorizer,
        query_animal_category_id_encoder: CategoricalVectorizer,
        query_animal_subcategory_id_encoder: CategoricalVectorizer,
        likes_scaler_save_file_path: str,
        query_phrase_encoder_save_file_path: str,
        query_animal_category_id_encoder_save_file_path: str,
        query_animal_subcategory_id_encoder_save_file_path: str,
        x_train: List[Data],
        y_train: List[int],
        x_test: List[Data],
        y_test: List[int],
        q_train: Optional[List[int]] = None,
        q_test: Optional[List[int]] = None,
    ) -> Tuple[PreprocessedData, PreprocessArtifact]:
        logger.info(
            f"""
data before preprocess
x_train: {len(x_train)}
y_train: {len(y_train)}
x_test: {len(x_test)}
y_test: {len(y_test)}
q_train: {sum(q_train) if q_train is not None else None}
q_test: {sum(q_test) if q_test is not None else None}
        """
        )

        likes_train = [[d.likes] for d in x_train]
        query_phrases_train = [[d.query_phrases] for d in x_train]
        query_animal_category_ids_train = [[d.query_animal_category_id] for d in x_train]
        query_animal_subcategory_ids_train = [[d.query_animal_subcategory_id] for d in x_train]

        likes_test = [[d.likes] for d in x_test]
        query_phrases_test = [[d.query_phrases] for d in x_test]
        query_animal_category_ids_test = [[d.query_animal_category_id] for d in x_test]
        query_animal_subcategory_ids_test = [[d.query_animal_subcategory_id] for d in x_test]

        _likes_train = likes_scaler.fit_transform(x=likes_train).tolist()
        _query_phrases_train = query_phrase_encoder.fit_transform(x=query_phrases_train).toarray().tolist()
        _query_animal_category_ids_train = (
            query_animal_category_id_encoder.fit_transform(x=query_animal_category_ids_train).toarray().tolist()
        )
        _query_animal_subcategory_ids_train = (
            query_animal_subcategory_id_encoder.fit_transform(x=query_animal_subcategory_ids_train).toarray().tolist()
        )

        _likes_test = likes_scaler.transform(x=likes_test).tolist()
        _query_phrases_test = query_phrase_encoder.transform(x=query_phrases_test).toarray().tolist()
        _query_animal_category_ids_test = (
            query_animal_category_id_encoder.transform(x=query_animal_category_ids_test).toarray().tolist()
        )
        _query_animal_subcategory_ids_test = (
            query_animal_subcategory_id_encoder.transform(x=query_animal_subcategory_ids_test).toarray().tolist()
        )

        _x_train = []
        for l, qp, qac, qas, v in zip(
            _likes_train,
            _query_phrases_train,
            _query_animal_category_ids_train,
            _query_animal_subcategory_ids_train,
            x_train,
        ):
            _x_train.append([*l, *qp, *qac, *qas, *v.feature_vector])

        _x_test = []
        for l, qp, qac, qas, v in zip(
            _likes_test,
            _query_phrases_test,
            _query_animal_category_ids_test,
            _query_animal_subcategory_ids_test,
            x_test,
        ):
            _x_test.append([*l, *qp, *qac, *qas, *v.feature_vector])

        logger.info(
            f"""
data after preprocess
x_train: {len(_x_train)}
y_train: {len(y_train)}
x_test: {len(_x_test)}
y_test: {len(y_test)}
q_train: {sum(q_train) if q_train is not None else None}
q_test: {sum(q_test) if q_test is not None else None}
        """
        )

        likes_scaler_save_file_path = likes_scaler.save(file_path=likes_scaler_save_file_path)
        query_phrase_encoder_save_file_path = query_phrase_encoder.save(file_path=query_phrase_encoder_save_file_path)
        query_animal_category_id_encoder_save_file_path = query_animal_category_id_encoder.save(
            file_path=query_animal_category_id_encoder_save_file_path
        )
        query_animal_subcategory_id_encoder_save_file_path = query_animal_subcategory_id_encoder.save(
            file_path=query_animal_subcategory_id_encoder_save_file_path
        )

        data = PreprocessedData(
            x_train=_x_train,
            y_train=y_train,
            x_test=_x_test,
            y_test=y_test,
            q_train=q_train,
            q_test=q_test,
        )
        artifact = PreprocessArtifact(
            likes_scaler_save_file_path=likes_scaler_save_file_path,
            query_phrase_encoder_save_file_path=query_phrase_encoder_save_file_path,
            query_animal_category_id_encoder_save_file_path=query_animal_category_id_encoder_save_file_path,
            query_animal_subcategory_id_encoder_save_file_path=query_animal_subcategory_id_encoder_save_file_path,
        )
        return data, artifact
