import logging
from abc import ABC, abstractmethod
from typing import List, Optional

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from view_model import AbstractAnimalViewModel, AbstractViolationTypeViewModel, AbstractViolationViewModel


class BaseView(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)


class AbstractViolationListView(ABC):
    def __init__(
        self,
        animal_view_model: AbstractAnimalViewModel,
        violation_type_view_model: AbstractViolationTypeViewModel,
        violation_view_model: AbstractViolationViewModel,
    ):
        self.animal_view_model = animal_view_model
        self.violation_type_view_model = violation_type_view_model
        self.violation_view_model = violation_view_model

    @abstractmethod
    def build(self):
        raise NotImplementedError


class ViolationListView(BaseView, AbstractViolationListView):
    def __init__(
        self,
        animal_view_model: AbstractAnimalViewModel,
        violation_type_view_model: AbstractViolationTypeViewModel,
        violation_view_model: AbstractViolationViewModel,
    ):
        BaseView.__init__(self)
        AbstractViolationListView.__init__(
            self,
            animal_view_model=animal_view_model,
            violation_type_view_model=violation_type_view_model,
            violation_view_model=violation_view_model,
        )

    def __build_days_from_select_box(self) -> int:
        options = self.violation_view_model.list_days_from()
        selected = st.selectbox(
            label="days from",
            options=options,
            index=0,
        )
        return selected

    def __build_sort_by_select_box(self) -> str:
        options = self.violation_view_model.list_violation_sort_by()
        selected = st.selectbox(
            label="sort by",
            options=options,
            index=0,
        )
        return selected

    def __build_violation_type_select_box(self) -> Optional[str]:
        options = self.violation_type_view_model.get_violation_types()
        _violation_type_names = ["ALL"]
        _violation_type_names.extend([v for v in options.keys()])
        _selected = st.selectbox(
            label="violation type",
            options=_violation_type_names,
            index=0,
        )
        selected = None if _selected == "ALL" else options[_selected]
        return selected

    def __build_aggregation_select_box(self) -> str:
        options = self.violation_view_model.list_aggregate_violation()
        return options[0]

    def __build_table(
        self,
        violation_df: pd.DataFrame,
    ):
        st.dataframe(violation_df)

    def __build_graph(
        self,
        aggregated_violation_df: pd.DataFrame,
        column: str,
    ):
        fig = go.Figure()
        violation_trace = go.Bar(
            x=aggregated_violation_df[column],
            y=aggregated_violation_df["count"],
        )
        fig.add_trace(violation_trace)
        st.plotly_chart(fig, use_container_width=True)

    def build(self):
        st.markdown("# Violations")
        days_from = self.__build_days_from_select_box()
        aggregated_violation = self.__build_aggregation_select_box()
        sort_by = self.__build_sort_by_select_box()
        violation_type_id = self.__build_violation_type_select_box()

        violation_df = self.violation_view_model.get_violations(
            violation_type_id=violation_type_id,
            days_from=days_from,
            sort_by=sort_by,
        )
        aggregated_violation_df = self.violation_view_model.aggregate_violations(
            violation_df=violation_df,
            column=aggregated_violation,
        )

        self.__build_table(violation_df=violation_df)
        self.__build_graph(
            aggregated_violation_df=aggregated_violation_df,
            column=aggregated_violation,
        )
