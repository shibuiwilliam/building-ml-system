from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Extra


class AccessLogCreateRequest(BaseModel):
    id: str
    phrases: List[str]
    animal_category_id: Optional[int] = None
    animal_subcategory_id: Optional[int] = None
    user_id: str
    likes: int
    animal_id: str
    action: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        extra = Extra.forbid
