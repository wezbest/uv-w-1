import os
import asyncio
import json
from datetime import datetime
import logging
from typing import List
from src.utils import *

from rich import print as rprint
from rich.panel import Panel
from rich.logging import RichHandler
from rich.console import Console
from rich.progress import track
from rich.tree import Tree

from playwright.async_api import async_playwright, Page


# Main function orchestrating the scraping
async def sniff():
    rprint(
        Panel(
            """Scraping 1st page of Issues and Prs, may not work with older repos""",
            title="[#87ff00][italic]Github Issues and Prs Scraper",
            border_style="#d700d7",
        )
    )

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

        # Stealthy modifications to avoid detection
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
            try:
                await scrape_github_issues_and_prs(repo_name, issue_url, pr_url, page)
                log.info(f"[green]Successfully scraped {repo_name}[/green]")
                console.line()
                console.rule(
                    f"[green]{repo_name} scrape successful[/green]", style="green"
                )
            except Exception as e:
                log.error(f"[red]Failed to scrape {repo_name}: {str(e)}[/red]")
                console.line()
                console.rule(f"[red]{repo_name} scrape failed[/red]", style="red")

        await browser.close()
    console.print()  # Add a blank line for spacing
    list_reports_directory()
