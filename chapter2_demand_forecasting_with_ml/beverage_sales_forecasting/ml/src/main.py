import os
from datetime import datetime

import hydra
import mlflow
from omegaconf import DictConfig
from src.dataset.data_manager import DATA_SOURCE
from src.dataset.schema import YearAndWeek
from src.jobs.optimize import OptimizerRunner
from src.jobs.predict import Predictor
from src.jobs.register import DataRegister
from src.jobs.retrieve import DataRetriever
from src.jobs.train import Trainer
from src.middleware.logger import configure_logger
from src.models.models import MODELS
from src.models.preprocess import DataPreprocessPipeline, WeekBasedSplit
from src.optimizer.optimizer import Optimizer
from src.optimizer.schema import DIRECTION, METRICS

logger = configure_logger(__name__)

DATE_FORMAT = "%Y-%m-%d"


@hydra.main(
    config_path="/opt/hydra",
    config_name="default",
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
    with mlflow.start_run(run_name=run_name):
        data_source = DATA_SOURCE.value_to_enum(value=cfg.jobs.data.source)
        train_year_and_week = YearAndWeek(
            year=cfg.jobs.data.train.year,
            week_of_year=cfg.jobs.data.train.week,
        )
        test_year_and_week = YearAndWeek(
            year=cfg.jobs.data.test.year,
            week_of_year=cfg.jobs.data.test.week,
        )

        date_from = cfg.jobs.data.target_data.get("date_from", None)
        if date_from is not None:
            date_from = datetime.strptime(date_from, "%Y-%m-%d").date()
        date_to = cfg.jobs.data.target_data.get("date_to", None)
        if date_to is not None:
            date_to = datetime.strptime(date_to, "%Y-%m-%d").date()

        data_preprocess_pipeline = DataPreprocessPipeline()
        data_retriever = DataRetriever()
        raw_df = data_retriever.retrieve_dataset(
            file_path=cfg.jobs.data.path,
            date_from=date_from,
            date_to=date_to,
            item=cfg.jobs.data.target_data.item,
            store=cfg.jobs.data.target_data.store,
            region=cfg.jobs.data.target_data.region,
            data_source=data_source,
        )
        xy_train, xy_test = data_retriever.train_test_split(
            raw_df=raw_df,
            train_year_and_week=train_year_and_week,
            test_year_and_week=test_year_and_week,
            data_preprocess_pipeline=data_preprocess_pipeline,
        )

        mlflow.log_param("target_date_date_from", date_from)
        mlflow.log_param("target_date_date_to", date_to)
        mlflow.log_param("target_date_item", cfg.jobs.data.target_data.item)
        mlflow.log_param("target_date_store", cfg.jobs.data.target_data.store)
        mlflow.log_param("target_date_region", cfg.jobs.data.target_data.region)

        _model = MODELS.get_model(name=cfg.jobs.model.name)
        model = _model.model(
            early_stopping_rounds=cfg.jobs.model.params.early_stopping_rounds,
            eval_metrics=cfg.jobs.model.params.eval_metrics,
            verbose_eval=cfg.jobs.model.params.verbose_eval,
        )
        if "params" in cfg.jobs.model.keys():
            model.reset_model(params=cfg.jobs.model.params)

        if cfg.jobs.optimize.run:
            metrics = METRICS.get_metrics(name=cfg.jobs.optimize.optuna.metrics)
            optimizer = Optimizer(
                data=xy_train.x,
                target=xy_train.y,
                direction=DIRECTION.MINIMIZE,
                cv=WeekBasedSplit(
                    n_splits=5,
                    gap=2,
                    min_train_size_rate=0.8,
                    columns=data_preprocess_pipeline.preprocessed_columns,
                    types=data_preprocess_pipeline.preprocessed_types,
                ),
            )
            optimize_runner = OptimizerRunner(
                model=model,
                optimizer=optimizer,
            )
            best_params = optimize_runner.optimize(
                params=cfg.jobs.optimize.optuna.light_gbm.parameters,
                n_trials=cfg.jobs.optimize.optuna.n_trials,
                n_jobs=cfg.jobs.optimize.optuna.n_jobs,
                metrics=metrics,
                fit_params=dict(
                    early_stopping_rounds=cfg.jobs.model.params.early_stopping_rounds,
                    eval_metric=cfg.jobs.model.params.eval_metrics,
                    verbose=cfg.jobs.model.params.verbose_eval,
                ),
            )
            logger.info(f"parameter optimize results: {best_params}")
            model.reset_model(params=best_params)

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

            target_items = cfg.jobs.data.predict.items
            if target_items == "ALL":
                target_items = None

            target_stores = cfg.jobs.data.predict.stores
            if target_stores == "ALL":
                target_stores = None

            predictions = predictor.predict(
                model=model,
                data_preprocess_pipeline=data_preprocess_pipeline,
                raw_df=raw_df,
                target_year=cfg.jobs.data.predict.year,
                target_week=cfg.jobs.data.predict.week,
                target_items=target_items,
                target_stores=target_stores,
            )
            logger.info(f"predictions: {predictions}")
            if cfg.jobs.predict.register:
                data_register = DataRegister()
                prediction_file_path = os.path.join(cwd, f"{model.name}_{now}")
                data_register.register(
                    predictions=predictions,
                    data_source=data_source,
                    prediction_file_path=prediction_file_path,
                )
            mlflow.log_param("predict_year", cfg.jobs.data.predict.year)
            mlflow.log_param("predict_week", cfg.jobs.data.predict.week)
            mlflow.log_param("predict_items", target_items)
            mlflow.log_param("predict_stores", target_stores)

        mlflow.log_artifact(os.path.join(cwd, ".hydra/config.yaml"))
        mlflow.log_artifact(os.path.join(cwd, ".hydra/hydra.yaml"))
        mlflow.log_artifact(os.path.join(cwd, ".hydra/overrides.yaml"))

        mlflow.log_param("train_year", cfg.jobs.data.train.year)
        mlflow.log_param("train_week", cfg.jobs.data.train.week)
        mlflow.log_param("test_year", cfg.jobs.data.test.year)
        mlflow.log_param("test_week", cfg.jobs.data.test.week)
        mlflow.log_param("model", model.name)
        mlflow.log_params(model.params)


if __name__ == "__main__":
    main()
