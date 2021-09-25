import json
import os
from datetime import datetime
from typing import Optional, Tuple
from uuid import uuid4

import click
from src.dataset.data_retriever import DataRetriever
from src.jobs.predict import PredictionJob
from src.jobs.train import TrainJob
from src.models.models import MODELS
from src.models.preprocess import DataPreprocessPipeline
from src.predict.predictor import OnnxPredictor
from src.utils.logger import configure_logger

logger = configure_logger(__name__)

DATE_FORMAT = "%Y-%m-%d"


@click.command(name="demand forecasting")
@click.option(
    "--data_file_path",
    type=str,
    default=None,
    required=False,
    help="data path",
)
@click.option(
    "--prediction_file_path",
    type=str,
    default=None,
    required=False,
    help="prediction target path",
)
@click.option(
    "--data_manager_api",
    type=str,
    default=None,
    required=False,
    help="data manager api endpoint",
)
@click.option(
    "--model_name",
    type=str,
    default="light_gbm_regression",
    required=True,
    help="model name",
)
@click.option(
    "--save_file_directory",
    type=str,
    default="/tmp",
    required=True,
    help="save result directory",
)
@click.option(
    "--onnx_file_path",
    type=str,
    default=None,
    required=False,
    help="pretrained onnx model file path",
)
@click.option(
    "--pretrained_model_path",
    type=str,
    default=None,
    required=False,
    help="pretrained model file path",
)
@click.option(
    "--fitted_preprocess_file_path",
    type=str,
    default=None,
    required=False,
    help="already fitted preprocess pipeline file path",
)
@click.option(
    "--store",
    "-s",
    type=str,
    required=False,
    multiple=True,
    help="store names to target; not specified = all; multiple specification allowed",
)
@click.option(
    "--item",
    "-i",
    type=str,
    required=False,
    multiple=True,
    help="item names to target; not specified = all; multiple specification allowed",
)
@click.option(
    "--train_start_date",
    type=str,
    required=False,
    help=f"train start date; format {DATE_FORMAT}",
)
@click.option(
    "--train_end_date",
    type=str,
    required=False,
    help=f"train end date; format {DATE_FORMAT}",
)
@click.option(
    "--test_start_date",
    type=str,
    required=False,
    help=f"test start date; format {DATE_FORMAT}",
)
@click.option(
    "--test_end_date",
    type=str,
    required=False,
    help=f"test end date; format {DATE_FORMAT}",
)
@click.option(
    "--predict_start_date",
    type=str,
    required=False,
    help=f"predict start date; format {DATE_FORMAT}",
)
@click.option(
    "--predict_end_date",
    type=str,
    required=False,
    help=f"predict end date; format {DATE_FORMAT}",
)
@click.option(
    "--experiment_param_file_path",
    type=str,
    required=False,
    help=f"path to experiment params",
)
@click.option(
    "--train_param_file_path",
    type=str,
    required=False,
    help=f"path to train params",
)
@click.option(
    "--retrieve_data",
    is_flag=True,
    help="run data retrieval",
)
@click.option(
    "--run_experiment",
    is_flag=True,
    help="run experiment",
)
@click.option(
    "--run_train",
    is_flag=True,
    help="run train",
)
@click.option(
    "--run_prediction",
    is_flag=True,
    help="run prediction",
)
def main(
    model_name: str,
    save_file_directory: str = "/tmp",
    data_file_path: Optional[str] = None,
    prediction_file_path: Optional[str] = None,
    data_manager_api: Optional[str] = None,
    onnx_file_path: Optional[str] = None,
    pretrained_model_path: Optional[str] = None,
    fitted_preprocess_file_path: Optional[str] = None,
    store: Tuple = tuple(),
    item: Tuple = tuple(),
    train_start_date: Optional[str] = None,
    train_end_date: Optional[str] = None,
    test_start_date: Optional[str] = None,
    test_end_date: Optional[str] = None,
    predict_start_date: Optional[str] = None,
    predict_end_date: Optional[str] = None,
    experiment_param_file_path: Optional[str] = None,
    train_param_file_path: Optional[str] = None,
    retrieve_data: bool = False,
    run_experiment: bool = False,
    run_train: bool = False,
    run_prediction: bool = False,
):
    logger.info(
        f"""
PARAMETERS:
    model_name: {model_name}
    save_file_directory:    {save_file_directory}
    data_file_path: {data_file_path}
    prediction_file_path:   {prediction_file_path}
    data_manager_api:   {data_manager_api}
    onnx_file_path: {onnx_file_path}
    pretrained_model_path:  {pretrained_model_path}
    fitted_preprocess_file_path:    {fitted_preprocess_file_path}
    store:  {store}
    item:   {item}
    train_start_date:   {train_start_date}
    train_end_date: {train_end_date}
    test_start_date:    {test_start_date}
    test_end_date:  {test_end_date}
    predict_start_date: {predict_start_date}
    predict_end_date:   {predict_end_date}
    experiment_param_file_path: {experiment_param_file_path}
    train_param_file_path: {train_param_file_path}
    retrieve_data:  {retrieve_data}
    run_experiment: {run_experiment}
    run_train:  {run_train}
    run_prediction: {run_prediction}
    """
    )
    _train_start_date = datetime.strptime(train_start_date, DATE_FORMAT) if train_start_date is not None else None
    _train_end_date = datetime.strptime(train_end_date, DATE_FORMAT) if train_end_date is not None else None
    _test_start_date = datetime.strptime(test_start_date, DATE_FORMAT) if test_start_date is not None else None
    _test_end_date = datetime.strptime(test_end_date, DATE_FORMAT) if test_end_date is not None else None
    _predict_start_date = datetime.strptime(predict_start_date, DATE_FORMAT) if predict_start_date is not None else None
    _predict_end_date = datetime.strptime(predict_end_date, DATE_FORMAT) if predict_end_date is not None else None

    data_retriever = DataRetriever(api_endpoint=data_manager_api)

    preprocess_pipeline = DataPreprocessPipeline()
    if fitted_preprocess_file_path is not None:
        preprocess_pipeline.load_pipeline(file_path=fitted_preprocess_file_path)

    meta_model = MODELS.get_value(name=model_name)
    if meta_model is None:
        raise ValueError
    model = meta_model.model()
    if pretrained_model_path is not None:
        model.load(file_path=pretrained_model_path)

    experiment_params = meta_model.params
    if experiment_param_file_path is not None:
        with open(experiment_param_file_path, "r") as f:
            experiment_params = json.load(f)

    train_params = meta_model.params
    if train_param_file_path is not None:
        with open(train_param_file_path, "r") as f:
            train_params = json.load(f)

    uuid = str(uuid4()).replace("-", "")[:6]
    base_directory_name = f"records_{uuid}"
    save_directory = os.path.join(save_file_directory, base_directory_name)
    os.makedirs(save_directory, exist_ok=True)
    with open(os.path.join(save_directory, "params.json"), "w") as f:
        json.dump(
            {
                "model_name": model_name,
                "save_file_directory": save_file_directory,
                "data_file_path": data_file_path,
                "prediction_file_path": prediction_file_path,
                "onnx_file_path": onnx_file_path,
                "pretrained_model_path": pretrained_model_path,
                "fitted_preprocess_file_path": fitted_preprocess_file_path,
                "store": store,
                "item": item,
                "train_start_date": train_start_date,
                "train_end_date": train_end_date,
                "test_start_date": test_start_date,
                "test_end_date": test_end_date,
                "predict_start_date": predict_start_date,
                "predict_end_date": predict_end_date,
                "experiment_param_file_path": experiment_param_file_path,
                "train_param_file_path": train_param_file_path,
                "run_experiment": run_experiment,
                "run_train": run_train,
                "run_prediction": run_prediction,
            },
            f,
        )

    stores = list(store) if len(store) > 0 else None
    items = list(item) if len(item) > 0 else None

    train_job = TrainJob(
        data_file_path=data_file_path,
        preprocess_pipeline=preprocess_pipeline,
        model=model,
        stores=stores,
        items=items,
        save_file_directory=save_directory,
    )

    if run_experiment:
        if _train_start_date is None or _train_end_date is None or _test_start_date is None or _test_end_date is None:
            raise ValueError
        train_job.experiment(
            train_start_date=_train_start_date,
            train_end_date=_train_end_date,
            test_start_date=_test_start_date,
            test_end_date=_test_end_date,
            model_params=experiment_params,
        )

    if run_train:
        if _train_start_date is None or _train_end_date is None:
            raise ValueError
        train_job.train(
            train_start_date=_train_start_date,
            train_end_date=_train_end_date,
            model_params=train_params,
        )

    if run_prediction:
        preprocess_pipeline = train_job.preprocess_pipeline
        preprocess_pipeline.include_target = False

        if train_job.onnx_file_path != "":
            onnx_file_path = train_job.onnx_file_path

        predictor = OnnxPredictor(
            file_path=onnx_file_path,
            preprocess_pipeline=preprocess_pipeline,
        )
        prediction_job = PredictionJob(
            prediction_file_path=prediction_file_path,
            predictor=predictor,
            stores=stores,
            items=items,
            save_file_directory=save_directory,
        )
        prediction_job.predict(
            predict_start_date=_predict_start_date,
            predict_end_date=_predict_end_date,
        )


if __name__ == "__main__":
    main()
