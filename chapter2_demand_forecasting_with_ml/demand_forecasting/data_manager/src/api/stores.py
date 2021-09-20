from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.container.container import container
from src.middleware.database import get_db
from src.repository.store_master_repository import StoreMaster

router = APIRouter()


@router.get("/", response_model=List[StoreMaster])
def get_store_master(
    id: Optional[str] = None,
    region_id: Optional[str] = None,
    name: Optional[str] = None,
    region_name: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return container.store_service.retrieve_store_master(
        db=db,
        id=id,
        region_id=region_id,
        name=name,
        region_name=region_name,
    )
