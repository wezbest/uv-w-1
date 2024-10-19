# Main entry point for the typer cli
import typer
from rich import print
from src.banner.b1 import pussy

panty = typer.Typer(name="AssSniff")


@panty.command()
def drive():
    pussy()
    print("hello")


@panty.command()
def drive2():
    print("hello Sniff")


if __name__ == "__main__":
    panty()
