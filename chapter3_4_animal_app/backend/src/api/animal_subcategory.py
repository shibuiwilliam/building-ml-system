from logging import getLogger
from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.middleware.database import get_session
from src.registry.container import container
from src.request_object.animal_subcategory import AnimalSubcategoryRequest
from src.response_object.animal_subcategory import AnimalSubcategoryResponse

logger = getLogger(__name__)

router = APIRouter()


@router.get("", response_model=List[AnimalSubcategoryResponse])
async def get_animal_subcategory(
    id: Optional[str] = None,
    name: Optional[str] = None,
    animal_category_name: Optional[str] = None,
    is_deleted: Optional[bool] = False,
    session: Session = Depends(get_session),
):
    data = container.animal_subcategory_usecase.retrieve(
        session=session,
        request=AnimalSubcategoryRequest(
            id=id,
            name=name,
            animal_category_name=animal_category_name,
            is_deleted=is_deleted,
        ),
    )
    return data
