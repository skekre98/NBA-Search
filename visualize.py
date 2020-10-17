import pandas as pd
from modules.scraper import get_game_stats
from lab.graph_builder import GraphBuilder


def main():

    games = [
        "https://www.basketball-reference.com/boxscores/202009300LAL.html",
        "https://www.basketball-reference.com/boxscores/202010020LAL.html",
        "https://www.basketball-reference.com/boxscores/202010040MIA.html",
        "https://www.basketball-reference.com/boxscores/202010060MIA.html",
        "https://www.basketball-reference.com/boxscores/202010090LAL.html",
        "https://www.basketball-reference.com/boxscores/202010110MIA.html"
    ]

    xlabels = ["Game 1", "Game 2", "Game 3", "Game 4", "Game 5", "Game 6"]
    gb = GraphBuilder(xlabels)
    for game in games:
        home_map, away_map = get_game_stats(game)
        if home_map["Jimmy Butler"]:
            jb = home_map["Jimmy Butler"]
        lbj = aw
    

if __name__ == "__main__":
    main()