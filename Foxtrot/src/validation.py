from pydantic import ValidationError

from models.pydantic_models import Cart


def validate_records(records: list[dict]) -> tuple[list, list]:


    valid_records = []
    invalid_records = []

    for record in records:
        try:
            validated_record = Cart(**record)

            valid_records.append(
                validated_record.model_dump()
            )

        except ValidationError as e:
            invalid_records.append(
                {
                    "record": record,
                    "errors": e.errors()
                }
            )

    return valid_records, invalid_records
