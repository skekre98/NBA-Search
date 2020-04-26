import requests
from bs4 import BeautifulSoup

base_url = "https://www.basketball-reference.com"

class Team(object):

    def __init__(self,name,w,l,r):
        self.name = name
        self.wins = w
        self.losses = l
        self.rank = r
    
    def __str__(self):
        s = "{}. {} ~ Wins: {} Losses: {}".format(self.rank, self.name, self.wins, self.losses)
        return s

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