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
    jb_line = []
    lbj_line = []
    for game in games:
        home_map, away_map = get_game_stats(game)
        if "Jimmy Butler" in home_map:
            jb = home_map["Jimmy Butler"]
            lbj = away_map["LeBron James"]
        else:
            jb = away_map["Jimmy Butler"]
            lbj = home_map["LeBron James"]
        for t in jb:
            if t[0] == "Points":
                jb_line.append(float(t[1]))
        for t in lbj:
            if t[0] == "Points":
                lbj_line.append(float(t[1]))
    gb.add_line(jb_line, "Jimmy Butler")
    gb.add_line(lbj_line, "LeBron James")
    gb.build_line_graph()
    gb.display()
    

if __name__ == "__main__":
    main()