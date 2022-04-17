from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Extra


class AccessLogCreateRequest(BaseModel):
    search_id: str
    phrases: List[str]
    animal_category_id: Optional[int] = None
    animal_subcategory_id: Optional[int] = None
    sort_by: str
    model_name: Optional[str]
    user_id: Optional[str]
    animal_id: str
    action: str
    created_at: Optional[datetime] = None

    class Config:
        extra = Extra.forbid
