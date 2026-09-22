from pydantic import BaseModel, Field
from typing import List, Dict
import pandas as pd 
from src.utils.logging import setup_logger

logger = setup_logger()

class weather_payload(BaseModel):
    latitude: float
    longitude: float
    hourly: Dict[str, List]


class transit_route(BaseModel):
    route_id: str
    vehicle_id: str
    scheduled_arrival: str
    actual_arrival: str
    status: str

class transit_payload(BaseModel):
    transit_system: str
    routes: List[transit_route]


def parse_weather(event: dict) -> pd.DataFrame:

    if not event or "payload" not in event:
        logger.warning("Empty or invalid weather event provided to parser.")
        return pd.DataFrame()

    
    try:
        vali