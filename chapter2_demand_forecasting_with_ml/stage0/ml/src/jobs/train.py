from dataclasses import dataclass
from typing import Optional, Tuple

import numpy as np
import pandas as pd
from pydantic import BaseModel
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, mean_squared_error
from src.dataset.schema import ITEMS, STORES
from src.middleware.logger import configure_logger
from src.models.base_model import BaseDemandForecastingModel
from src.models.preprocess import DataPreprocessPipeline

logger = configure_logger(name=__name__)


@dataclass
class Evaluation:
    eval_df: pd.DataFrame
    mean_absolute_error: float
    mean_absolute_percentage_error: float
    root_mean_squared_error: float


class Artifact(BaseModel):
    preprocess_file_path: Optional[str]
    model_file_path: Optional[str]


class Trainer(object):
    def __init__(self):
        pass

    def train(
        self,
        model: BaseDemandForecastingModel,
        x_train: pd.DataFrame,
        y_train: pd.DataFrame,
        x_test: pd.DataFrame,
        y_test: pd.DataFrame,
    ):
        model.train(
            x_train=x_train,
            y_train=y_train,
            x_test=x_test,
            y_test=y_test,
        )

    def __organize_eval_df(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        df = df.drop("item_price", axis=1)
        store_condition = [
            (df.store_chiba == 1),
            (df.store_ginza == 1),
            (df.store_kobe == 1),
            (df.store_morioka == 1),
            (df.store_nagoya == 1),
            (df.store_osaka == 1),
            (df.store_sendai == 1),
            (df.store_shinjuku == 1),
            (df.store_ueno == 1),
            (df.store_yokohama == 1),
        ]
        store_values = [
            "chiba",
            "ginza",
            "kobe",
            "morioka",
            "nagoya",
            "osaka",
            "sendai",
            "shinjuku",
            "ueno",
            "yokohama",
        ]

        item_condition = [
            (df.item_apple_juice == 1),
            (df.item_beer == 1),
            (df.item_coffee == 1),
            (df.item_fruit_juice == 1),
            (df.item_milk == 1),
            (df.item_mineral_water == 1),
            (df.item_orange_juice == 1),
            (df.item_soy_milk == 1),
            (df.item_sparkling_water == 1),
            (df.item_sports_drink == 1),
        ]
        item_values = [
            "apple_juice",
            "beer",
            "coffee",
            "fruit_juice",
            "milk",
            "mineral_water",
            "orange_juice",
            "soy_milk",
            "sparkling_water",
            "sports_drink",
        ]
        df["store"] = np.select(store_condition, store_values)
        df["item"] = np.select(item_condition, item_values)
        df = df[["year", "week_of_year", "store", "item"]]
        return df

    def __evaluate(self, df: pd.DataFrame):
        logger.info(
            f"""Evaluations
{df}"""
        )
        logger.info(
            f"""Predicted too high; diff -50
{df[df["diff"] < -50][["store", "item","y_true", "y_pred", "diff"]]}
        """
        )
        logger.info(
            f"""Predicted too low; diff 30
{df[df["diff"] > 30][["store", "item","y_true", "y_pred", "diff"]]}
        """
        )

        for store in STORES:
            _df = df[df["store"] == store]
            _diff = _df["y_true"].sum() - _df["y_pred"].sum()
            logger.info(
                f"""STORE {store}
total diff: {_diff}
average diff: {_diff/10}
            """
            )

        for item in ITEMS:
            _df = df[df["item"] == item]
            _diff = _df["y_true"].sum() - _df["y_pred"].sum()
            logger.info(
                f"""ITEM {item}
total diff: {_diff}
average diff: {_diff/10}
            """
            )

    def evaluate(
        self,
        model: BaseDemandForecastingModel,
        x: pd.DataFrame,
        y: pd.DataFrame,
    ) -> Evaluation:
        predictions = model.predict(x=x)
        eval_df = self.__organize_eval_df(df=x)
        eval_df = pd.concat(
            [eval_df, pd.DataFrame({"y_true": y.sales, "y_pred": predictions})],
            axis=1,
        )
        # eval_df.loc[eval_df["store"] == "morioka", "y_pred"] = eval_df[eval_df["store"] == "morioka"]["y_pred"] - 20
        # eval_df.loc[eval_df["store"] == "ginza", "y_pred"] = eval_df[eval_df["store"] == "ginza"]["y_pred"] + 25
        # eval_df.loc[eval_df["store"] == "shinjuku", "y_pred"] = eval_df[eval_df["store"] == "shinjuku"]["y_pred"] + 30
        # eval_df.loc[eval_df["store"] == "yokohama", "y_pred"] = eval_df[eval_df["store"] == "yokohama"]["y_pred"] + 20
        # eval_df.loc[eval_df["store"] == "osaka", "y_pred"] = eval_df[eval_df["store"] == "osaka"]["y_pred"] + 30
        # eval_df.loc[eval_df["item"] == "milk", "y_pred"] = eval_df[eval_df["item"] == "milk"]["y_pred"] + 40
        # eval_df.loc[eval_df["item"] == "soy_milk", "y_pred"] = eval_df[eval_df["item"] == "soy_milk"]["y_pred"] + 20
        # eval_df.loc[eval_df["item"] == "coffee", "y_pred"] = eval_df[eval_df["item"] == "coffee"]["y_pred"] + 30

        eval_df["diff"] = eval_df["y_true"] - eval_df["y_pred"]
        eval_df["error_rate"] = eval_df["diff"] / eval_df["y_true"]
        self.__evaluate(df=eval_df)

        rmse = mean_squared_error(
            y_true=eval_df.y_true,
            y_pred=eval_df.y_pred,
            squared=False,
        )
        mae = mean_absolute_error(
            y_true=eval_df.y_true,
            y_pred=eval_df.y_pred,
        )
        mape = mean_absolute_percentage_error(
            y_true=eval_df.y_true,
            y_pred=eval_df.y_pred,
        )
        evaluation = Evaluation(
            eval_df=eval_df,
            mean_absolute_error=mae,
            mean_absolute_percentage_error=mape,
            root_mean_squared_error=rmse,
        )
        logger.info(
            f"""
model: {model.name}
mae: {evaluation.mean_absolute_error}
mape: {evaluation.mean_absolute_percentage_error}
rmse: {evaluation.root_mean_squared_error}
            """
        )
        return evaluation

    def train_and_evaluate(
        self,
        model: BaseDemandForecastingModel,
        x_train: pd.DataFrame,
        y_train: pd.DataFrame,
        x_test: pd.DataFrame,
        y_test: pd.DataFrame,
        data_preprocess_pipeline: Optional[DataPreprocessPipeline] = None,
        preprocess_pipeline_file_path: Optional[str] = None,
        save_file_path: Optional[str] = None,
    ) -> Tuple[Evaluation, Artifact]:
        logger.info("start training and evaluation")
        self.train(
            model=model,
            x_train=x_train,
            y_train=y_train,
            x_test=x_test,
            y_test=y_test,
        )
        evaluation = self.evaluate(
            model=model,
            x=x_test,
            y=y_test,
        )

        artifact = Artifact()
        if data_preprocess_pipeline is not None and preprocess_pipeline_file_path is not None:
            artifact.preprocess_file_path = data_preprocess_pipeline.dump_pipeline(
                file_path=preprocess_pipeline_file_path
            )

        if save_file_path is not None:
            artifact.model_file_path = model.save(file_path=save_file_path)

        logger.info("done training and evaluation")
        return evaluation, artifact
