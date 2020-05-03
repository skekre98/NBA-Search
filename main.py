import os
import sys
from modules import scraper

def main():

    if sys.argv[1] and sys.argv[1] == "test":
        os.system('python -m unittest test.py')
        sys.exit()

    exit = False
    while not exit:
        query = input("NBA> ")
        if "west" in query:
            ranks = scraper.get_standings("west")
            for r in ranks:
                print(r)
            exit = True
        elif "east" in query:
            ranks = scraper.get_standings("east")
            for r in ranks:
                print(r)
            exit = True
        else:
            continue


if __name__ == "__main__":
    main()