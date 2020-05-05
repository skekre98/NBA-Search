import unittest
from modules import analysis

class TestAnalysis(unittest.TestCase):

    def test_fantasy_rec(self):
        score_list = analysis.fantasy_recommendations()
        self.assertEqual(len(score_list), 514, "Missing Players")
        self.assertTrue(score_list[0][1] > score_list[-1][1])
    
    def test_create_df(self):
        df, p_map = analysis.create_player_dataframe()
        self.assertEqual(len(df), 514, "Missing Players")
        for i in range(len(df)):
            p1 = df.iloc[i]['points']
            p2 = p_map[i][1]
            self.assertEqual(p1, p2)
    

if __name__ == '__main__':
    unittest.main()