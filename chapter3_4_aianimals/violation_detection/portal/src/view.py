import logging
import random
from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Optional

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from service import AbstractAnimalService, AbstractViolationService, AbstractViolationTypeService


class VIEWS(Enum):
    ViolationListView = "violations"
    ViolationCheckView = "check violation"

    @staticmethod
    def has_value(value: int) -> bool:
        return value in [v.value for v in VIEWS.__members__.values()]

    @staticmethod
    def get_list() -> List[str]:
        return [v.value for v in VIEWS.__members__.values()]


class BaseView(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)


class AbstractViolationListView(ABC):
    def __init__(
        self,
        animal_service: AbstractAnimalService,
        violation_type_service: AbstractViolationTypeService,
        violation_service: AbstractViolationService,
    ):
        self.animal_service = animal_service
        self.violation_type_service = violation_type_service
        self.violation_service = violation_service

    @abstractmethod
    def build(self):
        raise NotImplementedError


class ViolationListView(BaseView, AbstractViolationListView):
    def __init__(
        self,
        animal_service: AbstractAnimalService,
        violation_type_service: AbstractViolationTypeService,
        violation_service: AbstractViolationService,
    ):
        BaseView.__init__(self)
        AbstractViolationListView.__init__(
            self,
            animal_service=animal_service,
            violation_type_service=violation_type_service,
            violation_service=violation_service,
        )

    def __build_days_from_select_box(self) -> int:
        options = self.violation_service.list_days_from()
        selected = st.selectbox(
            label="days from",
            options=options,
            index=0,
        )
        return selected

    def __build_sort_by_select_box(self) -> str:
        options = self.violation_service.list_violation_sort_by()
        selected = st.selectbox(
            label="sort by",
            options=options,
            index=0,
        )
        return selected

    def __build_sort_select_box(self) -> str:
        options = self.violation_service.list_sort()
        selected = st.selectbox(
            label="order",
            options=options,
            index=0,
        )
        return selected

    def __build_violation_type_select_box(self) -> Optional[str]:
        options = self.violation_type_service.get_violation_types()
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
        options = self.violation_service.list_aggregate_violation()
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
        sort = self.__build_sort_select_box()
        violation_type_id = self.__build_violation_type_select_box()

        violation_df = self.violation_service.get_violations(
            violation_type_id=violation_type_id,
            days_from=days_from,
            sort_by=sort_by,
            sort=sort,
        )
        if not violation_df.empty:
            aggregated_violation_df = self.violation_service.aggregate_violations(
                violation_df=violation_df,
                column=aggregated_violation,
            )

            self.__build_table(violation_df=violation_df)
            self.__build_graph(
                aggregated_violation_df=aggregated_violation_df,
                column=aggregated_violation,
            )
        else:
            st.markdown("# no violation found")


class AbstractViolationCheckView(ABC):
    def __init__(
        self,
        animal_service: AbstractAnimalService,
        violation_type_service: AbstractViolationTypeService,
        violation_service: AbstractViolationService,
    ):
        self.animal_service = animal_service
        self.violation_type_service = violation_type_service
        self.violation_service = violation_service

    @abstractmethod
    def build(self):
        raise NotImplementedError


