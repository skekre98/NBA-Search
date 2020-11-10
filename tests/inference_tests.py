import unittest
import random
from data.text_data import non_nba, unsure
from inference.ranknode import RankNode
from inference.statnode import StatNode
from inference.infonode import InfoNode
from inference.inference_network import InferenceNetwork

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
    
    #Test response returns a str
    def test_response(self):
        node = InfoNode()
        test_verbs = ["be", "do", "build", "make", "Cannot Understand"]
        
        for verb in test_verbs:
            node.load_query(verb)
            resp = node.response()
            self.assertIsInstance(resp,str,"response test failed at verb: {}. Got instance of {}, expected instance of str".format(verb,type(resp)))
    
    #Test make and be responses generator return a str     
    def test_random_response(self):
        node = InfoNode()
        make_response = node.random_make_response()
        be_response = node.random_be_response()
        
        self.assertIsInstance(make_response,str,'make response returned instance of {}, expected instance of str'.format(type(make_response)))
        self.assertIsInstance(be_response,str,'be response returned instance of {}, expected instance of str'.format(type(be_response)))

# Test cases for inference network
class TestInferenceNetwork(unittest.TestCase):

    # Test if wrong rank classification is handled correctly
    def test_wrong_rank_classification(self):
        query = "Who is a better singer Beyonce or me in the shower?"
        handler = InferenceNetwork(query)
        node_type = handler.node_type
        response = handler.response()
        self.assertEqual(node_type, "rank")  # Making sure it gets wrongly classified as rank
        self.assertIn(response, {non_nba, unsure})
    
    # Test if wrong stat classification is handled correctly
    def test_wrong_stat_classification(self):
        query = "is this a shot?"
        handler = InferenceNetwork(query)
        node_type = handler.node_type
        response = handler.response()
        self.assertEqual(node_type, "stat")  # Making sure it gets wrongly classified as stat
        self.assertIn(response, {non_nba, unsure})   

if __name__ == '__main__':
    unittest.main()
