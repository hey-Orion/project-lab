def ingested_payloads(raw_records: list) -> tuple[list, list]:
    valid = []
    invalid = []

    for idx, raw_items in enumerate(raw_records):
        try:
            model = trans_raw.model_validate(raw_items)
            valid.append(model.model_dump())
        except ValidationError as e:
            invalid.append({"index": idx, "errors": e.errors(), "raw": raw_items})
        
    return valid, invalid


def ingested_payloads(raw_records: list) -> tuple[list, list]:
    valid = []
    invalid = []

    for idx, raw_items in enumerate(raw_records):
        try:
            model = trans_raw.model_validate(raw_items)
            valid.append(model.model_dump())
        except ValidationError as e:
            invalid.append({"index": idx, "errors": e.errors(), "raw": raw_items})

    return valid, invalid