import pandas as pd
from modules.scraper import get_game_stats


def main():

    games = [
        "https://www.basketball-reference.com/boxscores/202009300LAL.html",
        "https://www.basketball-reference.com/boxscores/202010020LAL.html",
        "https://www.basketball-reference.com/boxscores/202010040MIA.html",
        "https://www.basketball-reference.com/boxscores/202010060MIA.html",
        "https://www.basketball-reference.com/boxscores/202010090LAL.html",
        "https://www.basketball-reference.com/boxscores/202010110MIA.html"
    ]

    get_game_stats(games[0])

if __name__ == "__main__":
    main()