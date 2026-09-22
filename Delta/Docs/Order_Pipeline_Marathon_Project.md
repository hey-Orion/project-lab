# Marathon Project: Order Ingestion & Reporting Pipeline

**Tools covered:** `requests`, `pydantic`, `sqlalchemy`, `pytest`, and raw `SQL` (via SQLite) — 5 tools in one small, fixed-scope project.

**Purpose:** This is your closed-book drilling project. Study the reference below, then close this file and rebuild it from memory daily until you need zero lookups. Once cold, vary it (see the bottom section) rather than starting a new project.

---

## 1. Project Scope (deliberately small — resist adding to it)

A script that:
1. **Fetches** order data from an API (simulated with a mock URL/local JSON for practice).
2. **Validates** each record with Pydantic.
3. **Saves** valid records to a SQLite database via SQLAlchemy.
4. **Queries** the saved data with a plain SQL report (e.g., total revenue per customer).
5. **Tests** the validation and save logic with pytest.

This mirrors your actual Dataflow-Sentinel pattern at a tiny scale — the same shape, minus the orchestration layer.

---

## 2. Reference Implementation

```python
# order_pipeline.py

import sqlite3
import requests
from pydantic import BaseModel, ValidationError
from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


# --- 1. Models & DB Setup ---
class Base(DeclarativeBase):
    pass


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    customer_name = Column(String)
    amount = Column(Float)
    status = Column(String)


DB_PATH = "orders.db"
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
SessionLocal = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)


# --- 2. Pydantic Schema ---
class OrderSchema(BaseModel):
    id: int
    customer_name: str
    amount: float
    status: str


# --- 3. Fetch ---
def fetch_orders(url: str) -> list[dict]:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()


# --- 4. Validate ---
def validate_orders(raw_data: list[dict]) -> list[OrderSchema]:
    valid = []
    for item in raw_data:
        try:
            valid.append(OrderSchema.model_validate(item))
        except ValidationError as e:
            print(f"Skipping invalid record: {e}")
    return valid


# --- 5. Save ---
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


# --- 6. Report (raw SQL) ---
def revenue_report():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT customer_name, SUM(amount) AS total_revenue
        FROM orders
        WHERE status = 'completed'
        GROUP BY customer_name
        ORDER BY total_revenue DESC;
    """)
    results = cursor.fetchall()
    conn.close()
    return results


# --- 7. Orchestration ---
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
```

```python
# test_order_pipeline.py

import pytest
from pydantic import ValidationError
from order_pipeline import OrderSchema


def test_valid_order_schema():
    payload = {"id": 1, "customer_name": "Alice", "amount": 150.0, "status": "completed"}
    order = OrderSchema.model_validate(payload)
    assert order.customer_name == "Alice"
    assert order.amount == 150.0


def test_invalid_order_schema_missing_field():
    payload = {"id": 2, "customer_name": "Bob", "status": "completed"}  # missing 'amount'
    with pytest.raises(ValidationError):
        OrderSchema.model_validate(payload)


def test_invalid_order_schema_wrong_type():
    payload = {"id": 3, "customer_name": "Carol", "amount": "not_a_number", "status": "completed"}
    with pytest.raises(ValidationError):
        OrderSchema.model_validate(payload)
```

---

## 3. How to Drill This (closed-book method)

**Day 1 of the marathon:** Study this file fully — read every line, understand *why* each piece exists (not just what it does). Then close it and attempt a full rebuild from memory. Note every place you got stuck.

**Every day after:** Same rebuild, same project, no new scope. Track how many times you had to peek — the goal is that number shrinking toward zero.

**Suggested order when rebuilding from memory** (matches your own natural sequence from the 10-day program):
1. Imports
2. SQLAlchemy model + engine/session setup
3. Pydantic schema
4. Fetch function
5. Validate function
6. Save function
7. Raw SQL report function
8. Orchestration (`run_pipeline`)
9. pytest tests (3 of them — one valid, two invalid in different ways)

**Talk out loud** as you write each section — say what it does and why, not just type silently.

---

## 4. Variations (only once you're fully cold on the base version)

Once you can write the whole thing from a blank page with zero hints, vary it to test real understanding rather than memorized muscle memory:

1. Add a new field to `Order` (e.g., `order_date`) and update the schema, model, and report query to use it.
2. Change the report to use a SQLAlchemy query instead of raw SQL (tests whether you understand both approaches, not just one).
3. Add a new validation rule (e.g., `amount` must be positive) using Pydantic's `Field(gt=0)`.
4. Add a 4th test: an edge case (e.g., `amount == 0`).
5. Swap SQLite for a different table entirely (e.g., `Product` instead of `Order`) — proves you know the *pattern*, not just this exact code.
