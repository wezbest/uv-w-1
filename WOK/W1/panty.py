# Main entry point for the typer cli
import typer
from rich import print
from src.banner.b2 import pussy
from src.sc1.s1 import s1

# panty = typer.Typer(name="AssSniff")

###### Custom error handler
panty = typer.Typer(
    help="Panty - A lovely utility tool",
)


# Geenral Command Test 1
@panty.command()
def drive():
    pussy()
    print("hello")


# General command Test 2
@panty.command()
def drive2():
    pussy()
    print("hello Sniff")


# Scraper Commad Here
@panty.command()
def scrape():
    """Command executes scraping pussy"""
    print("[red] Scraping Panty [/red]")
    s1()


if __name__ == "__main__":
    panty()
