import sqlite3
import requests
from pydantic import BaseModel, ValidationError
from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass

class Order(Base):
    __tablemane__ = "orders"

    id = Column(Integer, primary_key=True)
    customer_name = Column(String)
    amount = Column(Float)
    status = Column(String)

DB_PATH = "order.db"
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
SessionLocal = sessionmaker(bind=enigne)


def init_db():
    Base.metadata.create_all(bind=enigne)

class OrderSchema(BaseModel):
    id: int 
    customer_name: str 
    amount: float 
    status: str 

def fetch_orders(url: str) -> list[dict]:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()

    