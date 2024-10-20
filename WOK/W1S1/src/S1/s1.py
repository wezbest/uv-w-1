import asyncio
from playwright.async_api import async_playwright
from rich.logging import RichHandler
import logging
from datetime import datetime
from urllib.parse import urlparse
from rich.traceback import install

install(show_locals=True)

URL = "https://porngifs.xxx/"
USER_AGENT = "Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"

# Set up Rich logger
logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)
logger = logging.getLogger("rich")


def get_filename(url, extension):
    domain = urlparse(url).netloc
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{domain}_{timestamp}.{extension}"


async def setup_browser():
    p = await async_playwright().start()
    browser = await p.chromium.launch()
    video_path = f"panties/{get_filename(URL, 'webm')}"
    context = await browser.new_context(
        user_agent=USER_AGENT,
        locale="de-DE",
        geolocation={"longitude": 13.4050, "latitude": 52.5200},
        permissions=["geolocation"],
        record_video_dir="panties/",
        record_video_size={"width": 1280, "height": 720},
    )
    return p, browser, context, video_path


async def navigate_and_check_url(page, url):
    response = await page.goto(url)
    if response.ok:
        logger.info(f"Successfully loaded URL: {response.url}")
        if response.url == url:
            logger.info("URL is correct")
        else:
            logger.warning(f"Warning: URL redirected to {response.url}")
    else:
        logger.error(f"Failed to load URL. Status: {response.status}")
    return response.ok


async def scroll_to_bottom(page):
    logger.info("Scrolling to the bottom of the page...")
    await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    await asyncio.sleep(2)  # Wait for any lazy-loaded content


async def capture_screenshot(page, url):
    screenshot_path = f"screenshots/{get_filename(url, 'png')}"
    await page.screenshot(path=screenshot_path)
    logger.info(f"Screenshot saved as {screenshot_path}")


async def main():
    p, browser, context, video_path = await setup_browser()
    page = await context.new_page()

    try:
        if await navigate_and_check_url(page, URL):
            await scroll_to_bottom(page)
            await capture_screenshot(page, URL)
            logger.info(f"Recording video to {video_path}")
            await asyncio.sleep(5)  # Record for 5 seconds
    except Exception as e:
        logger.exception(f"An error occurred: {str(e)}")
    finally:
        await context.close()
        await browser.close()
        await p.stop()
        logger.info(f"Video saved as {video_path}")
