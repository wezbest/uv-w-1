# This is explicitly for making the banner
from rich.console import Console
from rich.panel import Panel

console = Console()


def banner(txt):
    panel = Panel.fit(
        txt,
        title="Mistress",
        subtitle="ToiletSlave",
        style="Italic",
        border_style="magenta",
    )
    # Print the Panel
    console.print(panel)
