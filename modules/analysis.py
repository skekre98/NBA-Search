from datetime import date
import pandas as pd
from scraper import get_player_stats


# Function to recommend players for fantasy team 
def fantasy_recommendations():
    year = int(date.today().year)
    players = get_player_stats(year)
    player_scores = []
    for player in players:
        p_t = (player.name, player.get_fantasy_score())
        player_scores.append(p_t)
    player_scores.sort(key=lambda x:x[1], reverse=True)
    return player_scores


# Function to create player dataframe for clustering
def create_dataframe():
    year = int(date.today().year)
    players = get_player_stats(year)

    # Arrays for player categories 
    ns, pnts, rbs, asts, blks, fgp = [], [], [], [], [], []

    for p in players:
        ns.append(p.name)
        pnts.append(p.points)
        rbs.append(p.total_reb)
        asts.append(p.assists)
        blks.append(p.blocks)
        fgp.append(p.field_goal_percent)

    # Creating a pandas dataframe based on player categories 
    df = pd.DataFrame({
        'Player': ns,
        'points': pnts,
        'rebounds': rbs,
        'assists': asts,
        'blocks': blks,
        'field goal percent': fgp
    })

    return df