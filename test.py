import unittest
import random
from datetime import date
from modules import analysis, scraper
from inference.ranknode import RankNode
from inference.statnode import StatNode
from inference.infonode import InfoNode
from preprocess import funnel_name
import preprocess
from app import app

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
        home, away = scraper.get_game_adv_stats("https://www.basketball-reference.com/boxscores/202009300LAL.html")
        ad_stats = away['Anthony Davis']
        scraper_stats = {}
        for stat in ad_stats:
            scraper_stats.add(stat[0])
        
        for adv_stat in adv_stats:
            self.assertTrue(adv_stat in adv_stats)

# Test cases for stat node
class TestStatNode(unittest.TestCase):

    # Method to test stat node response 
    def test_node_response(self):
        node = StatNode()
        node.load_query("query")
        resp = node.response()
        stat = [int(word) for word in resp.split() if word.replace('.','').isdigit()]
        self.assertTrue(isinstance(resp, str))
    
    def test_extract_name(self):
        node = StatNode()
        node.load_query("What is Kobe Bryant's shooting percentage?")
        name = node.extract_name()
        self.assertEqual(name, "Kobe Bryant's")

    def test_extract_stat(self):
        node = StatNode()
        node.load_query("What is Kobe Bryant's true shooting percentage?")
        stat = node.extract_stat()
        self.assertEqual(stat, "true shooting percentage")
    
    def test_get_player_stat(self):
        node = StatNode()
        val = node.get_player_stat("Kobe Bryant", "true shooting percentage")
        self.assertTrue(isinstance(val, float))


# Test cases for rank node
class TestRankNode(unittest.TestCase):

    # Method to test rank node response 
    def test_node_response(self):
        query = "query"
        node = RankNode()
        node.load_query(query)
        resp = node.response()
        stat = [int(word) for word in resp.split() if word.replace('.','').isdigit()]
        self.assertTrue(isinstance(resp, str))
    
    # Method to test rank node metric conversion
    def test_metric2stat(self):
        query = "query"
        node = RankNode()
        node.load_query(query)
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
        query = "Who is a better shooter Kobe or Lebron?"
        node = RankNode()
        node.load_query(query)
        metric = node.extract_metric()
        self.assertEqual(metric, "shooter")
    
    # Method to test name extraction
    def test_extract_names(self):
        query = "Who is a better shooter Kobe Bryant or Lebron James?"
        node = RankNode()
        node.load_query(query)
        name1, name2 = node.extract_names()
        names = set([name1, name2])
        self.assertTrue("Kobe Bryant" in names)
        self.assertTrue("Lebron James" in names)
    
    # Method to test stat getter
    def test_get_stat(self):
        node = RankNode()
        names = ["Kobe Bryant", "Lebron James", "Klay Thompson"]
        stats = ["true shooting percentage", "total rebound percentage", "defensive box plus/minus"]
        for i in range(5):
            random_name = random.choice(names)
            random_stat = random.choice(stats)
            stat = node.get_stat(random_name, random_stat)
            self.assertTrue(isinstance(stat, float))

# Test case for data preprocess
class TestPreprocess(unittest.TestCase):

    # Method to test funnel name 
    def test_get_random_player_names(self):
        names = ["Bud Acton", "Gary Alexander", "Steven Adams"]
        for i in range(3):
            player_name = funnel_name(names[i])
            self.assertTrue(player_name in ' '.join(names))

# Test cases for URL Routing
class TestRouting(unittest.TestCase):
    # Method to test <blank> routing
    def test_blank_routing(self):
        with app.test_client() as c:
            response = c.get('')
            # 308: permanent redirect
            self.assertEqual(response.status_code, 308)

    # Method to test <some> routing
    def test_invalid_routing(self):
        with app.test_client() as c:
            response = c.get('/some/path/that/doesnt/exist')
            # 404: page not found
            self.assertEqual(response.status_code, 404)

    def test_authors_routing(self):
        with app.test_client() as c:
            response = c.get('/authors')
            # 200: response is OK
            self.assertEqual(response.status_code, 200)

    def test_blog_routing(self):
        with app.test_client() as c:
            response = c.get('/blog')
            self.assertEqual(response.status_code, 200)

    def test_chat_routing(self):
        with app.test_client() as c:
            response = c.get('/chat')
            self.assertEqual(response.status_code, 200)

    def test_download_routing(self):
        with app.test_client() as c:
            # expected response code is a 302 ('Moved Temporarily') because of the 'redirect'
            response = c.get('/download/1')
            self.assertEqual(response.status_code, 302)

            response = c.get('/download/2')
            self.assertEqual(response.status_code, 302)

            response = c.get('/download/3')
            self.assertEqual(response.status_code, 302)

    def test_download_routing_invalid_url(self):
        with app.test_client() as c:
            # invalid URL
            response = c.get('/download')
            self.assertEqual(response.status_code, 404)

    def test_get_bot_response_routing(self):
        with app.test_client() as c:
            response = c.post('/bot-msg', data={'msg': 'test message'})
            self.assertEqual(response.status_code, 200)

    def test_get_bot_response_routing_get_not_supported(self):
        with app.test_client() as c:
            # GET not supported
            response = c.get('/bot-msg')
            self.assertEqual(response.status_code, 405)

    def test_get_bot_response_routing_missing_param(self):
        with app.test_client() as c:
            # Bad request: missing param
            response = c.post('/bot-msg')
            self.assertEqual(response.status_code, 400)

    def test_home_routing(self):
        with app.test_client() as c:
            response = c.get('/')
            self.assertEqual(response.status_code, 200)

    def test_home2_routing(self):
        with app.test_client() as c:
            response = c.get('/home')
            self.assertEqual(response.status_code, 200)

    def test_predictions_routing(self):
        with app.test_client() as c:
            response = c.get('/predictions')
            self.assertEqual(response.status_code, 200)

# Test cases for info node
class TestInfoNode(unittest.TestCase):
    
    #Test extract_components returns correct verb
    def test_extract_components(self):
        node = InfoNode()
        test_phrase = {"who are you?":"be", "what do you do?":"do", "who build you?":"build", "who made you?":"make"}
          
        for phrase in test_phrase:
            node.load_query(phrase)
            test_verb = list(node.extract_components())[0]
            true_verb = test_phrase.get(phrase)
            
            self.assertTrue(test_verb == true_verb, 
                            "extract_components test failed at phrase: {}. Got verb: {}, expecting verb: {}.".format(phrase, test_verb, true_verb))
    
    #Test generate_random_response returns the correct response
    def test_generate_random_response(self):
        node = InfoNode()
        test_verbs = ["be", "do", "build", "make", "Cannot Understand"]
        
        for true_verb in test_verbs:
            verbs = node.generate_random_response(true_verb,test=True)
            
            self.assertTrue(true_verb in verbs,
                            "generate_random_response test failed at verb: {}. Got response for verb(s): {}, expecting response for verb: {}.".format(true_verb,verbs,true_verb))
    
    def test_response(self):
        node = InfoNode()
        test_verbs = ["be", "do", "build", "make", "Cannot Understand"]
        
        for verb in test_verbs:
            node.load_query(verb)
            resp = node.response()
            self.assertIsInstance(resp,str,"response test failed at verb: {}. Got instance of {}, expected instance of str".format(verb,type(resp)))
        

if __name__ == '__main__':
    unittest.main()
