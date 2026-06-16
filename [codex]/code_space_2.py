import os
import time
import yaml
import logging
import requests
import sys
import json
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

file_handler = logging.FileHandler("Alpha/logs/pipeline.log", encoding="utf-8")
console_handler = logging.StreamHandler(sys.stdout)


