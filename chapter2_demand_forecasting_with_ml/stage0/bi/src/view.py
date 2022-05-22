import os
from enum import Enum
from typing import List, Optional, Tuple

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from configurations import Configurations
from logger import configure_logger
from model import Container
from plotly.subplots import make_subplots
from service import ItemSalesPredictionEvaluationService, ItemSalesService, ItemService, StoreService

logger = configure_logger(__name__)


class BI(Enum):
    ITEM_SALES = "item_sales"
    ITEM_SALES_PREDICTION_EVALUATION = "item_sales_prediction_evaluation"


class TIME_FRAME(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


def init_container() -> Container:
    container = Container()
    container.load_sales_df(file_path=Configurations.item_sales_record_file)
    return container


def build_sales_prediction_target_selectbox(container: Container) -> Tuple[Optional[Container], Optional[str]]:
    options = [None]
    _options = os.listdir(Configurations.item_sales_prediction_dir)
    options.extend(_options)
    selected = st.sidebar.selectbox(
        label="Predictions Year_Week",
        options=options,
    )
    if selected is not None:
        container.load_prediction_df(
            prediction_file_path=os.path.join(
                Configurations.item_sales_prediction_dir,
                selected,
                "prediction.csv",
            ),
            prediction_record_file_path=os.path.join(
                Configurations.item_sales_prediction_dir,
                selected,
                "sales.csv",
            ),
        )
        return container, selected
    else:
        return None, None


def build_bi_selectbox() -> str:
    options = [None, BI.ITEM_SALES.value, BI.ITEM_SALES_PREDICTION_EVALUATION.value]
    selected = st.sidebar.selectbox(
        label="BI",
        options=options,
    )
    return selected


def build_store_selectbox(
    container: Container,
    store_service: StoreService,
) -> Optional[str]:
    options = store_service.list_stores(container=container)
    options.append("ALL")
    selected = st.sidebar.selectbox(
        label="store",
        options=options,
    )
    return selected


def build_item_selectbox(
    container: Container,
    item_service: ItemService,
) -> Optional[str]:
    options = item_service.list_items(container=container)
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


def build_aggregation_selectbox() -> str:
    options = ["store", "item"]
    selected = st.sidebar.selectbox(
        label="aggregate by",
        options=options,
    )
    return selected


def build_sort_selectbox() -> str:
    options = ["store", "item", "sales", "prediction", "diff", "error_rate"]
    selected = st.sidebar.selectbox(
        label="sort by",
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
            with st.expander(
                label=f"STORE {s} ITEM {i}",
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
                logger.info(f"Daily STORE {s} ITEM {i}")


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
            with st.expander(
                label=f"STORE {s} ITEM {i}",
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
                logger.info(f"Weekly STORE {s} ITEM {i}")


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
            with st.expander(
                label=f"STORE {s} ITEM {i}",
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
                logger.info(f"Monthly STORE {s} ITEM {i}")


def show_weekly_item_sales_evaluation(
    df: pd.DataFrame,
    year_week: str,
    aggregate_by: str,
    sort_by: str,
):
    st.markdown(f"### Weekly evaluation for {year_week}")
    if aggregate_by == "store":
        loop_in = df.store.unique()
        not_aggregated = "item"
    else:
        loop_in = df.item.unique()
        not_aggregated = "store"
    for li in loop_in:
        _df = df[df[aggregate_by] == li].reset_index(drop=True).sort_values(["year", "month", "week_of_year", sort_by])
        with st.expander(
            label=f"{aggregate_by} {li}",
            expanded=True,
        ):
            st.dataframe(_df)

            fig = make_subplots(specs=[[{"secondary_y": True}]])
            sales_trace = go.Bar(
                x=_df[not_aggregated],
                y=_df.sales,
                name="sales",
            )
            prediction_trace = go.Bar(
                x=_df[not_aggregated],
                y=_df.prediction,
                name="prediction",
            )
            diff_trace = go.Bar(
                x=_df[not_aggregated],
                y=_df["diff"],
                name="diff",
            )
            error_rate_trace = go.Scatter(
                x=_df[not_aggregated],
                y=_df["error_rate"],
                name="error_rate",
            )
            fig.add_trace(
                sales_trace,
                secondary_y=False,
            )
            fig.add_trace(
                prediction_trace,
                secondary_y=False,
            )
            fig.add_trace(
                diff_trace,
                secondary_y=False,
            )
            fig.add_trace(
                error_rate_trace,
                secondary_y=True,
            )
            fig.update_yaxes(
                title_text="numeric",
                range=[-100, 1000],
                secondary_y=False,
            )
            fig.update_yaxes(
                title_text="rate",
                range=[-1, 1],
                secondary_y=True,
            )
            st.plotly_chart(fig, use_container_width=True)
            logger.info(f"{aggregate_by} {li}")


def build_item_sales(
    container: Container,
    store_service: StoreService,
    item_service: ItemService,
    item_sales_service: ItemSalesService,
):
    logger.info("build item sales BI...")
    store = build_store_selectbox(
        container=container,
        store_service=store_service,
    )
    item = build_item_selectbox(
        container=container,
        item_service=item_service,
    )

    if store == "ALL":
        store = None
    if item == "ALL":
        item = None

    daily_sales_df = item_sales_service.retrieve_daily_item_sales(
        container=container,
        item=item,
        store=store,
    )

    stores = daily_sales_df.store.unique()
    items = daily_sales_df.item.unique()

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
    container: Container,
    store_service: StoreService,
    item_service: ItemService,
    item_sales_service: ItemSalesService,
    item_sales_prediction_evaluation_service: ItemSalesPredictionEvaluationService,
):
    logger.info("build item sales prediction evaluation BI...")
    store = build_store_selectbox(
        container=container,
        store_service=store_service,
    )
    item = build_item_selectbox(
        container=container,
        item_service=item_service,
    )

    aggregate_by = build_aggregation_selectbox()
    sort_by = build_sort_selectbox()

    if store == "ALL":
        store = None
    if item == "ALL":
        item = None

    container, year_week = build_sales_prediction_target_selectbox(container=container)
    if container is None or year_week is None:
        return

    weekly_sales_df = item_sales_service.retrieve_weekly_item_sales(daily_sales_df=container.prediction_record_df)
    weekly_sales_evaluation_df = item_sales_prediction_evaluation_service.aggregate_item_weekly_sales_evaluation(
        container=container,
        weekly_sales_df=weekly_sales_df,
        store=store,
        item=item,
    )
    show_weekly_item_sales_evaluation(
        df=weekly_sales_evaluation_df,
        year_week=year_week,
        aggregate_by=aggregate_by,
        sort_by=sort_by,
    )


def build(
    store_service: StoreService,
    item_service: ItemService,
    item_sales_service: ItemSalesService,
    item_sales_prediction_evaluation_service: ItemSalesPredictionEvaluationService,
):
    st.markdown("# Hi, I am BI by streamlit; Let's have a fun!")
    st.markdown("# Item sales record")

    container = init_container()
    bi = build_bi_selectbox()

    if bi is None:
        return
    elif bi == BI.ITEM_SALES.value:
        build_item_sales(
            container=container,
            store_service=store_service,
            item_service=item_service,
            item_sales_service=item_sales_service,
        )
    elif bi == BI.ITEM_SALES_PREDICTION_EVALUATION.value:
        build_item_sales_prediction_evaluation(
            container=container,
            store_service=store_service,
            item_service=item_service,
            item_sales_service=item_sales_service,
            item_sales_prediction_evaluation_service=item_sales_prediction_evaluation_service,
        )
    else:
        raise ValueError()
