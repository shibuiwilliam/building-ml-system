from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.container.container import container
from src.middleware.database import get_db
from src.repository.item_sale_repository import ItemSale

router = APIRouter()


@router.get("/", response_model=List[ItemSale])
def get_item_master(
    id: Optional[str] = None,
    item_name: Optional[str] = None,
    item_id: Optional[str] = None,
    store_name: Optional[str] = None,
    store_id: Optional[str] = None,
    item_price_id: Optional[str] = None,
    quantity: Optional[int] = None,
    sold_at: Optional[date] = None,
    day_of_week: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    return container.item_service.retrieve_item_sale(
        db=db,
        id=id,
        item_name=item_name,
        item_id=item_id,
        store_name=store_name,
        store_id=store_id,
        item_price_id=item_price_id,
        quantity=quantity,
        sold_at=sold_at,
        day_of_week=day_of_week,
        limit=limit,
        offset=offset,
    )
