import logging
import sys

def setup_logger(name: str = "charlie", log_level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    formatter = logging.Formatter(
        fmt="[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%SZ"
    )

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger