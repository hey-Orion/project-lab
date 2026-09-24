import sqlite3
import requests
from pydantic import BaseModel, ValidationError
from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

class Base(DeclarativeBase):
    pass

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    customer_name = Column(String)
    amount = Column(Float)
    status = Column(String)


DB_PATH = 'orders.db'
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

class OrderSchema(BaseModel):
    id: int 
    customer_name: str 
    amount: float 
    status: str 


def fetch_orders(url: str) -> list[dict]:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()


def validate_orders(raw_data: list[dict]) -> list[OrderSchema]:
    valid = []
    for item in raw_data:
        try:
            valid.append(OrderSchema.model_validate(item))
        except ValidationError as e:
            print(f"Skipping invalid record: {e}")
    return valid


def save_orders(valid_orders: list[OrderSchema]):
    session = SessionLocal()
    try:
        for order in valid_orders:
            db_order = Order(**order.model_dump())
            session.add(db_order)
        session.commit()
    except Exception:
        session.rollback()
        raise 
    finally:
        session.close()


def revenue_report():
    conn = sqlite3.commit(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        select customer_name, sum(amount) as total_revenue
        from orders
        where status = 'completed'
        group by customer_name
        order by total_revenue DESC;
    """)
    result = cursor.fetchall()
    conn.close()
    return result 


def run_pipeline(url: str):
    init_db()
    raw = fetch_orders(url)
    validated = validate_orders(raw)
    save_orders(validated)
    return revenue_report()

if __name__ == "__main__":
    report = run_pipeline("https://api.example.com/orders")
    for row in report:
        print(row)