import spacy
import pandas as pd
from datetime import date
from data.text_data import nba_words
from modules.scraper import get_player_stats
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans

nlp = spacy.load("en_core_web_sm")

"""
Function to determine if query is NBA related

Parameters
----------
query : string
    String representing user query

Returns
-------
score : int
    The certainty with which the query is NBA related
    1 ~ NBA query, 0 ~ unsure, -1 ~ Random query
"""
def isNBA(query):
    temp_query = query.lower()
    query_list = temp_query.split()
    for word in query_list:
        if word in nba_words:
            return 1
    
    doc = nlp(query)
    for ent in doc.ents:
        if ent.label_ == "ORG" or ent.label_ == "PERSON":
            return 0
    
    return -1

"""
Function to generate ranked list 
of players based on fantasy score.

Parameters
----------
n/a

Returns
-------
player_scores : list
    The ranked list of players with tuples containing
    name and score.
"""
def fantasy_recommendations():
    year = int(date.today().year)
    players = get_player_stats(year)
    player_scores = []
    for player in players:
        p_t = (player.name, player.get_fantasy_score())
        player_scores.append(p_t)
    player_scores.sort(key=lambda x:x[1], reverse=True)
    return player_scores


"""
Function to generate ranked list 
of players based on fantasy score.

Parameters
----------
n/a

Returns
-------
df : pandas.DataFrame
    The dataframe of player stats
player_map : dict
    The mapping of player name to dataframe index
"""
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

"""
Function to cluster NBA players based 
on attributes such as points, rebounds, 
assists, blocks, and field goal percentage.
The idea behind clustering players is to 
gain insights on potential trade options 
and tier lists. The clustering algorithm
of choice is KMeans.

Parameters
----------
clusters : int
    The final number of clusters desired

Returns
-------
player_clusters : list
    A 2D matrix representing the clusters 
    that were formed after KMeans
"""
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