import os
from datetime import date, datetime, timedelta

import hydra
import mlflow
from omegaconf import DictConfig
from src.configurations import Configurations
from src.dataset.data_manager import DBDataManager
from src.dataset.schema import YearAndWeek
from src.jobs.predict import Predictor
from src.jobs.register import DataRegister
from src.jobs.retrieve import DataRetriever
from src.jobs.train import Trainer
from src.middleware.db_client import PostgreSQLClient
from src.middleware.logger import configure_logger
from src.models.models import MODELS
from src.models.preprocess import DataPreprocessPipeline

logger = configure_logger(__name__)

DATE_FORMAT = "%Y-%m-%d"


@hydra.main(
    config_path="/opt/hydra",
    config_name=Configurations.target_config_name,
)
def main(cfg: DictConfig):
    logger.info("start ml...")
    logger.info(f"config: {cfg}")
    cwd = os.getcwd()
    run_name = "-".join(cwd.split("/")[-2:])

    logger.info(f"current working directory: {cwd}")
    logger.info(f"run_name: {run_name}")

    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000"))
    mlflow.set_experiment(cfg.name)
    with mlflow.start_run(run_name=run_name) as run:
        db_client = PostgreSQLClient()
        db_data_manager = DBDataManager(db_client=db_client)
        data_retriever = DataRetriever(db_data_manager=db_data_manager)

        earliest_sales_date = data_retriever.retrieve_item_sales_earliest_date()
        if earliest_sales_date is None:
            raise Exception("no sales record available")

        latest_sales_date = data_retriever.retrieve_item_sales_latest_date()
        if latest_sales_date is None:
            raise Exception("no sales record available")

        train_year = earliest_sales_date.isocalendar().year
        train_week = earliest_sales_date.isocalendar().week
        train_end_date = latest_sales_date + timedelta(days=-14)
        train_end_year = train_end_date.isocalendar().year
        train_end_week = train_end_date.isocalendar().week
        test_year = latest_sales_date.isocalendar().year
        test_week = latest_sales_date.isocalendar().week

        train_year_and_week = YearAndWeek(
            year=train_year,
            week_of_year=train_week,
        )
        train_end_year_and_week = YearAndWeek(
            year=train_end_year,
            week_of_year=train_end_week,
        )
        test_year_and_week = YearAndWeek(
            year=test_year,
            week_of_year=test_week,
        )

        data_preprocess_pipeline = DataPreprocessPipeline()
        raw_df = data_retriever.retrieve_dataset(
            date_from=earliest_sales_date,
            date_to=latest_sales_date,
            item=Configurations.target_item,
            store=Configurations.target_store,
            region=Configurations.target_region,
        )
        xy_train, xy_test = data_retriever.train_test_split(
            raw_df=raw_df,
            train_year_and_week=train_year_and_week,
            train_end_year_and_week=train_end_year_and_week,
            test_year_and_week=test_year_and_week,
            data_preprocess_pipeline=data_preprocess_pipeline,
        )

        mlflow.log_param("target_date_date_from", earliest_sales_date)
        mlflow.log_param("target_date_date_to", latest_sales_date)
        mlflow.log_param("target_date_item", Configurations.target_item)
        mlflow.log_param("target_date_store", Configurations.target_store)
        mlflow.log_param("target_date_region", Configurations.target_region)

        _model = MODELS.get_model(name=cfg.jobs.model.name)
        model = _model.model(
            early_stopping_rounds=cfg.jobs.model.params.early_stopping_rounds,
            eval_metrics=cfg.jobs.model.params.eval_metrics,
            verbose_eval=cfg.jobs.model.params.verbose_eval,
        )
        if "params" in cfg.jobs.model.keys():
            model.reset_model(params=cfg.jobs.model.params)

        if cfg.jobs.train.run:
            now = datetime.now().strftime("%Y%m%d_%H%M%S")
            preprocess_pipeline_file_path = os.path.join(cwd, f"{model.name}_{now}")
            save_file_path = os.path.join(cwd, f"{model.name}_{now}")
            onnx_file_path = os.path.join(cwd, f"{model.name}_{now}")
            trainer = Trainer()
            evaluation, artifact = trainer.train_and_evaluate(
                model=model,
                x_train=xy_train.x,
                y_train=xy_train.y,
                x_test=xy_test.x,
                y_test=xy_test.y,
                data_preprocess_pipeline=data_preprocess_pipeline,
                preprocess_pipeline_file_path=preprocess_pipeline_file_path,
                save_file_path=save_file_path,
                onnx_file_path=onnx_file_path,
            )
            mlflow.log_metrics(evaluation.dict())
            mlflow.log_artifact(artifact.preprocess_file_path)
            mlflow.log_artifact(artifact.model_file_path)
            mlflow.log_artifact(artifact.onnx_file_path)

        if cfg.jobs.predict.run:
            predictor = Predictor()
            next_date = latest_sales_date + timedelta(days=1)
            prediction_target_year = Configurations.target_year
            prediction_target_week = Configurations.target_week
            if prediction_target_year is None or prediction_target_week is None:
                prediction_latest_date = data_retriever.retrieve_prediction_latest_date()
                if prediction_latest_date is None:
                    raise ValueError
                next_prediction_latest_date = prediction_latest_date + timedelta(days=1)
                prediction_target_year = next_prediction_latest_date.isocalendar().year
                prediction_target_week = next_prediction_latest_date.isocalendar().week

            target_date = date.fromisocalendar(
                year=prediction_target_year,
                week=prediction_target_week,
                day=7,
            )

            data_to_be_predicted_df = data_retriever.retrieve_prediction_data(
                date_from=next_date,
                date_to=target_date,
            )

            target_items = Configurations.target_items
            if target_items[0] == "ALL":
                target_items = None

            target_stores = Configurations.target_stores
            if target_stores[0] == "ALL":
                target_stores = None

            predictions = predictor.predict(
                model=model,
                data_preprocess_pipeline=data_preprocess_pipeline,
                previous_df=raw_df,
                data_to_be_predicted_df=data_to_be_predicted_df,
                target_year=prediction_target_year,
                target_week=prediction_target_week,
                target_items=target_items,
                target_stores=target_stores,
            )
            logger.info(f"predictions: {predictions}")
            if cfg.jobs.predict.register:
                data_register = DataRegister(db_data_manager=db_data_manager)
                data_register.register(
                    predictions=predictions,
                    mlflow_experiment_id=run.info.experiment_id,
                    mlflow_run_id=run.info.run_id,
                )
            mlflow.log_param("predict_year", prediction_target_year)
            mlflow.log_param("predict_week", prediction_target_week)
            mlflow.log_param("predict_items", target_items)
            mlflow.log_param("predict_stores", target_stores)

        mlflow.log_artifact(os.path.join(cwd, ".hydra/config.yaml"))
        mlflow.log_artifact(os.path.join(cwd, ".hydra/hydra.yaml"))
        mlflow.log_artifact(os.path.join(cwd, ".hydra/overrides.yaml"))

        mlflow.log_param("train_year", train_year)
        mlflow.log_param("train_week", train_week)
        mlflow.log_param("test_year", test_year)
        mlflow.log_param("test_week", test_week)
        mlflow.log_param("model", model.name)
        mlflow.log_params(model.params)


if __name__ == "__main__":
    main()