class ViolationCheckView(BaseView, AbstractViolationCheckView):
    def __init__(
        self,
        animal_service: AbstractAnimalService,
        violation_type_service: AbstractViolationTypeService,
        violation_service: AbstractViolationService,
    ):
        BaseView.__init__(self)
        AbstractViolationCheckView.__init__(
            self,
            animal_service=animal_service,
            violation_type_service=violation_type_service,
            violation_service=violation_service,
        )

    def __build_violation_type_select_box(self) -> Optional[str]:
        options = self.violation_type_service.get_violation_types()
        _violation_type_names = ["ALL"]
        _violation_type_names.extend([v for v in options.keys()])
        _selected = st.selectbox(
            label="violation type",
            options=_violation_type_names,
            index=0,
        )
        selected = None if _selected == "ALL" else options[_selected]
        return selected

    def __build_is_effective_select_box(self) -> Optional[bool]:
        options = ["ALL", True, False]
        _selected = st.selectbox(
            label="is_effective",
            options=options,
            index=0,
        )
        selected = None if _selected == "ALL" else _selected
        return selected

    def __build_is_administrator_checked_select_box(self) -> Optional[bool]:
        options = ["ALL", True, False]
        _selected = st.selectbox(
            label="is_administrator_checked",
            options=options,
            index=0,
        )
        selected = None if _selected == "ALL" else _selected
        return selected

    def __build_sort_by_select_box(self) -> str:
        options = self.violation_service.list_violation_sort_by()
        selected = st.selectbox(
            label="sort by",
            options=options,
            index=0,
        )
        return selected

    def __build_sort_select_box(self) -> str:
        options = self.violation_service.list_sort()
        selected = st.selectbox(
            label="order",
            options=options,
            index=1,
        )
        return selected

    def __build_violation_container(
        self,
        violation: pd.DataFrame,
    ):
        st.markdown(f"{violation.animal_id}")
        image_col, text_col = st.columns([2, 2])
        with image_col:
            st.image(violation.photo_url, width=300)

        with text_col:
            st.markdown("### animal")
            st.write(violation.animal_id)
            st.write(violation.animal_name)
            st.write(violation.animal_description)
            st.write(f"deactivated {violation.is_animal_deactivated}")
            st.write(violation.animal_created_at)
            st.markdown("### violation")
            st.write(violation.id)
            st.write(violation.violation_type_name)
            st.write(f"judge: {violation.judge}")
            st.write(f"probability: {violation.probability}")
            st.write(f"is_effective: {violation.is_effective}")
            st.write(f"is_administrator_checked: {violation.is_administrator_checked}")
            st.write(violation.updated_at)

        is_violating = st.checkbox(
            label=f"is {violation.violation_type_name}",
            value=violation.is_effective,
            key=f"checkbox_{violation.id}_{violation.violation_type_name}_{violation.updated_at}",
        )
        is_administrator_checked = st.button(
            label="administrator checked",
            key=f"button_{violation.id}_{violation.violation_type_name}_{violation.updated_at}",
        )
        if is_administrator_checked:
            self.violation_service.register_admin_check(
                violation_id=violation.id,
                is_violation=is_violating,
            )
            if not is_violating:
                self.animal_service.activate(animal_id=violation.animal_id)
            else:
                self.animal_service.deactivate(animal_id=violation.animal_id)

    def build(self):
        st.markdown("# Violation check")
        violation_type_id = self.__build_violation_type_select_box()
        is_effective = self.__build_is_effective_select_box()
        is_administrator_checked = self.__build_is_administrator_checked_select_box()
        sort_by = self.__build_sort_by_select_box()
        sort = self.__build_sort_select_box()

        violation_df = self.violation_service.get_violations(
            violation_type_id=violation_type_id,
            is_effective=is_effective,
            is_administrator_checked=is_administrator_checked,
            sort_by=sort_by,
            sort=sort,
        )
        for _, violation in violation_df.iterrows():
            self.__build_violation_container(violation=violation)


class AbstractSidePane(ABC):
    def __init__(
        self,
        violation_list_view: AbstractViolationListView,
        violation_check_view: AbstractViolationCheckView,
    ):
        self.violation_list_view = violation_list_view
        self.violation_check_view = violation_check_view

    @abstractmethod
    def build(self):
        raise NotImplementedError


class SidePane(BaseView, AbstractSidePane):
    def __init__(
        self,
        violation_list_view: AbstractViolationListView,
        violation_check_view: AbstractViolationCheckView,
    ):
        BaseView.__init__(self)
        AbstractSidePane.__init__(
            self,
            violation_list_view=violation_list_view,
            violation_check_view=violation_check_view,
        )

    def __build_view_select_box(self):
        options = VIEWS.get_list()
        selected = st.sidebar.selectbox(
            label="view",
            options=options,
            index=0,
        )
        return selected

    def build(self):
        view = self.__build_view_select_box()
        if view == VIEWS.ViolationListView.value:
            self.violation_list_view.build()
        elif view == VIEWS.ViolationCheckView.value:
            self.violation_check_view.build()
        else:
            raise ValueError
