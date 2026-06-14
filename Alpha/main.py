import time
import logging
import requests
from requests.exceptions import RequestException

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