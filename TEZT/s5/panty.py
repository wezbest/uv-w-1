from rich.traceback import install
from src.p1 import pussy
from src.w2.p1 import sniff
import asyncio

install(show_locals=True)

###############################


def main():
    print("Hello from s3!")
    pussy()
    asyncio.run(sniff())


if __name__ == "__main__":
    main()
