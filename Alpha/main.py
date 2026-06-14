import os 
import time
import json
import yaml
import logging
import requests
import pandas as pd 
from datetime import datetime
from dotenv import load_dotenv
from requests.exceptions import RequestException
from pydantic import BaseModel, Field, EmailStr, ValidationError

load_dotenv()
URL = os.getenv("API_URL")

with open("config/main_config.yaml","r") as file:
    config = yaml.safe_load(file)
    
MIN = config["data_validation"]["min_amount"]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Alpha")

def fetch_api_data(url: str, retries: int = 2, delay: int = 1) -> list:
    for attempt in range(retries + 1):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            if attempt == retries:
                logger.error("[critical] error")
                raise RuntimeError("failed") from e 

            time.sleep(delay)
            delay *= 2 

    return []


class trans_raw(BaseModel):
    id: int = Field(gt=0)
    user_email: EmailStr
    amount: float = Field(gt=MIN)
    timestamp: datetime


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

