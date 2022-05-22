from enum import Enum
from typing import List, Optional, Tuple

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from logger import configure_logger
from service import ItemSalesPredictionEvaluationService, ItemSalesService, ItemService, RegionService, StoreService

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


def build_region_selectbox(region_service: RegionService) -> Optional[str]:
    options = region_service.list_regions()
    options.append("ALL")
    selected = st.sidebar.selectbox(
        label="region",
        options=options,
    )
    return selected


def build_store_selectbox(
    store_service: StoreService,
    region: Optional[str] = None,
) -> Optional[str]:
    options = store_service.list_stores(region=region)
    options.append("ALL")
    selected = st.sidebar.selectbox(
        label="store",
        options=options,
    )
    return selected


def build_item_selectbox(
    item_service: ItemService,
) -> Optional[str]:
    options = item_service.list_items()
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


def build_base(
    region_service: RegionService,
    store_service: StoreService,
    item_service: ItemService,
    item_sales_service: ItemSalesService,
) -> Tuple[Optional[str], Optional[str], Optional[str], List[str], List[str], pd.DataFrame]:
    region = build_region_selectbox(region_service=region_service)
    store = build_store_selectbox(
        store_service=store_service,
        region=region,
    )
    item = build_item_selectbox(item_service=item_service)

    if region == "ALL":
        region = None
    if store == "ALL":
        store = None
    if item == "ALL":
        item = None

    daily_sales_df = item_sales_service.retrieve_daily_item_sales(
        item=item,
        store=store,
        region=region,
    )

    stores = daily_sales_df.store.unique()
    items = daily_sales_df.item.unique()
    return region, store, item, stores, items, daily_sales_df


def build_item_sales(
    region_service: RegionService,
    store_service: StoreService,
    item_service: ItemService,
    item_sales_service: ItemSalesService,
):
    logger.info("build item sales BI...")
    _, _, _, stores, items, daily_sales_df = build_base(
        region_service=region_service,
        store_service=store_service,
        item_service=item_service,
        item_sales_service=item_sales_service,
    )
    time_frame = build_time_frame_selectbox()

    if time_frame == TIME_FRAME.DAILY.value:
        show_daily_item_sales(
            df=daily_sales_df,
            stores=stores,
            items=items,
        )
    elif time_frame == TIME_FRAME.WEEKLY.value:
        weekly_sales_df = item_sales_service.retrieve_weekly_item_sales(daily_sales_df=daily_sales_df)
        show_weekly_item_sales(
            df=weekly_sales_df,
            stores=stores,
            items=items,
        )
    elif time_frame == TIME_FRAME.MONTHLY.value:
        monthly_sales_df = item_sales_service.retrieve_monthly_item_sales(daily_sales_df=daily_sales_df)
        show_monthly_item_sales(
            df=monthly_sales_df,
            stores=stores,
            items=items,
        )


def build_item_sales_prediction_evaluation(
    region_service: RegionService,
    store_service: StoreService,
    item_service: ItemService,
    item_sales_service: ItemSalesService,
    item_sales_prediction_evaluation_service: ItemSalesPredictionEvaluationService,
):
    logger.info("build item sales prediction evaluation BI...")
    region, store, item, stores, items, daily_sales_df = build_base(
        region_service=region_service,
        store_service=store_service,
        item_service=item_service,
        item_sales_service=item_sales_service,
    )
    weekly_sales_df = item_sales_service.retrieve_weekly_item_sales(daily_sales_df=daily_sales_df)
    weekly_sales_evaluation_df = item_sales_prediction_evaluation_service.aggregate_item_weekly_sales_evaluation(
        weekly_sales_df=weekly_sales_df,
        region=region,
        store=store,
        item=item,
    )
    st.dataframe(weekly_sales_evaluation_df)


def build(
    region_service: RegionService,
    store_service: StoreService,
    item_service: ItemService,
    item_sales_service: ItemSalesService,
    item_sales_prediction_evaluation_service: ItemSalesPredictionEvaluationService,
):
    st.markdown("# Hi, I am BI by streamlit; Let's have a fun!")
    st.markdown("# Item sales record")

    bi = build_bi_selectbox()

    if bi is None:
        return
    elif bi == BI.ITEM_SALES.value:
        build_item_sales(
            region_service=region_service,
            store_service=store_service,
            item_service=item_service,
            item_sales_service=item_sales_service,
        )
    elif bi == BI.ITEM_SALES_PREDICTION_EVALUATION.value:
        build_item_sales_prediction_evaluation(
            region_service=region_service,
            store_service=store_service,
            item_service=item_service,
            item_sales_service=item_sales_service,
            item_sales_prediction_evaluation_service=item_sales_prediction_evaluation_service,
        )
    else:
        raise ValueError()
