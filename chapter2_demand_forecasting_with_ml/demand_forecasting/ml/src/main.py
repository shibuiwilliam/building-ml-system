import os
from datetime import datetime

import hydra
import pandas as pd
from omegaconf import DictConfig
from src.dataset.data_manager import DATA_SOURCE, load_df_from_csv
from src.dataset.schema import BASE_SCHEMA
from src.jobs.optimize import OptimizerRunner
from src.jobs.train import Trainer
from src.middleware.logger import configure_logger
from src.models.models import MODELS
from src.models.preprocess import DataPreprocessPipeline, WeekBasedSplit
from src.optimizer.optimizer import DIRECTION, Optimizer

logger = configure_logger(__name__)

DATE_FORMAT = "%Y-%m-%d"


@hydra.main(
    config_path="/opt/hydra",
    config_name="default",
)
def main(cfg: DictConfig):
    logger.info(f"config: {cfg}")
    cwd = os.getcwd()
    logger.info(f"os cwd: {cwd}")

    data_source = DATA_SOURCE.value_to_enum(value=cfg.jobs.data.source)
    if data_source == DATA_SOURCE.LOCAL:
        raw_df = load_df_from_csv(file_path=cfg.jobs.data.path)
    else:
        raise ValueError

    logger.info(
        f"""
train from: {cfg.jobs.data.train.year_from} to {cfg.jobs.data.test.year} {cfg.jobs.data.test.week-2}
test: year {cfg.jobs.data.test.year} week {cfg.jobs.data.test.week}
                """
    )

    raw_df["date"] = pd.to_datetime(raw_df["date"])
    raw_df = BASE_SCHEMA.validate(raw_df)
    logger.info(
        f"""
raw_df columns: {raw_df.columns}
raw_df shape: {raw_df.shape}
"""
    )

    data_preprocess_pipeline = DataPreprocessPipeline()

    weekly_df = data_preprocess_pipeline.preprocess(x=raw_df)
    weekly_train_df = weekly_df[
        ((weekly_df.year >= cfg.jobs.data.train.year_from) & (weekly_df.year < cfg.jobs.data.test.year))
        | ((weekly_df.year == cfg.jobs.data.test.year) & (weekly_df.week_of_year <= cfg.jobs.data.test.week - 2))
    ].reset_index(drop=True)
    weekly_test_df = weekly_df[
        (weekly_df.year == cfg.jobs.data.test.year) & (weekly_df.week_of_year == cfg.jobs.data.test.week)
    ].reset_index(drop=True)
    logger.info(
        f"""
weekly train df columns: {weekly_train_df.columns}
weekly train df shape: {weekly_train_df.shape}
weekly test df columns: {weekly_test_df.columns}
weekly test df shape: {weekly_test_df.shape}
"""
    )

    preprocessed_train_df = data_preprocess_pipeline.fit_transform(x=weekly_train_df)
    preprocessed_test_df = data_preprocess_pipeline.transform(x=weekly_test_df)
    logger.info(
        f"""
preprocessed train df columns: {preprocessed_train_df.columns}
preprocessed train df shape: {preprocessed_train_df.shape}
preprocessed test df columns: {preprocessed_test_df.columns}
preprocessed test df shape: {preprocessed_test_df.shape}
"""
    )

    x_train = preprocessed_train_df[data_preprocess_pipeline.preprocessed_columns].drop(
        ["sales", "store", "item"], axis=1
    )
    y_train = preprocessed_train_df["sales"]
    x_test = preprocessed_test_df[data_preprocess_pipeline.preprocessed_columns].drop(
        ["sales", "store", "item"], axis=1
    )
    y_test = preprocessed_test_df["sales"]
    logger.info(
        f"""
x_train shape: {x_train.shape}
y_train shape: {y_train.shape}
x_test shape: {x_test.shape}
y_test shape: {y_test.shape}
"""
    )

    _model = MODELS.get_model(name=cfg.jobs.model.name)
    model = _model.model(
        early_stopping_rounds=cfg.jobs.model.get("early_stopping_rounds", 200),
        eval_metrics=cfg.jobs.model.get("eval_metrics", "mse"),
        verbose_eval=cfg.jobs.model.get("verbose_eval", 1000),
    )
    if "params" in cfg.jobs.model.keys():
        model.reset_model(params=cfg.jobs.model.params)

    if cfg.jobs.search.run:
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
            scorings={"neg_mean_squared_error": "neg_mean_squared_error"},
        )
        optimize_runner = OptimizerRunner(
            model=model,
            optimizer=optimizer,
        )
        best_params = optimize_runner.optimize(
            params=cfg.jobs.search.optuna.light_gbm.parameters,
            n_trials=cfg.jobs.search.optuna.n_trials,
            n_jobs=cfg.jobs.search.optuna.n_jobs,
            scoring="test_neg_mean_squared_error",
            fit_params=dict(
                eval_set=[(x_test, y_test)],
                early_stopping_rounds=cfg.jobs.model.get("early_stopping_rounds", 200),
                eval_metric=cfg.jobs.model.get("eval_metrics", "mse"),
                verbose=cfg.jobs.model.get("verbose_eval", 1000),
            ),
        )
        logger.info(f"parameter search results: {best_params}")
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


if __name__ == "__main__":
    main()
