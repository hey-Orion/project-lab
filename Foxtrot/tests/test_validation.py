from src.validation import validate_records


def test_validate_records_success():

    records = [
        {
            "id": 1,
            "products": [
                {
                    "id": 101,
                    "title": "Phone",
                    "price": 100.0,
                    "quantity": 2,
                    "total": 200.0,
                    "discountPercentage": 10.0,
                    "discountedTotal": 180.0,
                    "thumbnail": "image.jpg"
                }
            ],
            "total": 200.0,
            "discountedTotal": 180.0,
            "totalProducts": 1,
            "totalQuantity": 2
        }
    ]

    valid_records, invalid_records = validate_records(records)

    assert len(valid_records) == 1
    assert len(invalid_records) == 0


def test_validate_records_failure():

    records = [
        {
            "id": -1,
            "products": [],
            "total": -100,
            "discountedTotal": 50,
            "totalProducts": 0,
            "totalQuantity": 0
        }
    ]

    valid_records, invalid_records = validate_records(records)

    assert len(valid_records) == 0
    assert len(invalid_records) == 1