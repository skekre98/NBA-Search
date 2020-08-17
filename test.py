import unittest
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

if __name__ == '__main__':
    unittest.main()