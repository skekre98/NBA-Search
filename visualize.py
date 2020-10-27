import pandas as pd
from modules.scraper import get_game_stats
from lab.graph_builder import GraphBuilder
from lab.table_builder import TableBuilder


def main():

    games = [
        "https://www.basketball-reference.com/boxscores/202009300LAL.html",
        "https://www.basketball-reference.com/boxscores/202010020LAL.html",
        "https://www.basketball-reference.com/boxscores/202010040MIA.html",
        "https://www.basketball-reference.com/boxscores/202010060MIA.html",
        "https://www.basketball-reference.com/boxscores/202010090LAL.html",
        "https://www.basketball-reference.com/boxscores/202010110MIA.html"
    ]

    
    col_labels = ["Name", "Points", "Assists"]
    tb = TableBuilder(col_labels)
    rows = [
        ["Lebron James", 25.0, 12.0],
        ["Kevin Durant", 24.0, 13.0],
        ["Jimmy Butler", 23.0, 14.0]
    ]

    for row in rows:
        tb.add_row(row)
    tb.build_table()
    tb.save('table')
    
if __name__ == "__main__":
    main()