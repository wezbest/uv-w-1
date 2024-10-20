import asyncio
from playwright.async_api import async_playwright
from rich.logging import RichHandler
import logging
from datetime import datetime
from urllib.parse import urlparse
from rich.traceback import install

install(show_locals=True)

# Playwright Stealth settings
STEALTH_SETTINGS = {
    "bypassCSP": True,
    "stealth": True,
    "headless": True,  # Set headless mode to True
    "slowMo": 50,
    "devtools": False,
}

# URLs to scrape
URLS = [
    "https://porngifs.xxx/",
    "https://pornhub.com/",
    # Add more URLs to this list
]

# User Agent
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
    browser = await p.chromium.launch(
        headless=STEALTH_SETTINGS["headless"],  # Set headless mode
        args=["--no-sandbox", "--disable-setuid-sandbox"],
    )
    context = await browser.new_context(
        user_agent=USER_AGENT,
        locale="de-DE",
        geolocation={"longitude": -43.1729, "latitude": -22.9068},
        permissions=["geolocation"],
        record_video_dir="panties/",
        record_video_size={"width": 1280, "height": 720},
    )
    page = await context.new_page()
    await page.evaluate_on_new_document(
        """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => false,
        });
        """
    )
    await page.evaluate_on_new_document(
        """
        Object.defineProperty(navigator, 'languages', {
          get: () => ['en-US', 'en'],
        });
        """
    )
    await page.evaluate_on_new_document(
        """
        const newProto = navigator.__proto__;
        delete newProto.webdriver;
        """
    )
    return p, browser, context, page


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
    # Scroll to bottom of page
    await page.evaluate("window.scrollTo(0, document.body.scrollHeight);")


async def capture_screenshot(page, url):
    # Take a screenshot
    screenshot_name = url.split("/")[-2] + ".png"
    await page.screenshot(path=f"panties/{screenshot_name}")
    logger.info(f"Screenshot saved as screenshots/{screenshot_name}")


async def perform_action_on_page(page, url):
    # Enter search query
    await page.fill("input#searched-query", "ass")
    await page.press("input#searched-query", "Enter")
    logger.info("Search query entered: ass")

    await scroll_to_bottom(page)
    await capture_screenshot(page, url)
    logger.info(f"Recording video to panties/{get_filename(url, 'webm')}")
    await asyncio.sleep(5)  # Record for 5 seconds


async def s1s():
    p, browser, context, page = await setup_browser()
    for url in URLS:
        try:
            if await navigate_and_check_url(page, url):
                await perform_action_on_page(page, url)
        except Exception as e:
            logger.exception(f"An error occurred: {str(e)}")
        finally:
            await context.close()
    await browser.close()
    await p.stop()
    logger.info("All videos saved")
