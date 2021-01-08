import sys
import requests
from datetime import date
from bs4 import BeautifulSoup, Comment
from difflib import SequenceMatcher
from modules.objects import Team, Player
from data.text_data import alltime_player_list
from fuzzywuzzy import fuzz, process
from data.text_data import total_stat_map, adv_stat_map

base_url = "https://www.basketball-reference.com"

"""
Function to get a map of current playoff 
scores

Parameters
----------
n/a

Returns
-------
bracket_map : dict
    A mapping of the NBA playoff bracket
"""
def get_playoff_bracket():
    year = int(date.today().year)
    url = "{}/playoffs/NBA_{}.html".format(base_url, str(year))
    resp = requests.get(url)
    page_content = BeautifulSoup(resp.content, "html.parser")
    table = page_content.findAll("tr")
    bracket_map = {
        "Western Conference First Round" : [],
        "Eastern Conference First Round" : [],
        "Western Conference Semifinals" : [],
        "Eastern Conference Semifinals" : [],
        "Western Conference Finals" : [],
        "Eastern Conference Finals" : [],
        "Finals" : []
    }

    for row in table:
        td_list = row.findAll("td")
        a_list = row.findAll("a")
        level = None
        if td_list:
            for t in td_list:
                if t.string in bracket_map:
                    level = t.string
        
        if level:
            team1 = a_list[0].string
            team2 = a_list[1].string
            curr_score = a_list[1].next_sibling.string
            score1 = curr_score[3]
            score2 = curr_score[5]
            cell = [(team1, str(score1)), (team2, str(score2))]
            bracket_map[level].append(cell)

    return bracket_map
    


"""
Function to get a list of player names
from specific year

Parameters
----------
year : int
    The year to scrape for NBA player
    names

Returns
-------
player_list : list
    The list of player names
"""
def get_player_names(year):
    url = "{}/leagues/NBA_{}_per_game.html".format(base_url, str(year))
    resp = requests.get(url)
    page_content = BeautifulSoup(resp.content, "html.parser")
    table = page_content.findAll("tr",attrs={"class":"full_table"})
    names = []
    for row in table:
        name = row.find("a").string
        names.append(name)
    return names


"""
Function to get a list of player objects 
with player stats

Parameters
----------
table : bs4.element.ResultSet
    BeautifulSoup object with player stats

Returns
-------
player_list : list
    The list of player objects with scraped stats
"""
def get_stat_list(table):
    player_list = []
    for row in table:
        name = row.find("a").string
        player = Player(name)
        attr = {}
        stats = row.findAll("td")
        for stat in stats:
            attr[stat["data-stat"]] = stat.string
        player.create(attr)
        player_list.append(player)
    return player_list

"""
Function to get current NBA standings in
the east, west, or entire NBA.

Parameters
----------
conf : str
    The requested conference standings

Returns
-------
standings : list
    The ranked list of teams to signify standings
"""
def get_standings(conf):
    resp = requests.get(base_url)
    page_content = BeautifulSoup(resp.content, "html.parser")
    table = page_content.findAll("tr",attrs={"class":"full_table"})

    # Iterate over ranking table in website HTML 
    standings = []
    for i,row in enumerate(table):
        team = row.find("a").get("title")
        wins = row.find("td",attrs={"data-stat":"wins"}).string
        losses = row.find("td",attrs={"data-stat":"losses"}).string
        team_map = {
            "name" : team,
            "wins" : wins,
            "losses" : losses
	    }
        standings.append(team_map)
        if i == 29:
            break
    
    # Return rankings based on conference 
    switch = {
        "all" : standings,
        "east": standings[:15],
        "west": standings[15:]
    }

    return switch.get(conf, "Invalid Conference")

"""
Function to get the player efficiency
rating for all NBA players in a specific
year

Parameters
----------
year : int
    The year to scrape for NBA player
    efficiency rating

Returns
-------
per_list : list
    The list of tuples with player name and PER
"""
def get_per(year):
    url = "{}/leagues/NBA_{}_advanced.html".format(base_url, str(year))
    resp = requests.get(url)
    page_content = BeautifulSoup(resp.content, "html.parser")
    table = page_content.findAll("tr",attrs={"class":"full_table"})
    per_list = []
    for row in table:
        name = row.find("a").string
        
        per = 0.0
        stats = row.findAll("td")
        for stat in stats:
            if stat["data-stat"] == "per" and stat.string:
                per = float(stat.string)
        per_list.append((name, per))
    return per_list

"""
Function to get the player name for a given
search string

Parameters
----------
query : string
    user-inputted query (as determined by
    NLP)

Returns
-------
target_name : string from `alltime_player_list`
"""
def get_target_name(query):
    target_name, ratio = process.extractOne(query, alltime_player_list, scorer=fuzz.partial_token_sort_ratio)

    return target_name

"""
Function to get the player URL for a given 
target_name from `alltime_player_list`

Parameters
----------
target_name : string
    from `alltime_player_list`

Returns
-------
url : string
"""
def get_player_url(target_name):
    ln_initial = target_name.split()[-1][0].lower()
    url = "{}/players/{}/".format(base_url, ln_initial)

    resp = requests.get(url)
    page_content = BeautifulSoup(resp.content, "html.parser")
    th = page_content.findAll("th")
    for row in th:
        a = row.find("a")
        if a and a.string == target_name:
            url = base_url + a["href"]
    
    return url

