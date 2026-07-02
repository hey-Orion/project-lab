import os
import pathlib import Path 
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parents[2] / '.env'
load_dotenv(dotenv_path=env_path)

def storage_path(filename: str) -> Path:

    root_dir = os.getenv("DATA_ROOT_DIR", "./data")
    target_dir = Path(root_dir).resolve()

    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir / filename
