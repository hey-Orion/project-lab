import os
import logging 
from pathlib import Path
from dotenv import load_dotenv
from config.settings import config

load_dotenv()

def get_logger(name: str) -> logging.Logger:

    log_dir = config["paths"]["LOGS"]
    log_dir.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level = os.getenv("LOG_LEVEL", "INFO"),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(
                log_dir / "nova.log",
                encoding="utf-8"
            ),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger(name)