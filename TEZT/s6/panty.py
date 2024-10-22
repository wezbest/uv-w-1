from rich.traceback import install
import asyncio
from src.b import pussy
from src.w import sniff

install(show_locals=True)

### Code ###


def main():
    pussy()
    asyncio.run(sniff())


if __name__ == "__main__":
    main()
