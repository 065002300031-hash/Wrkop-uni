from pydantic import BaseModel
from typing import Optional

class MenuBase(BaseModel):
    name: str
    category: str
    price: int
    prep_time: int
    image: Optional[str] = ""
    description: Optional[str] = ""

class MenuCreate(MenuBase):
    pass

class Menu(MenuBase):
    id: int
    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    order_code: str
    service_type: str
    customer_info: str
    items_summary: str
    total_price: int

class OrderCreate(OrderBase):
    pass

class OrderStatusUpdate(BaseModel):
    status: int

class Order(OrderBase):
    id: int
    status: int
    class Config:
        from_attributes = True