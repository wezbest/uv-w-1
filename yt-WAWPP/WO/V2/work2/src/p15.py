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


def rename_video_file(video_path, destination_path):
    """
    Rename a video file from the specified path to the destination path.

    Args:
        video_path (str): The path to the video file to be renamed.
        destination_path (str): The desired path for the renamed video file.

    Returns:
        bool: True if the file was successfully renamed, False otherwise.
    """
    try:
        os.rename(video_path, destination_path)
        return True
    except FileNotFoundError:
        print(f"[bold red]Video file not found: {video_path}[/bold red]")
        return False
    except Exception as e:
        print(f"[bold red]Error renaming video file: {e}[/bold red]")
        return False


def wait_for_video_file(video_path, timeout=10):
    """
    Wait for a video file to be created at the specified path.

    Args:
        video_path (str): The path to the video file to be created.
        timeout (int): The maximum number of seconds to wait for the file to be created.

    Returns:
        bool: True if the file was created within the specified timeout, False otherwise.
    """
    start_time = time.time()
    while not os.path.exists(video_path) and time.time() - start_time < timeout:
        time.sleep(0.1)
    return os.path.exists(video_path)


def rename_video_file_after_creation(video_path, destination_path):
    """
    Rename a video file after it has been created at the specified path.

    Args:
        video_path (str): The path to the video file to be created.
        destination_path (str): The desired path for the renamed video file.

    Returns:
        bool: True if the file was successfully created and renamed, False otherwise.
    """
    if wait_for_video_file(video_path):
        return rename_video_file(video_path, destination_path)
    else:
        return False


def p15F():
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
                video_path = f"clicks/video-{domain}.webm"
                destination_path = f"clicks/{c_d}-{domain}.webm"
                if rename_video_file_after_creation(video_path, destination_path):
                    rprint(
                        f"[bold green]Renamed video file for {pageVisit}...[/bold green]"
                    )
                else:
                    rprint(
                        f"[bold red]Failed to create or rename video file for {pageVisit}...[/bold red]"
                    )

        finally:
            rprint("[bold yellow]Closing browser context and browser...[/bold yellow]")
            # Close the context and browser
            context.close()
            br1.close()
            os.system("ls -al clicks/")

        rprint("[bold magenta]Done! URLs: [/bold magenta]")
        rprint(f"[bold cyan]{urls}[/bold cyan]")
