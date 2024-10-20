# --- imports
from rich.traceback import install
from src.ban import banner
from src.p16 import p16F

install(show_locals=True)
# ----


def main():
    banner("Work Continuation Here")
    p16F()


if __name__ == "__main__":
    main()
