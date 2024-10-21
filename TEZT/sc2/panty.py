# main.py
from src.v1 import main as main_sniff
from src.b1 import pussy  # Import the function, not the module


def main():
    pussy()  # Run the synchronous function
    main_sniff()  # Run
