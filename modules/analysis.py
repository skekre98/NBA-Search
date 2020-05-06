from datetime import date
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans
from modules.scraper import get_player_stats


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
def create_player_dataframe():
    year = int(date.today().year)
    players = get_player_stats(year)

    # Arrays for player categories 
    ns, pnts, rbs, asts, blks, fgp = [], [], [], [], [], []
    player_map = {}

    for i, p in enumerate(players):
        player_map[i] = p.name
        ns.append(p.name)
        pnts.append(p.points)
        rbs.append(p.total_reb)
        asts.append(p.assists)
        blks.append(p.blocks)
        fgp.append(p.field_goal_percent)

    # Creating a pandas dataframe based on player categories 
    df = pd.DataFrame({
        'points': pnts,
        'rebounds': rbs,
        'assists': asts,
        'blocks': blks,
        'field goal percent': fgp
    })

    return df, player_map


# Function to cluster players based on overall stats
def build_stat_clusters(clusters):
    data, p_map = create_player_dataframe()
    km = KMeans(n_clusters=clusters).fit(data)
    cluster_map = pd.DataFrame()
    cluster_map['data_index'] = data.index.values
    cluster_map['cluster'] = km.labels_

    # cluster list 
    player_clusters = []
    # Iterate over cluster map
    for i in range(clusters):
        c = cluster_map[cluster_map.cluster == i]
        group = []
        for id, cluster in c.iterrows():
            group.append(p_map[cluster['data_index']])
        player_clusters.append(group)
    
    return player_clusters