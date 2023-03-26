from pydantic import BaseModel
from datetime import datetime


class RetailOut(BaseModel):
    id: int = None
    dt: datetime
    gtin: str
    prid: str
    inn: str
    id_sp: str
    type_operation: str
    price: int
    cnt: int

    class Config:
        orm_mode = True
