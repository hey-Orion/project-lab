import os
import time
import json
import yaml
import logging
import sys
import requests
import pandas as pd

from typing import Optional
from datetime import datetime
from dotenv import load_dotenv
from requests.exceptions import RequestException
from pydantic import BaseModel, Field, EmailStr, ValidationError

load_dotenv()

API_URL = os.getenv("API_URL")


with open("Alpha/config/main_config.yaml", "r") as file:
    config = yaml.safe_load(file)

os.makedirs("Alpha/logs", exist_ok=True)

# --- FIXED LOGGING CONFIGURATION ---
# We configure the handlers manually to guarantee UTF-8 encoding on Windows
file_handler = logging.FileHandler("Alpha/logs/pipeline.log", encoding="utf-8")
console_handler = logging.StreamHandler(sys.stdout)

# Force the console handler to use UTF-8 if it's available, bypassing the Windows CP1252 default
if hasattr(console_handler.stream, "reconfigure"):
    console_handler.stream.reconfigure(encoding="utf-8")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[file_handler, console_handler]
)

logger = logging.getLogger("Alpha")


def fetch_api_data(url: str, retries: int = 2, delay: int = 1) -> list:

    for attempt in range(retries + 1):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()

            logger.info("API data fetched successfully")

            return response.json()

        except RequestException as e:

            if attempt == retries:
                logger.error(
                    f"API request failed after {retries} retries"
                )
                raise RuntimeError("Failed to fetch API data") from e

            time.sleep(delay)
            delay *= 2


class Users(BaseModel):
    id: int = Field(gt=0)
    name: str
    username: str
    email: EmailStr
    phone: str
    website: str
    timestamp: Optional[datetime] = Field(
        default_factory=datetime.now
    )


def ingest_payloads(raw_records: list) -> tuple[list, list]:
    valid = []
    invalid = []

    for idx, raw_item in enumerate(raw_records):

        try:
            model = Users.model_validate(raw_item)
            valid.append(model.model_dump())

        except ValidationError as e:
            invalid.append(
                {
                    "index": idx,
                    "errors": e.errors(),
                    "raw": raw_item,
                }
            )

    return valid, invalid


def valid_to_csv(valid_records: list) -> None:

    if not valid_records:
        logger.info("No valid records found")
        return

    output_csv = config["paths"]["valid"]
    chunk_size = config["processing"]["chunk_size"]

    os.makedirs(
        os.path.dirname(output_csv),
        exist_ok=True
    )

    df = pd.DataFrame(valid_records)

    for i in range(0, len(df), chunk_size):
        chunk = df.iloc[i:i + chunk_size]

        # FIX: "w" on the first chunk clears out the old file from previous runs.
        # "a" on subsequent chunks safely appends the rest of the current run.
        current_mode = "w" if i == 0 else "a"
        
        # FIX: Only write the header on the very first chunk
        include_header = True if i == 0 else False

        chunk.to_csv(
            output_csv,
            mode=current_mode,
            index=False,
            header=include_header
        )

    logger.info(
        f"Saved {len(valid_records)} valid records to {output_csv}"
    )


def invalid_to_json(invalid_records: list) -> None:

    if not invalid_records:
        logger.info("No invalid records found")
        return

    error_log_path = config["paths"]["invalid_json"]

    os.makedirs(
        os.path.dirname(error_log_path),
        exist_ok=True
    )

    with open(
        error_log_path,
        "a",
        encoding="utf-8"
    ) as file:

        for record in invalid_records:
            file.write(
                json.dumps(record) + "\n"
            )

    logger.info(
        f"Saved {len(invalid_records)} invalid records to {error_log_path}"
    )


def transform_records() -> pd.DataFrame:
    valid_csv_path = config["paths"]["valid"]

    if not os.path.exists(valid_csv_path):
        logger.warning(f"Bronze file {valid_csv_path} does not exist yet.")
        return pd.DataFrame()

    df = pd.read_csv(valid_csv_path)
    
    if "id" not in df.columns:
        logger.error(f"Required column 'id' missing in {valid_csv_path}.")
        return pd.DataFrame()

    # --- ADD THIS TO REMOVE DUPLICATES ---
    # Keeps the last occurrence (most recent timestamp) and drops older duplicates
    df = df.drop_duplicates(subset=["id"], keep="last")
    # -------------------------------------

    df = df.dropna(subset=["id"])
    df["email"] = df["email"].str.strip().str.lower()
    df["username"] = df["username"].str.strip().str.lower()
    df["website"] = df["website"].fillna("N/A")
    df["timestamp"] = df["timestamp"].fillna(datetime.now().isoformat())

    logger.info(f"Successfully transformed {len(df)} unique records")
    return df


def main():
    logger.info(
        "🎬 Starting Alpha Data Pipeline Process..."
    )

    # 1. Extraction Tier
    if not API_URL:
        logger.error(
            "Environment configuration missing: API_URL variable not loaded."
        )
        return

    raw_payloads = fetch_api_data(API_URL)

    if not raw_payloads:
        logger.warning(
            "Pipeline run completed early: No raw records fetched from target stream."
        )
        return

    valid, invalid = ingest_payloads(raw_payloads)

    valid_to_csv(valid)
    invalid_to_json(invalid)

    clean_df = transform_records()


    logger.info(
        "🎉Data Pipeline run executed successfully."
    )


if __name__ == "__main__":
    main()