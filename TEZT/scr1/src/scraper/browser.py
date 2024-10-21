# scraper/browser.py

from playwright.async_api import async_playwright
from src.config import BROWSER_SETTINGS, USER_AGENT
from rich.traceback import install
from playwright_stealth import stealth_async

install(show_locals=True)


async def setup_browser():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True)
    context = await browser.new_context(**BROWSER_SETTINGS, user_agent=USER_AGENT)

    # Use Playwright Stealth to evade detection
    await stealth_async(context)

    # Set geolocation to Thailand (Bangkok)
    await context.set_geolocation({"latitude": 13.7563, "longitude": 100.5018})
    await context.grant_permissions(["geolocation"])

    return playwright, browser, context


async def start_recording(context):
    await context.tracing.start(screenshots=True, snapshots=True, sources=True)


async def stop_recording(context, video_path):
    await context.tracing.stop(path=video_path)
