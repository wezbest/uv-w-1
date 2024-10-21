import os
import datetime
import logging
from rich import print
from rich.logging import RichHandler
from src.config import GEOLOCATION, OUTPUT_DIRS, USER_AGENT
from rich.traceback import install

install(show_locals=True)


def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = RichHandler()
    logger.addHandler(handler)
    logger.markup = True
    return logger


logger = setup_logger()


async def scrape_website(page, url):
    logger.info(f"[bold blue1]Scraping[/bold blue1]: {url}")

    # Set user agent
    await page.set_user_agent(USER_AGENT)

    # Navigate to the URL
    await page.goto(url, wait_until="networkidle")

    # Set geolocation to Thailand (Bangkok)
    context = page.context
    await context.set_geolocation({"latitude": 13.7563, "longitude": 100.5018})
    await context.grant_permissions(["geolocation"])

    # Get the current date and time
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Take a screenshot
    screenshot_path = os.path.join(
        OUTPUT_DIRS["screenshots"], f"{url.split('//')}_{timestamp}.png"
    )
    await page.screenshot(path=screenshot_path, full_page=True)
    logger.info(f"[green]Screenshot saved[/green]: {screenshot_path}")

    # Record a video
    video_path = os.path.join(
        OUTPUT_DIRS["videos"], f"{url.split('//')}_{timestamp}.webm"
    )
    try:
        await context.tracing.start(screenshots=True, snapshots=True, sources=True)
        await page.reload()  # Trigger some action for the video
        await context.tracing.stop(path=video_path)
        logger.info(f"[green]Video saved[/green]: {video_path}")
    except Exception as e:
        logger.error(f"[bold red]Error recording video[/bold red]: {str(e)}")


async def process_url(context, url):
    page = await context.new_page()
    try:
        await scrape_website(page, url)
    except Exception as e:
        logger.error(f"[bold red]Error scraping[/bold red] {url}: {str(e)}")
    finally:
        await page.close()
