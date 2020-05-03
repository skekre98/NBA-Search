from modules import scraper

def main():

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