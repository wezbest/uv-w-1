#  Downloading the following - https://playwright.dev/python/docs/introduction
# This is same work of p1.py but with changes

from playwright.sync_api import sync_playwright
from datetime import datetime, timezone

# Target and userAgent
url = [
    "https://www.coingecko.com/",
    "https://www.coinwatch.com/",
    "https://www.meanbitches.com/",
]
uA = "Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"
c_d = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


# Actual Code here
def m_F2():
    """ALl operations will be in this function"""
    with sync_playwright() as p:
        # Launch broser
        br1 = p.chromium.launch()

        # Create a new browser context
        context_config = {
            "record_video_dir": "clicks/",
            "user_agent": uA,
            "locale": "de-DE",
            "timezone_id": "Europe/Berlin",
        }
        context = br1.new_context(**context_config)

        # Create a new page
        page1 = context.new_page()

        # Visit the page specified
        page1.goto(url[2])

        # Create sreenshot - wih current date time
        page1.screenshot(path=f"clicks/{c_d}-s1.png", full_page=True)

        # Close the page and then the context
        page1.close()
        context.close()

        # Close the browser
        br1.close()
