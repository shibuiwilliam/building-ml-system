from logging import getLogger
from typing import List, Optional

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from src.middleware.assert_token import token_assertion
from src.registry.container import container
from src.request_object.animal_category import AnimalCategoryRequest
from src.request_object.animal_subcategory import AnimalSubcategoryRequest
from src.response_object.animal_category import AnimalCategoryResponse
from src.response_object.animal_subcategory import AnimalSubcategoryResponse

logger = getLogger(__name__)

router = APIRouter()


@router.get("", response_model=List[AnimalCategoryResponse])
async def get_animal_category(
    id: Optional[int] = None,
    name_en: Optional[str] = None,
    name_ja: Optional[str] = None,
    is_deleted: Optional[bool] = False,
    token: str = Header(...),
    session: Session = Depends(container.database.get_session),
):
    await token_assertion(
        token=token,
        session=session,
    )
    data = container.animal_category_usecase.retrieve(
        session=session,
        request=AnimalCategoryRequest(
            id=id,
            name_en=name_en,
            name_ja=name_ja,
            is_deleted=is_deleted,
        ),
    )
    return data


@router.get("/subcategory", response_model=List[AnimalSubcategoryResponse])
async def get_animal_subcategory(
    id: Optional[int] = None,
    name_en: Optional[str] = None,
    name_ja: Optional[str] = None,
    animal_category_name_en: Optional[str] = None,
    animal_category_name_ja: Optional[str] = None,
    is_deleted: Optional[bool] = False,
    token: str = Header(...),
    session: Session = Depends(container.database.get_session),
):
    await token_assertion(
        token=token,
        session=session,
    )
    data = container.animal_subcategory_usecase.retrieve(
        session=session,
        request=AnimalSubcategoryRequest(
            id=id,
            name_en=name_en,
            name_ja=name_ja,
            animal_category_name_en=animal_category_name_en,
            animal_category_name_ja=animal_category_name_ja,
            is_deleted=is_deleted,
        ),
    )
    return data
