import os
import asyncio
import time
from datetime import datetime
import logging
from typing import List

from rich.logging import RichHandler
from rich import print
from rich.console import Console
from rich.progress import track

from playwright.async_api import async_playwright, Page  # Standard Playwright

# Setting up rich logger
logging.basicConfig(
    level=logging.INFO, format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)
log = logging.getLogger("rich")
console = Console()


# Create a 'reports' folder if it doesn't exist
def ensure_reports_folder():
    """
    Ensures that the 'reports' folder exists. If it doesn't, it creates it.
    """
    reports_folder = "reports"
    if not os.path.exists(reports_folder):
        os.makedirs(reports_folder)
        log.info(f"[green]Created reports folder at: {reports_folder}[/green]")
    return reports_folder


# Function to convert repo names to URLs
def convert_to_github_urls(repo_names: List[str]) -> List[str]:
    """
    Converts repository names to GitHub URLs for issues and pull requests.
    :param repo_names: List of repo names in the form 'username/repo'.
    :return: List of URLs.
    """
    log.info("[yellow]Converting repo names to GitHub URLs...[/yellow]")
    urls = []
    for repo in repo_names:
        issue_url = f"https://github.com/{repo}/issues"
        pr_url = f"https://github.com/{repo}/pulls"
        urls.append((issue_url, pr_url))
        log.info(
            f"[cyan]Converted {repo} to Issues URL: {issue_url} and PRs URL: {pr_url}[/cyan]"
        )
    return urls


# Function to read user-agent from file or use default
def get_user_agent(file_path: str) -> str:
    """
    Retrieves the user-agent from the specified file, if it exists. Otherwise, defaults to Linux Android user-agent.
    :param file_path: Path to the user-agent file.
    :return: The user-agent string.
    """
    if os.path.exists(file_path):
        log.info(f"[green]User-agent file found: {file_path}[/green]")
        with open(file_path, "r") as file:
            user_agent = file.readline().strip()
            log.info(f"[cyan]Using user-agent from file: {user_agent}[/cyan]")
            return user_agent
    else:
        default_user_agent = "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.93 Mobile Safari/537.36"
        log.warning("[red]User-agent file not found. Using default user-agent.[/red]")
        return default_user_agent


# Function to take a screenshot and store it in the reports folder
async def take_screenshot(page: Page, website_name: str) -> None:
    """
    Takes a screenshot of the current page and saves it in the 'reports' folder.
    :param page: The Playwright page instance.
    :param website_name: The name of the website being scraped.
    """
    reports_folder = ensure_reports_folder()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_path = os.path.join(
        reports_folder, f"{website_name}_screenshot_{timestamp}.png"
    )
    await page.screenshot(path=screenshot_path, full_page=True)
    log.info(f"[cyan]Screenshot saved at {screenshot_path}[/cyan]")


# Function to record a video and store it in the reports folder
async def record_video(page: Page, website_name: str) -> None:
    """
    Records a video of the entire page while scrolling and saves it in the 'reports' folder.
    :param page: The Playwright page instance.
    :param website_name: The name of the website being scraped.
    """
    reports_folder = ensure_reports_folder()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    video_path = os.path.join(reports_folder, f"{website_name}_video_{timestamp}.webm")

    # Scroll and record the video
    await page.evaluate("""() => {
        window.scrollBy(0, document.body.scrollHeight);
    }""")
    await page.wait_for_timeout(5000)  # Wait 5 seconds while scrolling for video effect
    await page.context.close()
    log.info(f"[cyan]Video recorded and saved at {video_path}[/cyan]")


# Function to scrape issues and PRs
async def scrape_github_issues_and_prs(repo_url: str, pr_url: str, page: Page) -> None:
    """
    Scrapes the first page of issues and pull requests from a GitHub repository.
    :param repo_url: GitHub issues URL.
    :param pr_url: GitHub pull requests URL.
    :param page: The Playwright page instance.
    """
    log.info(f"[yellow]Scraping issues from {repo_url}...[/yellow]")
    await page.goto(repo_url)
    await take_screenshot(page, "github_issues")

    log.info(f"[yellow]Scraping PRs from {pr_url}...[/yellow]")
    await page.goto(pr_url)
    await take_screenshot(page, "github_prs")

    # Additionally, record videos
    await record_video(page, "github")


# Function to read repo names from the file
def read_repo_names(file_path: str) -> List[str]:
    """
    Reads the repository names from the given text file.
    :param file_path: Path to the text file containing repo names.
    :return: List of repo names.
    """
    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
        log.error(
            f"[red]Repository file is either empty or does not exist: {file_path}[/red]"
        )
        raise FileNotFoundError("Repository file is empty or missing.")

    with open(file_path, "r") as file:
        repos = [line.strip() for line in file if line.strip()]
        log.info(f"[green]Read {len(repos)} repositories from {file_path}[/green]")
        return repos


# The main function that orchestrates the scraping
async def sniff():
    repo_file = "config/repos.txt"
    user_agent_file = "config/useragent.txt"

    # Read repository names
    repo_names = read_repo_names(repo_file)

    # Convert repository names to GitHub URLs
    urls = convert_to_github_urls(repo_names)

    # Get the user agent string
    user_agent = get_user_agent(user_agent_file)

    # Launch Playwright in headless mode
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent=user_agent, viewport={"width": 1280, "height": 720}
        )

        # Apply stealthy modifications to the context before pages are opened
        await context.add_init_script(
            """
            () => {
                Object.defineProperty(navigator, 'webdriver', { get: () => false });
                Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
                Object.defineProperty(navigator, 'platform', { get: () => 'Win32' });
            }
            """
        )

        for issue_url, pr_url in track(
            urls, description="[green]Scraping repositories...[/green]"
        ):
            page = await context.new_page()

            await scrape_github_issues_and_prs(issue_url, pr_url, page)

        await browser.close()
