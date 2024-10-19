# Main entry point for the typer cli 
import typer 
from rich import print

panty = typer.Typer(name="AssSniff")

@panty.command()
def drive():
    print("hello")

if __name__ == "__main__":
    panty()
