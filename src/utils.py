import logging
from typing import Generator, List, Any


def get_logger(name: str = "crypto_pipeline") -> logging.Logger:
    
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

    return logger


def chunk_list(lst: List[Any], size: int) -> Generator[List[Any], None, None]:
    for i in range(0, len(lst), size):
        yield lst[i:i + size]