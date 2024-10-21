# scraper/browser.py

from playwright.async_api import async_playwright
from src.config import BROWSER_SETTINGS, USER_AGENT
from rich.traceback import install

install(show_locals=True)


async def setup_browser():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True)
    context = await browser.new_context(**BROWSER_SETTINGS, user_agent=USER_AGENT)
    return playwright, browser, context
