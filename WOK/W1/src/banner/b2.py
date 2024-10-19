import logging
from rich.logging import RichHandler
import requests as rq
from rich.console import Console

console = Console()  # Sta

# Define urls
url = [
    "https://snips.sh/f/7l7_Yp0Htz?r=1",
]


def pussy() -> None:
    logging.basicConfig(
        level="DEBUG",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)],
    )
    logger = logging.getLogger(__name__)

    for x in url:
        try:
            r = rq.get(x)
            r.raise_for_status()  # Raises an HTTPError for bad responses
            logger.info(f"Success: Status code {r.status_code}")
            print(r.text)  # This will print the response text to the console
            console.rule(f"[bold green] {x} [/bold green]", style="bold green")
        except rq.RequestException as e:
            logger.error(
                f"Failed to fetch {x}. Status code: {e.response.status_code if e.response else 'N/A'}. Error: {str(e)}"
            )
            console.rule(f"[bold red] {x} [/bold red]", style="bold red")
