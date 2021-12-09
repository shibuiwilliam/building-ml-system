from datetime import datetime

from pydantic import BaseModel, Extra


class LikeResponse(BaseModel):
    id: str
    animal_id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        extra = Extra.forbid
