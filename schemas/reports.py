from pydantic import BaseModel
from typing import List, Optional


class Gtin(BaseModel):
    """ Параметры товара """
    gtin: Optional[str]
    product_name: Optional[str]
    product_short_name: Optional[str]
    tnved: Optional[str]
    tnved10: Optional[str]
    brand: Optional[str]
    country: Optional[str]
    loss_percentage: Optional[float]
    message: Optional[str]


class NewReport(BaseModel):
    """ Параметры для отчета от менеджера """
    id_sp: str
    gtins: List[Gtin]
