import yaml
from pathlib import Path 
from src.extractors import fetch_weather
from src.utils.logging import setup_logger

logger = setup_logger()

def run_extraction_sanity_check():
    config_path = Path(__file__).resolve().parents[1] / "config" / "architecture_config.yaml"
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    weather_url = config["api_endpoints"]["weather_url"]

    weather_event = fetch_weather(weather_url)

    if weather_event:
        logger.info("--- SMOKE TEST SUCCESSFUL ---")
        logger.info(f"Event UUID: {weather_event['event_id']}")
        logger.info(f"Payload Keys: {list(weather_event['payload'].keys())}")
    else:
        logger.error("Extraction smoke test failed.")

if __name__ == "__main__":
    run_extraction_sanity_check()
