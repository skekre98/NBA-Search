import unittest
from modules import analysis

class TestAnalysis(unittest.TestCase):

    def test_fantasy_rec(self):
        score_list = analysis.fantasy_recommendations()
        self.assertEqual(len(score_list), 514, "Missing Players")
        self.assertTrue(score_list[0][1] > score_list[-1][1])
    
    def test_create_df(self):
        d = analysis.create_dataframe()
        self.assertEqual(len(d), 514, "Missing Players")

if __name__ == '__main__':
    unittest.main()