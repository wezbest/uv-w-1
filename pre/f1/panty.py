from rich.traceback import install
import asyncio
from rich.console import Console
from src.banner import pussy
from src.scraper import sniff

install(show_locals=True)
console = Console()

### Code ###


def main():
    pussy()
    asyncio.run(sniff())
    console.rule(f"[green]DONE[/green]", style="green")


if __name__ == "__main__":
    main()
