import logging
from abc import ABC, abstractmethod
from typing import List

import plotly.graph_objects as go
import streamlit as st
from view_model import AbstractAnimalViewModel, AbstractViolationTypeViewModel, AbstractViolationViewModel


class BaseView(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)


class AbstractViolationView(ABC):
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


class ViolationView(BaseView, AbstractViolationView):
    def __init__(
        self,
        animal_view_model: AbstractAnimalViewModel,
        violation_type_view_model: AbstractViolationTypeViewModel,
        violation_view_model: AbstractViolationViewModel,
    ):
        BaseView.__init__(self)
        AbstractViolationView.__init__(
            self,
            animal_view_model=animal_view_model,
            violation_type_view_model=violation_type_view_model,
            violation_view_model=violation_view_model,
        )

    def build(self):
        st.markdown("# Violations")
        violation_df = self.violation_view_model()
        st.dataframe(violation_df)
