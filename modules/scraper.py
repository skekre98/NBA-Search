import sys
import requests
from bs4 import BeautifulSoup
from objects import Team, Player

base_url = "https://www.basketball-reference.com"

# Method to convert stats to player objects
def get_player_list(table):
    player_list = []
    for row in table:
        name = row.find("a").string
        player = Player(name)
        attr = {}
        stats = row.findAll("td")
        for stat in stats:
            attr[stat["data-stat"]] = stat.string
        player.set(attr)
        player_list.append(player)
    return player_list

# Method to scrape standings from website
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

# Method to scrape player stats from website 
def get_player_stats():
    url = "{}/leagues/NBA_2020_per_game.html".format(base_url)
    resp = requests.get(url)
    page_content = BeautifulSoup(resp.content, "html.parser")
    table = page_content.findAll("tr",attrs={"class":"full_table"})
    return get_player_list(table)


l = get_player_stats()

for p in l:
    score = p.get_fantasy_score()
    print(p.name, score)