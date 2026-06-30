from sqlalchemy import Column, Integer, String
from database import Base

class Menu(Base):
    __tablename__ = "menus"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String)
    price = Column(Integer)
    prep_time = Column(Integer)
    image = Column(String, default="")
    description = Column(String, default="")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    order_code = Column(String, unique=True, index=True)
    service_type = Column(String)
    customer_info = Column(String)
    items_summary = Column(String)
    total_price = Column(Integer)
    status = Column(Integer, default=1)