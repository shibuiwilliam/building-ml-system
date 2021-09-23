from datetime import date, datetime
from typing import List, Optional, Union

import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from src.models.dataset import DAYS_OF_WEEK, ITEMS, STORES
from src.utils.logger import configure_logger

logger = configure_logger(__name__)


class Evaluator(object):
    def __init__(
        self,
        dates: List[Union[date, datetime]],
        stores: List[str],
        items: List[str],
        true_sales: np.ndarray,
        predicted_sales: np.ndarray,
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
        return mean_squared_error(
            self.true_sales,
            self.predicted_sales,
            squared=squared,
        )

    def __set_week(self):
        for date in self.dates:
            isocalendar = date.isocalendar()
            self.week.append(isocalendar.week)
            self.day_of_week.append(DAYS_OF_WEEK[isocalendar.weekday - 1])

    def __set_diffs(self):
        diff = self.true_sales - self.predicted_sales
        self.diffs = np.abs(diff) if self.absolute else diff

    def __set_error_rate(self):
        self.__set_diffs()
        self.error_rates = self.diffs / self.true_sales

    def __make_date_based_results(self):
        self.date_based_results = pd.DataFrame(
            {
                "dates": self.dates,
                "week": self.week,
                "day_of_week": self.day_of_week,
                "stores": self.stores,
                "items": self.items,
                "true_sales": self.true_sales,
                "predicted_sales": self.predicted_sales,
                "diffs": self.diffs,
                "error_rates": self.error_rates,
            }
        )
        self.date_based_results["date"] = pd.to_datetime(self.date_based_results["date"])

    def __make_week_based_results(self):
        weeks = set(self.week)
        _weeks = []
        _stores = []
        _items = []
        _true_sales = []
        _predicted_sales = []
        _diffs = []
        _error_rates = []
        for store in STORES:
            for item in ITEMS:
                for week in weeks:
                    _df = self.date_based_results[self.date_based_results["store"] == store][
                        self.date_based_results["item"] == item
                    ][self.date_based_results["week"] == week]
                    _weeks.append(week)
                    _stores.append(store)
                    _items.append(item)
                    _true_sales.append(_df.true_sales.sum())
                    _predicted_sales.append(_df.predicted_sales.sum())
                    _diffs.append(_df.diffs.sum())
                    _error_rates.append(_df.error_rates.sum())
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
        if self.date_based_results is not None:
            self.date_based_results.to_csv(file_path)

    def save_week_based_results(self, file_path: str):
        if self.week_based_results is not None:
            self.week_based_results.to_csv(file_path)
