from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.container.container import container
from src.middleware.database import get_db
from src.repository.item_master_repository import ItemMaster
from src.repository.item_price_repository import ItemPrice
from src.repository.item_sale_repository import ItemSale

router = APIRouter()


@router.get("/masters", response_model=List[ItemMaster])
async def get_item_master(
    id: Optional[str] = None,
    item_name: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return container.item_service.retrieve_item_master(
        db=db,
        id=id,
        item_name=item_name,
    )


@router.get("/prices", response_model=List[ItemPrice])
async def get_item_price(
    id: Optional[str] = None,
    item_name: Optional[str] = None,
    item_id: Optional[str] = None,
    applied_from: Optional[date] = None,
    applied_to: Optional[date] = None,
    applied_at: Optional[date] = None,
    db: Session = Depends(get_db),
):
    return container.item_service.retrieve_item_price(
        db=db,
        id=id,
        item_name=item_name,
        item_id=item_id,
        applied_from=applied_from,
        applied_to=applied_to,
        applied_at=applied_at,
    )


@router.get("/sales", response_model=List[ItemSale])
async def get_item_sale(
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
