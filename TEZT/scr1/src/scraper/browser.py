# scraper/browser.py

from playwright.async_api import async_playwright
from config import BROWSER_SETTINGS


async def setup_browser():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True)
    context = await browser.new_context(**BROWSER_SETTINGS)
    return playwright, browser, context
