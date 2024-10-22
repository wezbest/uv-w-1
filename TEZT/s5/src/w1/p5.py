import os
import asyncio
import json
from datetime import datetime
import logging
from typing import List

from rich.logging import RichHandler
from rich import print
from rich.console import Console
from rich.progress import track

from playwright.async_api import async_playwright, Page

# Setting up rich logger
logging.basicConfig(
    level=logging.INFO, format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)
log = logging.getLogger("rich")
console = Console()


# Create a 'reports' folder if it doesn't exist
def ensure_reports_folder():
    reports_folder = "reports"
    if not os.path.exists(reports_folder):
        os.makedirs(reports_folder)
        log.info(f"[green]Created reports folder at: {reports_folder}[/green]")
    return reports_folder


# Function to read user-agent from file or use default
def get_user_agent(file_path: str) -> str:
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
    reports_folder = ensure_reports_folder()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_path = os.path.join(
        reports_folder, f"{website_name}_screenshot_{timestamp}.png"
    )
    await page.screenshot(path=screenshot_path, full_page=True)
    log.info(f"[cyan]Screenshot saved at {screenshot_path}[/cyan]")


# Function to store data as JSON and text file
# Function to store data as JSON and text file
def store_results_as_files(repo_name: str, issues: List[str], prs: List[str]) -> None:
    """
    Stores the scraped issues and PRs in both a JSON and text file in the reports folder.
    :param repo_name: The name of the GitHub repository.
    :param issues: List of issues.
    :param prs: List of pull requests.
    """
    reports_folder = ensure_reports_folder()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    json_path = os.path.join(reports_folder, f"{repo_name}_results_{timestamp}.json")
    text_path = os.path.join(reports_folder, f"{repo_name}_results_{timestamp}.txt")

    # Debugging logs to check if issues/PRs were scraped correctly
    if not issues and not prs:
        log.warning(f"[red]No issues or PRs found for {repo_name}[/red]")

    # Save results as JSON
    with open(json_path, "w") as json_file:
        json.dump({"issues": issues, "prs": prs}, json_file, indent=4)
        log.info(f"[cyan]Results saved as JSON at {json_path}[/cyan]")

    # Save results as text
    with open(text_path, "w") as text_file:
        text_file.write("Issues:\n")
        if issues:
            text_file.write("\n".join(issues) + "\n")
        else:
            text_file.write("No issues found.\n")

        text_file.write("\nPull Requests:\n")
        if prs:
            text_file.write("\n".join(prs) + "\n")
        else:
            text_file.write("No pull requests found.\n")

        log.info(f"[cyan]Results saved as text at {text_path}[/cyan]")


# Function to scrape issues and PRs
async def scrape_github_issues_and_prs(
    repo_name: str, repo_url: str, pr_url: str, page: Page
) -> None:
    """
    Scrapes the first page of issues and pull requests from a GitHub repository.
    :param repo_name: GitHub repository name.
    :param repo_url: GitHub issues URL.
    :param pr_url: GitHub pull requests URL.
    :param page: The Playwright page instance.
    """
    log.info(f"[yellow]Scraping issues from {repo_url}...[/yellow]")
    await page.goto(repo_url)
    await page.wait_for_selector(".js-issue-row")  # Ensure the page is fully loaded

    # Scraping issue titles
    issues = await page.evaluate("""
        () => {
            return [...document.querySelectorAll('.js-issue-row .h4 a')].map(e => e.textContent.trim());
        }
    """)

    log.info(f"[cyan]Scraped {len(issues)} issues for {repo_name}[/cyan]")
    await take_screenshot(page, f"{repo_name}_issues")

    log.info(f"[yellow]Scraping PRs from {pr_url}...[/yellow]")
    await page.goto(pr_url)
    await page.wait_for_selector(".js-issue-row")  # Ensure the page is fully loaded

    # Scraping PR titles
    prs = await page.evaluate("""
        () => {
            return [...document.querySelectorAll('.js-issue-row .h4 a')].map(e => e.textContent.trim());
        }
    """)

    log.info(f"[cyan]Scraped {len(prs)} PRs for {repo_name}[/cyan]")
    await take_screenshot(page, f"{repo_name}_prs")

    # Store results in files
    store_results_as_files(repo_name, issues, prs)


# Function to read repo names from the file
def read_repo_names(file_path: str) -> List[str]:
    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
        log.error(
            f"[red]Repository file is either empty or does not exist: {file_path}[/red]"
        )
        raise FileNotFoundError("Repository file is empty or missing.")
    with open(file_path, "r") as file:
        repos = [line.strip() for line in file if line.strip()]
        log.info(f"[green]Read {len(repos)} repositories from {file_path}[/green]")
        return repos


# Main function orchestrating the scraping
async def sniff():
    repo_file = "config/repos.txt"
    user_agent_file = "config/useragent.txt"

    # Read repository names
    repo_names = read_repo_names(repo_file)

    # Convert repository names to GitHub URLs
    urls = [
        (f"https://github.com/{repo}/issues", f"https://github.com/{repo}/pulls")
        for repo in repo_names
    ]

    # Get the user agent string
    user_agent = get_user_agent(user_agent_file)

    # Launch Playwright in headless mode
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent=user_agent, viewport={"width": 1280, "height": 720}
        )

        # Apply stealthy modifications to avoid detection
        await context.add_init_script("""
            () => {
                Object.defineProperty(navigator, 'webdriver', { get: () => false });
                Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
                Object.defineProperty(navigator, 'platform', { get: () => 'Win32' });
            }
        """)

        # Loop through the repositories and scrape issues and PRs
        for repo_name, (issue_url, pr_url) in track(
            zip(repo_names, urls), description="[green]Scraping repositories...[/green]"
        ):
            page = await context.new_page()
            await scrape_github_issues_and_prs(repo_name, issue_url, pr_url, page)

        await browser.close()
