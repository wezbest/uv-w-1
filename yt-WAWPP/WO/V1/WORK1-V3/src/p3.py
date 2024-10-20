from playwright.sync_api import sync_playwright
from datetime import datetime, timezone

# Target and userAgent
urls = [
    "https://www.coingecko.com/",
    "https://coinswatch.com/",
    "https://www.meanbitches.com/",
]
uA = "Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"


def m_F3():
    """All operations will be in this function"""
    with sync_playwright() as p:
        # Launch browser
        br1 = p.chromium.launch()

        # Loop through the URLs
        for index, url in enumerate(urls):
            # Create a new browser context
            c_d = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            context_config = {
                "record_video_dir": "clicks/",
                "record_video_size": {"width": 640, "height": 480},
                "user_agent": uA,
                "locale": "de-DE",
                "timezone_id": "Europe/Berlin",
            }
            context = br1.new_context(**context_config)

            # Create a new page
            page1 = context.new_page()

            # Visit the page specified
            page1.goto(url)

            # Create screenshot
            page1.screenshot(path=f"clicks/{c_d}-s{index+1}.png", full_page=True)

            # Close the page
            page1.close()

            # Close the context
            context.close()

            # Rename the video file
            import os

            for filename in os.listdir("clicks/"):
                if filename.startswith("video-") and filename.endswith(".webm"):
                    os.rename(f"clicks/{filename}", f"clicks/{c_d}-video{index+1}.webm")

        # Close the browser
        br1.close()


m_F3()
