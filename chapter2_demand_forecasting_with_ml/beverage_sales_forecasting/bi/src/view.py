from enum import Enum
from typing import Dict, List, Optional, Union

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from logger import configure_logger
from plotly.subplots import make_subplots
from view_model import ItemSalesViewModel, ItemViewModel, RegionViewModel, StoreViewModel

logger = configure_logger(__name__)


class BI(Enum):
    ITEM_SALES = "item_sales"
    ITEM_SALES_PREDICTION_EVALUATION = "item_sales_prediction_evaluation"


class TIME_FRAME(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


def build_bi_selectbox() -> str:
    options = [None, BI.ITEM_SALES.value, BI.ITEM_SALES_PREDICTION_EVALUATION.value]
    selected = st.sidebar.selectbox(
        label="BI",
        options=options,
    )
    return selected


def build_region_selectbox(region_view_model: RegionViewModel) -> Optional[str]:
    options = region_view_model.list_regions()
    options.append("ALL")
    selected = st.sidebar.selectbox(
        label="region",
        options=options,
    )
    return selected


def build_store_selectbox(
    store_view_model: StoreViewModel,
    region: Optional[str] = None,
) -> Optional[str]:
    options = store_view_model.list_stores(region=region)
    options.append("ALL")
    selected = st.sidebar.selectbox(
        label="store",
        options=options,
    )
    return selected


def build_item_selectbox(
    item_view_model: ItemViewModel,
) -> Optional[str]:
    options = item_view_model.list_items()
    options.append("ALL")
    selected = st.sidebar.selectbox(
        label="item",
        options=options,
    )
    return selected


def build_time_frame_selectbox() -> Optional[str]:
    options = [TIME_FRAME.DAILY.value, TIME_FRAME.WEEKLY.value, TIME_FRAME.MONTHLY.value]
    selected = st.sidebar.selectbox(
        label="time frame",
        options=options,
    )
    return selected


def show_daily_item_sales(
    df: pd.DataFrame,
    stores: List[str],
    items: List[str],
):
    st.markdown("### Daily summary")
    for s in stores:
        for i in items:
            _df = (
                df[(df.store == s) & (df.item == i)]
                .drop(["store", "item"], axis=1)
                .reset_index(drop=True)
                .sort_values("date")
            )
            region = _df.region.unique()[0]
            _df = _df.drop("region", axis=1)
            with st.expander(
                label=f"REGION {region} STORE {s} ITEM {i}",
                expanded=True,
            ):
                st.dataframe(_df)

                fig = go.Figure()
                sales_trace = go.Bar(
                    x=_df.date,
                    y=_df.sales,
                )
                fig.add_trace(sales_trace)
                fig.update_yaxes(range=[0, 150])
                st.plotly_chart(fig, use_container_width=True)
                logger.info(f"REGION {region} STORE {s} ITEM {i}")


def show_weekly_item_sales(
    df: pd.DataFrame,
    stores: List[str],
    items: List[str],
):
    st.markdown("### Weekly summary")
    for s in stores:
        for i in items:
            _df = (
                df[(df.store == s) & (df.item == i)]
                .drop(["store", "item"], axis=1)
                .reset_index(drop=True)
                .sort_values(["year", "month", "week_of_year"])
            )
            region = _df.region.unique()[0]
            _df = _df.drop("region", axis=1)
            with st.expander(
                label=f"REGION {region} STORE {s} ITEM {i}",
                expanded=True,
            ):
                st.dataframe(_df)

                fig = go.Figure()
                sales_trace = go.Bar(
                    x=_df.year.astype(str)
                    .str.cat(_df.month.astype(str), sep="_")
                    .str.cat(_df.week_of_year.astype(str), sep="_"),
                    y=_df.sales,
                )
                fig.add_trace(sales_trace)
                fig.update_yaxes(range=[0, 1000])
                st.plotly_chart(fig, use_container_width=True)
                logger.info(f"REGION {region} STORE {s} ITEM {i}")


def show_monthly_item_sales(
    df: pd.DataFrame,
    stores: List[str],
    items: List[str],
):
    st.markdown("### Monthly summary")
    for s in stores:
        for i in items:
            _df = (
                df[(df.store == s) & (df.item == i)]
                .drop(["store", "item"], axis=1)
                .reset_index(drop=True)
                .sort_values(["year", "month"])
            )
            region = _df.region.unique()[0]
            _df = _df.drop("region", axis=1)
            with st.expander(
                label=f"REGION {region} STORE {s} ITEM {i}",
                expanded=True,
            ):
                st.dataframe(_df)

                fig = go.Figure()
                sales_trace = go.Bar(
                    x=_df.year.astype(str).str.cat(_df.month.astype(str), sep="_"),
                    y=_df.sales,
                )
                fig.add_trace(sales_trace)
                fig.update_yaxes(range=[0, 5000])
                st.plotly_chart(fig, use_container_width=True)
                logger.info(f"REGION {region} STORE {s} ITEM {i}")


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

    time_frame = build_time_frame_selectbox()

    if region == "ALL":
        region = None
    if store == "ALL":
        store = None
    if item == "ALL":
        item = None

    daily_df = item_sales_view_model.retrieve_daily_item_sales(
        item=item,
        store=store,
        region=region,
    )

    stores = daily_df.store.unique()
    items = daily_df.item.unique()

    if time_frame == TIME_FRAME.DAILY.value:
        show_daily_item_sales(
            df=daily_df,
            stores=stores,
            items=items,
        )
    elif time_frame == TIME_FRAME.WEEKLY.value:
        weekly_df = item_sales_view_model.retrieve_weekly_item_sales(daily_df=daily_df)
        show_weekly_item_sales(
            df=weekly_df,
            stores=stores,
            items=items,
        )
    elif time_frame == TIME_FRAME.MONTHLY.value:
        monthly_df = item_sales_view_model.retrieve_monthly_item_sales(daily_df=daily_df)
        show_monthly_item_sales(
            df=monthly_df,
            stores=stores,
            items=items,
        )


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

    if bi is None:
        return
    elif bi == BI.ITEM_SALES.value:
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
