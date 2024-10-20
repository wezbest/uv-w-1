# Entry point into application actual code will be in its own subdirectory
from src.p5 import m_F5
from src.ban import banner
from rich.traceback import install

install(show_locals=True)


def main():
    print("Hello from work1!")
    banner("Running m_F3 Using DIR as a list \n Looping through list of website")
    m_F5()


if __name__ == "__main__":
    main()
