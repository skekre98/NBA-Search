class Team(object):

    def __init__(self,name,w,l,r):
        self.name = name
        self.wins = w
        self.losses = l
        self.rank = r
    
    def __str__(self):
        s = "{}. {} ~ Wins: {} Losses: {}".format(self.rank, self.name, self.wins, self.losses)
        return s

class Player(object):

    def __init__(self, n):
        self.name = n
        self.position = None
        self.team = None
        self.games = None
        self.games_started = None
        self.min_played = None
        self.field_goals = None
        self.field_goal_attempts = None
        self.field_goal_percent = None
        self.three_points = None
        self.three_point_attempts = None
        self.three_point_percent = None
        self.two_points = None
        self.two_point_attempts = None
        self.two_point_percent = None
        self.eFG = None
        self.ft = None
        self.fta = None
        self.ftp = None
        self.off_reb = None
        self.def_reb = None
        self.total_reb = None
        self.assists = None
        self.steals = None
        self.blocks = None
        self.turnovers = None
        self.personal_fouls = None
        self.points = None

    
    def create(self, attr):
        self.position = attr["pos"]
        self.team = attr["team_id"]
        self.games = int(attr["g"])
        self.games_started = int(attr["gs"])
        self.min_played = float(attr["mp_per_g"])
        self.field_goals = float(attr["fg_per_g"])
        self.field_goal_attempts = float(attr["fga_per_g"])
        self.field_goal_percent = float(attr["fg_pct"]) if attr["fg_pct"] else -1.0
        self.three_points = float(attr["fg3_per_g"])
        self.three_point_attempts = float(attr["fg3a_per_g"])
        self.three_point_percent = float(attr["fg3_pct"]) if attr["fg3_pct"] else -1.0
        self.two_points = float(attr["fg2_per_g"])
        self.two_point_attempts = float(attr["fg2a_per_g"])
        self.two_point_percent = float(attr["fg2_pct"]) if attr["fg2_pct"] else -1.0
        self.eFG = float(attr["efg_pct"]) if attr["efg_pct"] else -1
        self.ft = float(attr["ft_per_g"])
        self.fta = float(attr["fta_per_g"])
        self.ftp = float(attr["ft_pct"]) if attr["ft_pct"] else -1.0
        self.off_reb = float(attr["orb_per_g"])
        self.def_reb = float(attr["drb_per_g"])
        self.total_reb = float(attr["trb_per_g"])
        self.assists = float(attr["ast_per_g"])
        self.steals = float(attr["stl_per_g"])
        self.blocks = float(attr["blk_per_g"])
        self.turnovers = float(attr["tov_per_g"])
        self.personal_fouls = float(attr["pf_per_g"])
        self.points = float(attr["pts_per_g"])
    
    def get_fantasy_score(self):
        score = 0
        score += 3 * self.three_points
        score += 2 * self.two_points
        score += self.ft
        score += 1.2 * self.total_reb
        score += 1.5 * self.assists
        score += 2 * self.blocks
        score += 2 * self.steals
        score += -1 * self.turnovers
        return score
        
        



