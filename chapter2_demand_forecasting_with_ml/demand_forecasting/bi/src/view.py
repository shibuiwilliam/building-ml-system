from typing import Dict, List, Optional, Union

import plotly.graph_objects as go
import streamlit as st
from logger import configure_logger
from view_model import ItemSaleViewModel, ItemViewModel, StoreViewModel

logger = configure_logger(__name__)


def build_item_sales_record():
    st.markdown("# Hi, I am bi by streamlit; be gentle.")
    st.markdown("# Item sales record")

    store_view_model = StoreViewModel()
    item_view_model = ItemViewModel()
    item_sale_view_model = ItemSaleViewModel()

    for store_name in store_view_model.store_masters:
        fig = go.Figure()
        for item_name in item_view_model.item_masters:
            quantities = item_sale_view_model.quantity_by_store_item(
                store_name=store_name,
                item_name=item_name,
            )
            fig.add_trace(
                go.Scatter(
                    x=quantities.dates,
                    y=quantities.quantities,
                    name=f"store_{store_name}_item_{item_name}",
                )
            )
        st.plotly_chart(
            fig,
            use_container_width=True,
        )
