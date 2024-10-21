# scraper.py
from playwright.async_api import async_playwright
from rich.logging import RichHandler
import logging
from datetime import datetime
from rich.traceback import install
import os
import asyncio

install(show_locals=True)

# Set up logging
logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)

# Create the results directory if it doesn't exist
if not os.path.exists("results"):
    os.makedirs("results")


# Define a function to read the repository names from a text file
async def read_repos(file_name: str) -> list:
    """
    Reads the repository names from a text file.

    Args:
    file_name (str): The name of the text file containing the repository names.

    Returns:
    list: A list of repository names.
    """
    try:
        with open(file_name, "r") as file:
            repos = file.readlines()
            repos = [repo.strip() for repo in repos]
            return repos
    except FileNotFoundError:
        logging.error(
            f"[bold red]File {file_name} not found.[/bold red]", extra={"markup": True}
        )
        return []


# Define a function to generate the GitHub issue and PR URLs
async def generate_urls(repo: str) -> tuple:
    """
    Generates the GitHub issue and PR URLs for a given repository.

    Args:
    repo (str): The name of the repository in the format 'owner/repo'.

    Returns:
    tuple: A tuple containing the issue URL and the PR URL.
    """
    issue_url = f"https://github.com/{repo}/issues"
    pr_url = f"https://github.com/{repo}/pulls"
    return issue_url, pr_url


# Define a function to scrape the first page of GitHub issues and PRs
async def scrape_github(repo: str, issue_url: str, pr_url: str) -> None:
    """
    Scrapes the first page of GitHub issues and PRs for a given repository.

    Args:
    repo (str): The name of the repository in the format 'owner/repo'.
    issue_url (str): The URL of the GitHub issues page.
    pr_url (str): The URL of the GitHub PRs page.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            geolocation={"longitude": 41.890221, "latitude": 12.492348},
            permissions=["geolocation"],
        )
        page = await context.new_page()

        # Set the user agent
        user_agent = await read_user_agent()
        await page.set_user_agent(user_agent)

        # Scrape the issues page
        await page.goto(issue_url)
        issues = await page.query_selector_all(".js-issue-row")
        with open(
            f"results/{repo}_issues_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", "w"
        ) as file:
            for issue in issues:
                title = await issue.query_selector(".js-issue-title")
                if title:
                    file.write(await title.text_content() + "\n")

        # Scrape the PRs page
        await page.goto(pr_url)
        prs = await page.query_selector_all(".js-issue-row")
        with open(
            f"results/{repo}_prs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", "w"
        ) as file:
            for pr in prs:
                title = await pr.query_selector(".js-issue-title")
                if title:
                    file.write(await title.text_content() + "\n")

        await browser.close()


# Define a function to read the user agent from a text file
async def read_user_agent() -> str:
    """
    Reads the user agent from a text file.

    Returns:
    str: The user agent.
    """
    try:
        with open("useragent.txt", "r") as file:
            user_agent = file.read().strip()
            return user_agent
    except FileNotFoundError:
        logging.error(
            "[bold red]User agent file not found. Using default user agent.[/bold red]",
            extra={"markup": True},
        )
        return "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Mobile Safari/537.36"


# Define the main function
async def sniff() -> None:
    """
    The main function.
    """
    repos = await read_repos("repos.txt")
    if not repos:
        logging.error("[bold red]No repositories found.[/bold red]")
