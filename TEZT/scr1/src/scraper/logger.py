# scraper/logger.py

import logging
from rich.logging import RichHandler
from rich.traceback import install

install(show_locals=True)


def setup_logger():
    logging.basicConfig(
        level="INFO",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)],
    )
    return logging.getLogger("rich")
