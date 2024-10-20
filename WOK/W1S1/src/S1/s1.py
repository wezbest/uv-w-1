# TEZT/t1/src/sc1/s1.py
import asyncio
from playwright.async_api import async_playwright
from rich import print as print

URL = "https://www.coingecko.com/"
USER_AGENT = "Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"


async def setup_browser():
    p = await async_playwright().start()
    browser = await p.chromium.launch()
    context = await browser.new_context(
        user_agent=USER_AGENT,
        locale="de-DE",
        geolocation={"longitude": 13.4050, "latitude": 52.5200},
        permissions=["geolocation"],
        record_video_dir="videos/",
        record_video_size={"width": 1280, "height": 720},
    )
    return p, browser, context


async def navigate_and_check_url(page, url):
    response = await page.goto(url)
    if response.ok:
        print(f"[green]Successfully loaded URL: {response.url}[/green]")
        if response.url == url:
            print("[green]URL is correct[/green]")
        else:
            print(f"[yellow]Warning: URL redirected to {response.url}[/yellow]")
    else:
        print(f"[red]Failed to load URL. Status: {response.status}[/red]")
    return response.ok


async def scroll_to_bottom(page):
    print("[blue]Scrolling to the bottom of the page...[/blue]")
    await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    await asyncio.sleep(2)  # Wait for any lazy-loaded content


async def capture_screenshot(page):
    await page.screenshot(path="screenshots/screenshot.png")
    print("[blue]Screenshot saved as screenshots/screenshot.png[/blue]")


async def record_video(page):
    print("[blue]Recording video...[/blue]")
    await asyncio.sleep(5)  # Record for 5 seconds
    print("[blue]Video saved in videos/ directory[/blue]")


async def s1():
    p, browser, context = await setup_browser()
    try:
        page = await context.new_page()
        if await navigate_and_check_url(page, URL):
            await scroll_to_bottom(page)
            await capture_screenshot(page)
            await record_video(page)
    except Exception as e:
        print(f"[red]An error occurred: {str(e)}[/red]")
    finally:
        await context.close()
        await browser.close()
        await p.stop()
