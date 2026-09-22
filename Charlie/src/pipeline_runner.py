import yaml
from pathlib import Path 
from src.extractors import fetch_weather, fetch_transit
from src.parsers import parse_weather, parse_transit
from src.utils.logging import setup_logger

logger = setup_logger()

def run_pipeline():
    config_path = Path(__file__).resolve().parents[1] / "config" / "architecture_config.yaml"
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    weather_url = config["api_endpoints"]["weather_url"]
    transit_url = config["api_endpoints"]["transit_url"]
    
    weather_raw = fetch_weather(weather_url)
    transit_raw = fetch_transit(transit_url)

    logger.info("Passing payloads to validation parsers...")
    weather_df = parse_weather(weather_raw)
    transit_df = parse_transit(transit_raw)

    if not weather_df.empty and not transit_df.empty:
        logger.info("--- VALIDATION & PARSING SUCCESSFUL ---")
        logger.info(f"Weather rows generated: {len(weather_df)}")
        logger.info(f"Transit routes validated:\n{transit_df[['route_id', 'status']]}")
    else:
        logger.error("Data tracking dropped during structural conversion.")

if __name__ == "__main__":
    run_pipeline()
