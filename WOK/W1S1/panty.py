# Main Entry point
from src.S1.s1 import s1s
import asyncio
from rich.traceback import install

install(show_locals=True)


def main():
    print("Hello from w1s1!")
    asyncio.run(s1s())


if __name__ == "__main__":
    main()
