import datetime
from pydantic import BaseModel


class Market(BaseModel):
    id: int
    name: str
    open_date: datetime.date
    close_date: datetime.date
    operation_status: bool
    seller_id: int

    class Config:
        orm_mode = True


class MarketCreate(BaseModel):
    id: int
    name: str
    open_date: datetime.date
    close_date: datetime.date
    operation_status: bool
    seller_id: int

    class Config:
        orm_mode = True