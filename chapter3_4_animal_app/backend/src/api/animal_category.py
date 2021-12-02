from logging import getLogger
from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.middleware.database import get_session
from src.registry.container import container
from src.request_object.animal_category import AnimalCategoryQuery
from src.response_object.animal_category import AnimalCategoryModel

logger = getLogger(__name__)

router = APIRouter()


@router.get("", response_model=List[AnimalCategoryModel])
async def get_animal_category(
    id: Optional[str] = None,
    name: Optional[str] = None,
    is_deleted: Optional[bool] = False,
    session: Session = Depends(get_session),
):
    data = container.animal_category_usecase.retrieve(
        session=session,
        request=AnimalCategoryQuery(
            id=id,
            name=name,
            is_deleted=is_deleted,
        ),
    )
    return data
