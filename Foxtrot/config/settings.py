from pathlib import Path
import yaml

CONFIG_FILE = Path("config/config.yaml")

with open(CONFIG_FILE, "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

for key, value in config["paths"].items():
    config["paths"][key] = Path(value)