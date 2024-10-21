# scraper/tasks.py

import os
import datetime
from scraper.logger import setup_logger
from config import GEOLOCATION, OUTPUT_DIRS
from rich.traceback import install

install(show_locals=True)

logger = setup_logger()


async def scrape_website(page, url):
    logger.info(f"[bold blue]Scraping[/bold blue]: {url}")

    # Navigate to the URL
    await page.goto(url, wait_until="networkidle")

    # Set geolocation to Brazil (Rio de Janeiro)
    context = page.context
    await context.set_geolocation(GEOLOCATION)
    await context.grant_permissions(["geolocation"])

    # Get the current date and time
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Take a screenshot
    screenshot_path = os.path.join(
        OUTPUT_DIRS["screenshots"], f"{url.split('//')[1]}_{timestamp}.png"
    )
    await page.screenshot(path=screenshot_path, full_page=True)
    logger.info(f"[green]Screenshot saved[/green]: {screenshot_path}")

    # Record a video
    video_path = os.path.join(
        OUTPUT_DIRS["videos"], f"{url.split('//')[1]}_{timestamp}.webm"
    )
    await context.tracing.start(screenshots=True, snapshots=True, sources=True)
    await page.reload()  # Trigger some action for the video
    await context.tracing.stop(path=video_path)
    logger.info(f"[green]Video saved[/green]: {video_path}")


async def process_url(context, url):
    page = await context.new_page()
    try:
        await scrape_website(page, url)
    except Exception as e:
        logger.error(f"[bold red]Error scraping[/bold red] {url}: {str(e)}")
    finally:
        await page.close()
