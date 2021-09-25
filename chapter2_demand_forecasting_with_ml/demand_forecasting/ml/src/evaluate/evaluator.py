from typing import List, Optional, Union

import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from src.dataset.schema import DAYS_OF_WEEK
from src.utils.logger import configure_logger

logger = configure_logger(__name__)


class Evaluator(object):
    def __init__(
        self,
        dates: pd.Series,
        stores: pd.Series,
        items: pd.Series,
        true_sales: Union[np.ndarray, pd.Series],
        predicted_sales: Union[np.ndarray, pd.Series],
        absolute: bool = False,
    ):
        self.dates = dates
        self.week: List[int] = []
        self.day_of_week: List[str] = []
        self.stores = stores
        self.items = items
        self.true_sales = true_sales
        self.predicted_sales = predicted_sales
        self.absolute = absolute
        self.diffs: Optional[np.ndarray] = None
        self.error_rates: Optional[np.ndarray] = None
        self.date_based_results: Optional[pd.DataFrame] = None
        self.week_based_results: Optional[pd.DataFrame] = None

        self.__set_week()
        self.__set_diffs()
        self.__set_error_rate()
        self.__make_date_based_results()
        self.__make_week_based_results()

    def get_mse(
        self,
        squared: bool = True,
    ):
        mse = mean_squared_error(
            self.true_sales,
            self.predicted_sales,
            squared=squared,
        )
        logger.info(f"mean squared error with squared={squared}: {mse}")
        return mse

    def __set_week(self):
        for date in self.dates:
            isocalendar = date.isocalendar()
            self.week.append(isocalendar.week)
            self.day_of_week.append(DAYS_OF_WEEK[isocalendar.weekday - 1])

    def __set_diffs(self):
        diffs = self.true_sales - self.predicted_sales
        self.diffs = abs(diffs) if self.absolute else diffs

    def __set_error_rate(self):
        self.__set_diffs()
        self.error_rates = self.diffs / self.true_sales

    def __make_date_based_results(self):
        self.date_based_results = pd.DataFrame(
            {
                "dates": self.dates,
                "weeks": self.week,
                "day_of_week": self.day_of_week,
                "stores": self.stores,
                "items": self.items,
                "true_sales": self.true_sales,
                "predicted_sales": self.predicted_sales,
                "diffs": self.diffs,
                "error_rates": self.error_rates,
            }
        )
        self.date_based_results["dates"] = pd.to_datetime(self.date_based_results["dates"])

    def __make_week_based_results(self):
        _weeks = []
        _stores = []
        _items = []
        _true_sales = []
        _predicted_sales = []
        _diffs = []
        _error_rates = []
        for store in set(self.stores):
            for item in set(self.items):
                for week in set(self.week):
                    _df = self.date_based_results[self.date_based_results["stores"] == store][
                        self.date_based_results["items"] == item
                    ][self.date_based_results["weeks"] == week]
                    _weeks.append(week)
                    _stores.append(store)
                    _items.append(item)
                    _true_sales.append(_df.true_sales.sum())
                    _predicted_sales.append(_df.predicted_sales.sum())
                    _diff = _df.true_sales.sum() - _df.predicted_sales.sum()
                    if self.absolute:
                        _diff = abs(_diff)
                    _diffs.append(_diff)
                    _error_rate = _diff / _df.true_sales.sum()
                    _error_rates.append(_error_rate)
        self.week_based_results = pd.DataFrame(
            {
                "weeks": _weeks,
                "stores": _stores,
                "items": _items,
                "true_sales": _true_sales,
                "predicted_sales": _predicted_sales,
                "diffs": _diffs,
                "error_rates": _error_rates,
            }
        )

    def save_date_based_results(self, file_path: str):
        logger.info(f"save daily based dataframe to csv: {file_path}")
        if self.date_based_results is not None:
            self.date_based_results.to_csv(file_path, index=False)

    def save_week_based_results(self, file_path: str):
        logger.info(f"save weekly based dataframe to csv: {file_path}")
        if self.week_based_results is not None:
            self.week_based_results.to_csv(file_path, index=False)
