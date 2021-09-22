from datetime import date, datetime
from typing import List, Union

import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from src.models.dataset import DAYS_OF_WEEK, ITEMS, STORES


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

        self.__set_week()
        self.diffs: np.ndarray = self.__set_diffs()
        self.error_rates: np.ndarray = self.__set_error_rate()
        self.date_based_results = self.make_date_based_results()
        self.week_based_results = self.make_week_based_results()

    def __set_week(self):
        for date in self.dates:
            isocalendar = date.isocalendar()
            self.week.append(isocalendar.week)
            self.day_of_week.append(DAYS_OF_WEEK[isocalendar.weekday - 1])

    def get_mse(
        self,
        squared: bool = True,
    ):
        return mean_squared_error(
            self.true_sales,
            self.predicted_sales,
            squared=squared,
        )

    def __set_diffs(self) -> np.ndarray:
        diff = self.true_sales - self.predicted_sales
        return np.abs(diff) if self.absolute else diff

    def __set_error_rate(self) -> np.ndarray:
        return self.diffs / self.true_sales

    def make_date_based_results(self) -> pd.DataFrame:
        df = pd.DataFrame(
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
        df["date"] = pd.to_datetime(df["date"])
        return df

    def make_week_based_results(self) -> pd.DataFrame:
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
        df = pd.DataFrame(
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
        return df
