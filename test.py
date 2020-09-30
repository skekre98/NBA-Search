import unittest
import random
from datetime import date
from modules import analysis, scraper
from inference.ranknode import RankNode
import preprocess

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
    
    # Method to test advanced stat scraper 
    def test_get_adv_stats(self):
        names = ["Kobe Bryant", "Lebron James", "Klay Thompson"]
        stats = ["true shooting percentage", "total rebound percentage", "defensive plus/minus"]
        for i in range(5):
            random_name = random.choice(names)
            random_stat = random.choice(stats)
            stat = scraper.get_adv_stat(random_name, random_stat)
            self.assertTrue(isinstance(stat, float))

# Test cases for rank node
class TestRankNode(unittest.TestCase):

    # Method to test rank node response 
    def test_node_response(self):
        query = "query"
        node = RankNode(query)
        resp = node.response()
        stat = [int(word) for word in resp.split() if word.replace('.','').isdigit()]
        self.assertTrue(isinstance(resp, str))
    
    # Method to test rank node metric conversion
    def test_metric2stat(self):
        node = RankNode("Query")
        test_map = {
            "true shooting percentage" : "shooting",
            "defensive plus/minus" : "defending",
            "player efficiency rating" : "player",
        }

        for stat in test_map:
            metric = test_map[stat]
            predicted_stat = node.metric2stat(metric)
            self.assertEqual(predicted_stat, stat)

        metric = "This is nothing"
        predicted_stat = node.metric2stat(metric)
        self.assertIsNone(predicted_stat)
    
    # Method to test metric extraction
    def test_extract_metric(self):
        node = RankNode("Who is a better shooter Kobe or Lebron?")
        metric = node.extract_metric()
        self.assertEqual(metric, "shooter")
    
    # Method to test name extraction
    def test_extract_names(self):
        node = RankNode("Who is a better shooter Kobe Bryant or Lebron James?")
        name1, name2 = node.extract_names()
        names = set([name1, name2])
        self.assertTrue("Kobe Bryant" in names)
        self.assertTrue("Lebron James" in names)
    
    # Method to test stat getter
    def test_get_stat(self):
        node = RankNode("Query")
        names = ["Kobe Bryant", "Lebron James", "Klay Thompson"]
        stats = ["true shooting percentage", "total rebound percentage", "defensive plus/minus"]
        for i in range(5):
            random_name = random.choice(names)
            random_stat = random.choice(stats)
            stat = node.get_stat(random_name, random_stat)
            self.assertTrue(isinstance(stat, float))


if __name__ == '__main__':
    unittest.main()