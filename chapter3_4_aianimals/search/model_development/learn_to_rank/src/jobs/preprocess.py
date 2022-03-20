import random
from typing import Dict, List, Optional, Tuple

from pydantic import BaseModel
from src.dataset.schema import Data
from src.middleware.logger import configure_logger
from src.models.preprocess import CategoricalVectorizer, NumericalMinMaxScaler
from src.dataset.schema import RawData, SplitData
from sklearn.model_selection import train_test_split

logger = configure_logger(name=__name__)


def make_query_id(
    phrases: str,
    animal_category_id: Optional[int],
    animal_subcategory_id: Optional[int],
) -> str:
    return f"{phrases}_{animal_category_id}_{animal_subcategory_id}"


def random_split(
    raw_data: RawData,
    test_size: float = 0.3,
) -> SplitData:
    logger.info("random split")
    x_train, x_test, y_train, y_test = train_test_split(
        raw_data.data,
        raw_data.target,
        test_size=test_size,
        shuffle=True,
    )
    return SplitData(
        x_train=x_train,
        x_test=x_test,
        y_train=y_train,
        y_test=y_test,
        q_train=None,
        q_test=None,
    )


def split_by_qid(
    raw_data: RawData,
    test_size: float = 0.3,
) -> SplitData:
    logger.info("split by qid")
    x_train = []
    y_train = []
    x_test = []
    y_test = []
    q_train = []
    q_test = []
    _data: Dict[str, List[Tuple]] = {}
    for r, t in zip(raw_data.data, raw_data.target):
        qid = make_query_id(
            phrases=r.query_phrases,
            animal_category_id=r.query_animal_category_id,
            animal_subcategory_id=r.query_animal_subcategory_id,
        )
        if qid in _data.keys():
            _data[qid].append((r, t))
        else:
            _data[qid] = [(r, t)]
    for _, rts in _data.items():
        if len(rts) == 1:
            x_train.append(rts[0][0])
            y_train.append(rts[0][1])
            q_train.append(1)
        else:
            l = len(rts)
            if l > 10000:
                l = 10000
            _rts = random.sample(rts, l)
            train_size = int(l * (1 - test_size))
            for i, rt in enumerate(_rts):
                if i < train_size:
                    x_train.append(rt[0])
                    y_train.append(rt[1])
                else:
                    x_test.append(rt[0])
                    y_test.append(rt[1])
            q_train.append(train_size)
            q_test.append(l - train_size)
    return SplitData(
        x_train=x_train,
        x_test=x_test,
        y_train=y_train,
        y_test=y_test,
        q_train=q_train,
        q_test=q_test,
    )


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

        likes_train = likes_scaler.fit_transform(x=[[d.likes] for d in x_train]).tolist()
        query_phrases_train = (
            query_phrase_encoder.fit_transform(x=[[d.query_phrases] for d in x_train]).toarray().tolist()
        )
        query_animal_category_ids_train = (
            query_animal_category_id_encoder.fit_transform(x=[[d.query_animal_category_id] for d in x_train])
            .toarray()
            .tolist()
        )
        query_animal_subcategory_ids_train = (
            query_animal_subcategory_id_encoder.fit_transform(x=[[d.query_animal_subcategory_id] for d in x_train])
            .toarray()
            .tolist()
        )

        likes_test = likes_scaler.transform(x=[[d.likes] for d in x_test]).tolist()
        query_phrases_test = query_phrase_encoder.transform(x=[[d.query_phrases] for d in x_test]).toarray().tolist()
        query_animal_category_ids_test = (
            query_animal_category_id_encoder.transform(x=[[d.query_animal_category_id] for d in x_test])
            .toarray()
            .tolist()
        )
        query_animal_subcategory_ids_test = (
            query_animal_subcategory_id_encoder.transform(x=[[d.query_animal_subcategory_id] for d in x_test])
            .toarray()
            .tolist()
        )

        _x_train = []
        for l, qp, qac, qas, v in zip(
            likes_train,
            query_phrases_train,
            query_animal_category_ids_train,
            query_animal_subcategory_ids_train,
            x_train,
        ):
            _x_train.append(
                [
                    *l,
                    *qp,
                    *qac,
                    *qas,
                    *v.feature_vector.animal_category_vector,
                    *v.feature_vector.animal_subcategory_vector,
                    *v.feature_vector.name_vector,
                    *v.feature_vector.description_vector,
                ]
            )

        _x_test = []
        for l, qp, qac, qas, v in zip(
            likes_test,
            query_phrases_test,
            query_animal_category_ids_test,
            query_animal_subcategory_ids_test,
            x_test,
        ):
            _x_test.append(
                [
                    *l,
                    *qp,
                    *qac,
                    *qas,
                    *v.feature_vector.animal_category_vector,
                    *v.feature_vector.animal_subcategory_vector,
                    *v.feature_vector.name_vector,
                    *v.feature_vector.description_vector,
                ]
            )

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
