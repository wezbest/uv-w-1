import os
import datetime
import logging
import re
from rich import print
from rich.logging import RichHandler
from src.scraper.browser import start_recording, stop_recording
from src.config import GEOLOCATION, OUTPUT_DIRS, USER_AGENT
from rich.traceback import install

install(show_locals=True)


def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = RichHandler()
    logger.addHandler(handler)
    return logger


logger = setup_logger()


async def scrape_website(page, url):
    logger.info(f"[bold blue1]Scraping[/bold blue1]: {url}", extra={"markup": True})

    # Navigate to the URL
    await page.goto(url, wait_until="networkidle")

    # Set geolocation to Thailand (Bangkok)
    context = page.context
    await context.set_geolocation({"latitude": 13.7563, "longitude": 100.5018})
    await context.grant_permissions(["geolocation"])

    # Get the current date and time
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Remove special characters from the URL for the filename
    filename_safe_url = re.sub(r"\W+", "_", url.split("//")[-1])

    # Take a screenshot
    screenshot_path = os.path.join(
        "rez",
        OUTPUT_DIRS["rez"]["screenshots"],
        f"{filename_safe_url}_{timestamp}.png",
    )
    await page.screenshot(path=screenshot_path, full_page=True)
    logger.info(
        f"[green]Screenshot saved[/green]: {screenshot_path}", extra={"markup": True}
    )

    # Record a video
    video_path = os.path.join(
        "rez", OUTPUT_DIRS["rez"]["videos"], f"{filename_safe_url}_{timestamp}.webm"
    )

    try:
        # Check if recording is already in progress
        if not context.is_recording():
            # Start video recording
            await start_recording(page.context)

            # Trigger some action for the video (e.g., reload the page)
            await page.reload()

            # Wait for 5 seconds to capture the page load
            await page.wait_for_timeout(5000)

            # Stop video recording and save the video
            await stop_recording(page.context, video_path)
            logger.info(
                f"[green]Video saved[/green]: {video_path}", extra={"markup": True}
            )
        else:
            logger.warning(
                f"[yellow]Video recording already in progress for {url}[/yellow]",
                extra={"markup": True},
            )
    except Exception as e:
        logger.error(
            f"[bold red]Error recording video[/bold red]: {str(e)}",
            extra={"markup": True},
        )


async def process_url(context, url):
    page = await context.new_page()
    try:
        await scrape_website(page, url)
    except Exception as e:
        logger.error(
            f"[bold red]Error scraping[/bold red] {url}: {str(e)}",
            extra={"markup": True},
        )
    finally:
        await page.close()
