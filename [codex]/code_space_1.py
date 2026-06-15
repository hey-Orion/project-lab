import pytest
import pandas as pd
from micro_sentinel import ingest_payloads, transform_records  # Imports your logic

# Step 1: The Test Data Factory (Fixture)
@pytest.fixture
def mock_raw_stream_data():
    return [
        {
            "id": 10,
            "name": "Jane Doe",
            "username": " JANE_DOE ",  # Needs trimming
            "email": "JANE@Domain.Com", # Needs lowercasing
            "phone": "555-1234",
            "website": None,            # Needs Imputation (N/A)
            "timestamp": "2026-06-15T20:00:00"
        },
        {
            "id": -5,                   # Should fail! IDs must be gt=0
            "name": "Corrupted Data",
            "username": "bad_user",
            "email": "not-an-email",    # Should fail! Invalid email format
            "phone": "000",
            "website": "malicious.site"
        }
    ]

# Step 2: The Core Logic Validation Test
def test_pipeline_ingestion_and_quality_gate(mock_raw_stream_data):
    # Execute the raw validation splitter engine
    valid, invalid = ingest_payloads(mock_raw_stream_data)
    
    # Assertions: Confirm your Pydantic rules isolated the rows accurately
    assert len(valid) == 1       # Jane Doe should slide right through
    assert len(invalid) == 1     # The corrupted block should be isolated 
    
    # Confirm structural dictionary serialization 
    assert valid[0]["id"] == 10
    assert invalid[0]["index"] == 1