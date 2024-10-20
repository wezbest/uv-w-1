# Entry point into application actual code will be in its own subdirectory
from src.p1 import m_F1
from src.p2 import m_F2
from src.ban import banner
from rich.traceback import install

install(show_locals=True)


def main():
    print("Hello from work1!")
    banner("Running m_F2 Using DIR as a list")
    m_F2()


if __name__ == "__main__":
    main()
