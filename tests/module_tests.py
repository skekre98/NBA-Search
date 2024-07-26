import unittest
import random
from datetime import date
from modules import analysis, scraper


# Test cases for Analysis API 
class TestAnalysis(unittest.TestCase):

    # Method to test fantasy recommendations 
    def test_fantasy_rec(self):
        score_list = analysis.fantasy_recommendations()
        self.assertTrue(len(score_list) > 100, "Missing Players")
        self.assertTrue(score_list[0][1] > score_list[-1][1])
    
    # Method to test dataframe creation 
    def test_create_df(self):
        df, p_map = analysis.create_player_dataframe()
        self.assertTrue(True)
    
    # Method to test clustering algorithm 
    def test_cluster(self):
        c = 100
        res = analysis.build_stat_clusters(c)
        self.assertTrue(len(res), c)
    
    def test_query_filter(self):
        flag_1 = analysis.isNBA("Will this team make it to the finals?")
        flag_0 = analysis.isNBA("Michael Jordan is good!")
        flag_n = analysis.isNBA("This is a random query...")
        self.assertEqual(flag_1, 1)
        self.assertEqual(flag_0, 0)
        self.assertEqual(flag_n, -1)

# Test cases for web scraper 
class TestScraper(unittest.TestCase):

    # Method to test web scraper for Player Efficiency Rating
    def test_get_per(self):
        year = int(date.today().year)
        per_list = scraper.get_per(year)
        for t in per_list:
            self.assertTrue(isinstance(t[0], str))
            self.assertTrue(isinstance(t[1], float))
    
    # Method to test scraper for player names
    def test_get_names(self):
        year = int(date.today().year)
        names = scraper.get_player_names(year)
        for n in names:
            self.assertTrue(isinstance(n, str))
    
    # Method to test scraper for playoff bracket
    def test_get_playoff_bracket(self):
        bracket = scraper.get_playoff_bracket()
        levels = {
            "Western Conference First Round",
            "Eastern Conference First Round",
            "Western Conference Semifinals",
            "Eastern Conference Semifinals",
            "Western Conference Finals",
            "Eastern Conference Finals",
            "Finals"
        }
        for l in bracket:
            self.assertTrue(l in levels)
    
    # Method to test get target name  
    def test_get_target_name(self):
        lebron_jamess = ["LeBron James", "Lebron James", "Lebron"]
        for i in lebron_jamess:
            self.assertEqual(scraper.get_target_name(i), "LeBron James")
        
        shaquille_oneals = ["Shaquille O'Neal", "Shaq O'Niel", "Shakiel O'Neal"]
        for i in shaquille_oneals:
            self.assertEqual(scraper.get_target_name(i), "Shaquille O'Neal")
        
        klay_thompsons = ["Klay Thompson", "Clay Thompson", "Clay Thomson", "Klay Thomson"]
        for i in klay_thompsons:
            self.assertEqual(scraper.get_target_name(i), "Klay Thompson")
        
        kobe_bryants = ["Kobe Bryant", "kobe", "Kobe"]        
        for i in kobe_bryants:
            self.assertEqual(scraper.get_target_name(i), "Kobe Bryant")
        
        wilt_chamberlains = ["Wilt Chamberlain", "Wilt", "wilt"]        
        for i in wilt_chamberlains:
            self.assertEqual(scraper.get_target_name(i), "Wilt Chamberlain")

        dennis_rodmans = ["Dennis Rodman", "Rodman", "rodman"]        
        for i in dennis_rodmans:
            self.assertEqual(scraper.get_target_name(i), "Dennis Rodman")

    # Method to test get player url  
    def test_get_player_url(self):
        self.assertEqual(scraper.get_player_url("Kobe Bryant"), "https://www.basketball-reference.com/players/b/bryanko01.html")
        self.assertEqual(scraper.get_player_url("LeBron James"), "https://www.basketball-reference.com/players/j/jamesle01.html")
        self.assertEqual(scraper.get_player_url("Dennis Rodman"), "https://www.basketball-reference.com/players/r/rodmade01.html")

    # Method to test advanced stat scraper for player
    def test_get_adv_stats(self):
        names = ["Kobe Bryant", "Lebron James", "Klay Thompson"]
        stats = ["true shooting percentage", "total rebound percentage", "defensive box plus/minus"]
        for i in range(5):
            random_name = random.choice(names)
            random_stat = random.choice(stats)
            stat = scraper.get_adv_stat(random_name, random_stat)
            self.assertTrue(isinstance(stat, float))
    
    # Method to test advanced stat scraper from game link 
    def test_get_game_adv_stats(self):
        adv_stats = ['Minutes Played', 'True Shooting Percentage', 'Effective Field Goal Percentage', '3-Point Attempt Rate', 'Free Throw Attempt Rate']
        home, away = scraper.get_game_stats("https://www.basketball-reference.com/boxscores/202009300LAL.html",adv_stats=True)
        ad_stats = away['Anthony Davis']
        scraper_stats = set()
        for stat in ad_stats:
            scraper_stats.add(stat[0])
        
        for adv_stat in adv_stats:
            self.assertTrue(adv_stat in adv_stats)

if __name__ == '__main__':
    unittest.main()
