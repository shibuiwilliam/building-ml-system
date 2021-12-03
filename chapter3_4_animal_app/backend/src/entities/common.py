from pydantic import BaseModel


class Count(BaseModel):
    count: int

    class Config:
        orm_mode = True
