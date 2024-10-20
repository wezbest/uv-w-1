from playwright.sync_api import sync_playwright
from datetime import datetime, timezone
from rich import print as rprint  # For rprinting
from rich.traceback import install

install(show_locals=True)

# Target and userAgent
urls = [
    "https://www.coingecko.com/",
    "https://www.femscat.com/main.php",
    "https://www.meanbitches.com/",
]
uA = "Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"
c_d = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


# Actual Code here
def m_F22():
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

        rprint("[bold yellow]Looping through URLs...[/bold yellow]")
        for index, pageVisit in enumerate(urls):
            rprint(f"[bold blue]Visiting URL: {pageVisit}...[/bold blue]")
            # Create a new page
            page1 = context.new_page()

            # Visit the page specified
            page1.goto(pageVisit)

            rprint(f"[bold cyan]Taking screenshot of {pageVisit}...[/bold cyan]")
            # Create screenshot - with current date time
            page1.screenshot(path=f"clicks/{c_d}-s{index+1}.png", full_page=True)

            rprint(f"[bold green]Closing page {pageVisit}...[/bold green]")
            # Close the page
            page1.close()

        rprint("[bold yellow]Closing browser context and browser...[/bold yellow]")
        # Close the context and browser
        context.close()
        br1.close()

        rprint("[bold magenta]Done! URLs: [/bold magenta]")
        rprint(f"[bold cyan]{urls}[/bold cyan]")


m_F22()
