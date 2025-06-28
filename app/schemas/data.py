from pydantic import BaseModel

class DataEntrySchema(BaseModel):
    id: int
    name: str
    meta: str
    score: float = None

    class Config:
        orm_mode = True 