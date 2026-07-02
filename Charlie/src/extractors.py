import uuid
from datetime import datetime, timezone
import requests 
from src.utils.logging import setup_logger

logger = setup_logger()


def fetch_weather(url: str) -> dict:
    logger.info("fetching weather data....")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        return {
            "event_id": str(uuid.uuid4()),
            "extracted_at": datetime.now(timezone.utc).isoformat(),
            "data_source": "open_meteo",
            "payload": response.json()
            
        }
    except Exception as e:
        logger.error(f"weather fetch failed: {e}")
        return{}

def fetch_transit(url: str) -> dict:
    logger.info("fetching transit data...")
    try:
        mock_payload = {
            "transit_system": "Metropolitan Transit Authority",
            "routes": [
                {"route_id": "Line-A", "vehicle_id": "V101", "scheduled_arrival": "2026-07-02T20:00:00Z", "actual_arrival": "2026-07-02T20:04:12Z", "status": "Delayed"},
                {"route_id": "Line-B", "vehicle_id": "V205", "scheduled_arrival": "2026-07-02T20:15:00Z", "actual_arrival": "2026-07-02T20:14:55Z", "status": "On-Time"},
                {"route_id": "Line-C", "vehicle_id": "V112", "scheduled_arrival": "2026-07-02T20:30:00Z", "actual_arrival": "2026-07-02T20:41:00Z", "status": "Delayed"}
            ]
        }

        return {
            "event_id": str(uuid.uuid4()),
            "extracted_at": datetime.now(timezone.utc).isoformat(),
            "data_source": "internal_transit_feed",
            "payload": mock_payload
        }

    except Exception as e:
        logger.error(f"Transit fetch failed: {e}")
        return {}