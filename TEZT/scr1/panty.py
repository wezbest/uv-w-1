# main.py

import asyncio
import os
from src.scraper.logger import setup_logger
from src.scraper.browser import setup_browser
from src.scraper.tasks import process_url
from src.config import URLS, OUTPUT_DIRS
from rich.traceback import install

install(show_locals=True)


async def main():
    logger = setup_logger()

    for directory in OUTPUT_DIRS.values():
        os.makedirs(directory, exist_ok=True)

    playwright, browser, context = await setup_browser()

    try:
        tasks = [process_url(context, url) for url in URLS]
        await asyncio.gather(*tasks)
    finally:
        await browser.close()
        await playwright.stop()

    logger.info("[bold green]Scraping completed![/bold green]")


if __name__ == "__main__":
    asyncio.run(main())
