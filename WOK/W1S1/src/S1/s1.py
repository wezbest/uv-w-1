# Testing scraping logic here
import asyncio
from playwright.async_api import async_playwright

from rich.traceback import install

install(show_locals=True)

url = "https://www.sex.com/gifs/"


async def s1s():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        print(await page.title())
        await browser.close()
