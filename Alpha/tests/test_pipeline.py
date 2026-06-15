import pytest

from Alpha.main import ingest_payloads


@pytest.fixture
def valid_record():
    return {
        "id": 10,
        "name": "Jane Doe",
        "username": " JANE_DOE ",
        "email": "JANE@Domain.Com",
        "phone": "555-1234",
        "website": "malicious.site",
        "timestamp": "2026-06-15T20:00:00"
    }


@pytest.fixture
def invalid_record():
    return {
        "id": -5,
        "name": "Corrupted Data",
        "username": "bad_user",
        "email": "not-an-email",
        "phone": "000",
        "website": "malicious.site"
    }


def test_valid_record_passes_quality_gate(valid_record):
    valid, invalid = ingest_payloads([valid_record])

    assert len(valid) == 1
    assert len(invalid) == 0

    assert valid[0]["id"] == 10
    assert valid[0]["name"] == "Jane Doe"


def test_invalid_record_fails_quality_gate(invalid_record):
    valid, invalid = ingest_payloads([invalid_record])

    assert len(valid) == 0
    assert len(invalid) == 1

    assert invalid[0]["index"] == 0


def test_mixed_records_are_separated_correctly(
    valid_record,
    invalid_record
):
    valid, invalid = ingest_payloads(
        [
            valid_record,
            invalid_record
        ]
    )

    assert len(valid) == 1
    assert len(invalid) == 1

    assert valid[0]["id"] == 10
    assert invalid[0]["index"] == 1