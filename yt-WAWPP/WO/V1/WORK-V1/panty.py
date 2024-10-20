# Entry point into application actual code will be in its own subdirectory
from src.p1 import m_F1
from src.ban import banner


def main():
    print("Hello from work1!")
    banner("Running m_F1 getting screnshot in clics directory")
    m_F1()


if __name__ == "__main__":
    main()
