from logging import getLogger
from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.middleware.database import get_session
from src.registry.container import container
from src.schema.animal import AnimalCreate, AnimalModel, AnimalModelWithLike

logger = getLogger(__name__)

router = APIRouter()


@router.get("", response_model=List[AnimalModelWithLike])
async def get_animal(
    id: Optional[str] = None,
    name: Optional[str] = None,
    animal_category_name: Optional[str] = None,
    animal_subcategory_name: Optional[str] = None,
    user_id: Optional[str] = None,
    deactivated: Optional[bool] = False,
    session: Session = Depends(get_session),
):
    data = container.animal_usecase.retrieve(
        session=session,
        id=id,
        name=name,
        animal_category_name=animal_category_name,
        animal_subcategory_name=animal_subcategory_name,
        user_id=user_id,
        deactivated=deactivated,
    )
    return data


@router.post("", response_model=Optional[AnimalModel])
async def create_animal(
    animal: AnimalCreate,
    session: Session = Depends(get_session),
):
    data = container.animal_usecase.register(
        session=session,
        record=animal,
    )
    return data