"""
Function to get the total statistic
for NBA player career

Parameters
----------
name : string
    NBA player for stat retrieval
stat : string
    statistic to return

Returns
-------
stat_list : list
    The list of tuples with player name and PER
"""
def get_total_stat(name, stat):
    target_name = get_target_name(name)
    url = get_player_url(target_name)
    resp = requests.get(url)
    page_content = BeautifulSoup(resp.content, "html.parser")
    tfoot_soup = page_content.find("tfoot")
    stat_tag = total_stat_map[stat]
    stat_td = tfoot_soup.find("td", attrs={"data-stat":stat_tag})
    return float(stat_td.string) if stat_td else 0.0

"""
Function to get the advanced statistic
for NBA player career

Parameters
----------
name : string
    NBA player for stat retrieval
stat : string
    statistic to return

Returns
-------
stat_list : list
    The list of tuples with player name and PER
"""
def get_adv_stat(name, stat):
    target_name = get_target_name(name)
    url = get_player_url(target_name)
    resp = requests.get(url)
    page_content = BeautifulSoup(resp.content, "html.parser")
    advanced_div = page_content.find("div",attrs={"id":"all_advanced"})
    comments = advanced_div.find_all(string=lambda text: isinstance(text, Comment))[0]
    stat_html = str(comments)
    stat_soup = BeautifulSoup(stat_html, "html.parser")
    stat_tag = adv_stat_map[stat]
    stat_td = stat_soup.find("td", attrs={"data-stat":stat_tag})
    return float(stat_td.string) if stat_td else 0.0


"""
Function to get NBA players stats
for a specific year

Parameters
----------
year : int
    The year to scrape for NBA player
    stats

Returns
-------
get_player_list(table) : list
    The list of player objects with scraped stats
"""
def get_player_stats(year):
    url = "{}/leagues/NBA_{}_per_game.html".format(base_url, str(year))
    resp = requests.get(url)
    page_content = BeautifulSoup(resp.content, "html.parser")
    table = page_content.findAll("tr",attrs={"class":"full_table"})
    return get_stat_list(table)


"""
Function to get NBA player's stats
for a specific game

Parameters
----------
link : string
    The game to scrape for NBA player
    stats

Returns
-------
home_map : dict
    A dictionary of players with list of stats as value
away_map : dict
    A dictionary of players with list of stats as value
"""
def get_game_stats(link):
    resp = requests.get(link)
    page_content = BeautifulSoup(resp.content, "html.parser")
    table = page_content.findAll("table",attrs={"class":"sortable stats_table"})

    home_map = {}
    away_map = {}
    home_table = table[0]
    away_table = table[8]
    home_team = home_table.find("caption").string.split(" (")[0]
    away_team = away_table.find("caption").string.split(" (")[0]
    home_map["name"] = home_team
    away_map["name"] = away_team

    labels_tr = home_table.find("tr",attrs={"class":"thead"})
    labels_th = labels_tr.findAll("th")
    labels = []
    for i, th in enumerate(labels_th):
        if i > 0:
            labels.append(th["aria-label"])
    
    home_tr_list = home_table.findAll("tr")
    away_tr_list = away_table.findAll("tr")
    for i in range(len(home_tr_list)):
        home_tr = home_tr_list[i]
        away_tr = away_tr_list[i]
        if home_tr.find("th").find("a"):
            home_player = home_tr.find("th").find("a").string
            away_player = away_tr.find("th").find("a").string
            home_td = home_tr.findAll("td")
            away_td = away_tr.findAll("td")
            home_stat_list = []
            away_stat_list = []
            for j in range(min(len(away_td), len(home_td))):
                home_stat_list.append((labels[j], home_td[j].string))
                away_stat_list.append((labels[j], away_td[j].string))
            home_map[home_player] = home_stat_list
            away_map[away_player] = away_stat_list

    return home_map, away_map


"""
Function to get NBA player's advanced stats
for a specific game

Parameters
----------
link : string
    The game to scrape for NBA player
    advanced stats

Returns
-------
home_map : dict
    A dictionary of players with list of advanced stats as value
away_map : dict
    A dictionary of players with list of advanced stats as value
"""
def get_game_adv_stats(link):
    resp = requests.get(link)
    page_content = BeautifulSoup(resp.content, "html.parser")
    table = page_content.findAll("table",attrs={"class":"sortable stats_table"})

    home_map = {}
    away_map = {}
    home_table = table[7]
    away_table = table[15]
    home_team = table[0].find("caption").string.split(" (")[0]
    away_team = table[8].find("caption").string.split(" (")[0]
    home_map["name"] = home_team
    away_map["name"] = away_team

    labels_tr = home_table.find("tr",attrs={"class":"thead"})
    labels_th = labels_tr.findAll("th")
    labels = []
    for i, th in enumerate(labels_th):
        if i > 0:
            labels.append(th["aria-label"])
    
    home_tr_list = home_table.findAll("tr")
    away_tr_list = away_table.findAll("tr")
    for i in range(len(home_tr_list)):
        home_tr = home_tr_list[i]
        away_tr = away_tr_list[i]
        if home_tr.find("th").find("a"):
            home_player = home_tr.find("th").find("a").string
            away_player = away_tr.find("th").find("a").string
            home_td = home_tr.findAll("td")
            away_td = away_tr.findAll("td")
            home_stat_list = []
            away_stat_list = []
            for j in range(min(len(away_td), len(home_td))):
                home_stat_list.append((labels[j], home_td[j].string))
                away_stat_list.append((labels[j], away_td[j].string))
            home_map[home_player] = home_stat_list
            away_map[away_player] = away_stat_list

    return home_map, away_map
    
