import os
from datetime import datetime

import hydra
from omegaconf import DictConfig
from src.dataset.data_manager import DATA_SOURCE
from src.dataset.schema import YearAndWeek
from src.jobs.optimize import OptimizerRunner
from src.jobs.predict import Predictor
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
    logger.info(f"os cwd: {cwd}")

    data_source = DATA_SOURCE.value_to_enum(value=cfg.jobs.data.source)
    train_year_and_week = YearAndWeek(
        year=cfg.jobs.data.train.year,
        week_of_year=cfg.jobs.data.train.week,
    )
    test_year_and_week = YearAndWeek(
        year=cfg.jobs.data.test.year,
        week_of_year=cfg.jobs.data.test.week,
    )
    data_preprocess_pipeline = DataPreprocessPipeline()
    data_retriever = DataRetriever()

    raw_df = data_retriever.retrieve_dataset(
        cfg=cfg,
        data_source=data_source,
    )
    xy_train, xy_test = data_retriever.train_test_split(
        raw_df=raw_df,
        train_year_and_week=train_year_and_week,
        test_year_and_week=test_year_and_week,
        data_preprocess_pipeline=data_preprocess_pipeline,
    )
    x_train = xy_train.x
    y_train = xy_train.y
    x_test = xy_test.x
    y_test = xy_test.y

    _model = MODELS.get_model(name=cfg.jobs.model.name)
    model = _model.model(
        early_stopping_rounds=cfg.jobs.model.get("early_stopping_rounds", 200),
        verbose_eval=cfg.jobs.model.get("verbose_eval", 1000),
    )
    if "params" in cfg.jobs.model.keys():
        model.reset_model(params=cfg.jobs.model.params)

    if cfg.jobs.optimize.run:
        metrics = METRICS.get_metrics(name=cfg.jobs.optimize.optuna.metrics)
        optimizer = Optimizer(
            data=x_train,
            target=y_train,
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
                early_stopping_rounds=cfg.jobs.model.get("early_stopping_rounds", 200),
                eval_metric=cfg.jobs.model.get("eval_metrics", "mse"),
                verbose=cfg.jobs.model.get("verbose_eval", 1000),
            ),
        )
        logger.info(f"parameter optimize results: {best_params}")
        model.reset_model(params=best_params)

    if cfg.jobs.train.run:
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_file_path = os.path.join(cwd, f"{model.name}_{now}")
        onnx_file_path = os.path.join(cwd, f"{model.name}_{now}")
        trainer = Trainer()
        trainer.train_and_evaluate(
            model=model,
            x_train=x_train,
            y_train=y_train,
            x_test=x_test,
            y_test=y_test,
            save_file_path=save_file_path,
            onnx_file_path=onnx_file_path,
        )

    if cfg.jobs.predict.run:
        predictor = Predictor()
        target_items = cfg.jobs.data.predict.get("items", "ALL")
        if target_items == "ALL":
            target_items = None

        target_stores = cfg.jobs.data.predict.get("stores", "ALL")
        if target_stores == "ALL":
            target_stores = None

        predictions = predictor.predict(
            model=model,
            data_preprocess_pipeline=data_preprocess_pipeline,
            raw_df=raw_df,
            target_year=cfg.jobs.data.predict.get("year", 2019),
            target_week=cfg.jobs.data.predict.get("week", 50),
            target_items=target_items,
            target_stores=target_stores,
        )
        logger.info(f"predictions: {predictions}")


if __name__ == "__main__":
    main()
