import pytest
import pytest
from pydantic import ValidationError
from src.order_pipeline import OrderSchema

def test_valid_order_schema():
    payload = {"id": 1, "customer_name": "Alice", "amount": 150.0, "status": "completed"}
    order = OrderSchema.model_validate(payload)
    assert order.customer_name == "Alice"
    assert order.amount == 150.0

def test_invalid_order_schema_missing_field():
    payload = {"id": 2, "customer_name": "Bob", "status": "completed"}  # missing 'amount'
    with pytest.raise(ValidationError):
        OrderSchema.model_validate(payload)

def test_invalid_order_schema_wrong_type():
    payload = {"id": 3, "customer_name": "Carol", "amount": "not_a_number", "status": "completed"}
    with pytest.raise(ValidationError):
        OrderSchema.model_validate(payload)