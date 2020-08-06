import sys
import requests
from bs4 import BeautifulSoup
from modules.objects import Team, Player

base_url = "https://www.basketball-reference.com"

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
def get_player_list(table):
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
        team = row.find("a")["title"]
        wins = row.find("td",attrs={"data-stat":"wins"}).string
        losses = row.find("td",attrs={"data-stat":"losses"}).string
        t = Team(team, wins, losses, i%15+1)
        standings.append(t)
    
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
            if stat["data-stat"] == "per":
                per = float(stat.string)
        per_list.append((name, per))
    return per_list

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
    return get_player_list(table)