from playwright.sync_api import sync_playwright
from datetime import datetime, timezone
from rich import print as rprint  # For rprinting
from rich.traceback import install
import os
import time

install(show_locals=True)

# Target and userAgent
urls = [
    "https://www.coingecko.com/",
    "https://www.femscat.com/main.php",
    "https://www.meanbitches.com/",
]
uA = "Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"
c_d = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


def p12F():
    """All operations will be in this function"""
    rprint("[bold magenta]Starting Playwright Script...[/bold magenta]")
    with sync_playwright() as p:
        rprint("[bold cyan]Launching Chromium Browser...[/bold cyan]")
        br1 = p.chromium.launch()

        rprint("[bold green]Creating a new browser context...[/bold green]")
        context_config = {
            "record_video_dir": "clicks/",
            "record_video_size": {"width": 640, "height": 480},
            "user_agent": uA,
            "locale": "de-DE",
            "timezone_id": "Europe/Berlin",
        }
        context = br1.new_context(**context_config)

        try:
            rprint("[bold yellow]Looping through URLs...[/bold yellow]")
            for index, pageVisit in enumerate(urls):
                rprint(f"[bold blue]Visiting URL: {pageVisit}...[/bold blue]")
                # Create a new page
                page1 = context.new_page()

                # Visit the page specified
                page1.goto(pageVisit)

                # Extract the domain name from the URL
                domain = pageVisit.split("//")[-1].split("/")[0]

                rprint(f"[bold cyan]Taking screenshot of {pageVisit}...[/bold cyan]")
                # Create screenshot - with current date time and domain name
                page1.screenshot(path=f"clicks/{c_d}-{domain}.png", full_page=True)

                rprint(f"[bold green]Closing page {pageVisit}...[/bold green]")
                # Close the page
                page1.close()

                # Wait for the video file to be created
                time.sleep(2)

                # Rename the video file to the domain name
                for filename in os.listdir("clicks/"):
                    if filename.startswith("video-") and filename.endswith(".webm"):
                        os.rename(f"clicks/{filename}", f"clicks/{c_d}-{domain}.webm")

        finally:
            rprint("[bold yellow]Closing browser context and browser...[/bold yellow]")
            # Close the context and browser
            context.close()
            br1.close()
            os.system("ls -al clicks/")

        rprint("[bold magenta]Done! URLs: [/bold magenta]")
        rprint(f"[bold cyan]{urls}[/bold cyan]")
