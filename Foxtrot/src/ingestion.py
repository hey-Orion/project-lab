import requests
from typing import Any


def fetch_data(url: str, timeout: int = 5) -> list[dict[str, Any]]:

    try:
        response = requests.get(url, timeout=timeout)

        response.raise_for_status()

        data = response.json()

        # Direct list response
        if isinstance(data, list):
            return data

        # DummyJSON style response
        if isinstance(data, dict):

            if "carts" in data:
                return data["carts"]

        raise ValueError(
            "Could not find a valid list of records"
        )

    except requests.exceptions.Timeout:
        print("Request timed out")
        raise

    except requests.exceptions.ConnectionError:
        print("Failed to connect to API")
        raise

    except ValueError as e:
        print(f"Invalid response: {e}")
        raise