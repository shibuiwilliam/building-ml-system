from enum import Enum
from typing import Dict, List, Optional, Union

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from logger import configure_logger
from view_model import ItemSalesViewModel, ItemViewModel, RegionViewModel, StoreViewModel

logger = configure_logger(__name__)


class BI(Enum):
    ITEM_SALES = "item_sales"
    ITEM_SALES_PREDICTION_EVALUATION = "item_sales_prediction_evaluation"


def build_bi_selectbox() -> str:
    options = [BI.ITEM_SALES.value, BI.ITEM_SALES_PREDICTION_EVALUATION.value]
    selected = st.sidebar.selectbox(
        label="BI",
        options=options,
    )
    return selected


def build_region_selectbox(region_view_model: RegionViewModel) -> Optional[str]:
    options = [None]
    regions = region_view_model.list_regions()
    options.extend(regions)
    selected = st.sidebar.selectbox(
        label="region",
        options=options,
    )
    return selected


def build_store_selectbox(
    store_view_model: StoreViewModel,
    region: Optional[str] = None,
) -> Optional[str]:
    options = [None]
    stores = store_view_model.list_stores(region=region)
    options.extend(stores)
    selected = st.sidebar.selectbox(
        label="store",
        options=options,
    )
    return selected


def build_item_selectbox(
    item_view_model: ItemViewModel,
) -> Optional[str]:
    options = [None]
    items = item_view_model.list_items()
    options.extend(items)
    selected = st.sidebar.selectbox(
        label="item",
        options=options,
    )
    return selected


def build_item_sales(
    region_view_model: RegionViewModel,
    store_view_model: StoreViewModel,
    item_view_model: ItemViewModel,
    item_sales_view_model: ItemSalesViewModel,
):
    logger.info("build item sales BI...")
    region = build_region_selectbox(region_view_model=region_view_model)
    store = build_store_selectbox(
        store_view_model=store_view_model,
        region=region,
    )
    item = build_item_selectbox(item_view_model=item_view_model)

    dataset = item_sales_view_model.list_item_sales(
        item=item,
        store=store,
        region=region,
    )
    df = pd.DataFrame([d.dict() for d in dataset])
    st.dataframe(df)


def build_item_sales_prediction_evaluation(
    region_view_model: RegionViewModel,
    store_view_model: StoreViewModel,
    item_view_model: ItemViewModel,
    item_sales_view_model: ItemSalesViewModel,
):
    logger.info("build item sales prediction evaluation BI...")


def build(
    region_view_model: RegionViewModel,
    store_view_model: StoreViewModel,
    item_view_model: ItemViewModel,
    item_sales_view_model: ItemSalesViewModel,
):
    st.markdown("# Hi, I am BI by streamlit; Let's have a fun!")
    st.markdown("# Item sales record")

    bi = build_bi_selectbox()

    if bi == BI.ITEM_SALES.value:
        build_item_sales(
            region_view_model=region_view_model,
            store_view_model=store_view_model,
            item_view_model=item_view_model,
            item_sales_view_model=item_sales_view_model,
        )
    elif bi == BI.ITEM_SALES_PREDICTION_EVALUATION.value:
        build_item_sales_prediction_evaluation(
            region_view_model=region_view_model,
            store_view_model=store_view_model,
            item_view_model=item_view_model,
            item_sales_view_model=item_sales_view_model,
        )
    else:
        raise ValueError()
