from rich.traceback import install
import asyncio
from rich.console import Console
from src.b import pussy
from src.w import sniff

install(show_locals=True)
console = Console()

### Code ###


def main():
    pussy()
    asyncio.run(sniff())
    console.rule("[bright green] DONE [/bright green]", style="green")


if __name__ == "__main__":
    main()
