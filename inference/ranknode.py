import random

class RankNode(object):

    def __init__(self, query):
        self.query = query

    def response(self):
        name_1, name_2 = self.extract_name()
        metric = self.extract_metric()
        stat_1 = self.get_stat(name_1, metric)
        stat_2 = self.get_stat(name_2, metric)
        entity_1 = (name_1, stat_1) 
        entity_2 = (name_2, stat_2)

        better_player = lambda a, b : a if a[1] > b[1] else b
        max_entity = better_player(entity_1, entity_2)

        resp_1 = "{} has performed better in the past with a {} or {}".format(max_entity[0], metric, max_entity[1])
        resp_2 = "Statistically speaking {} is superior with a {} or {}".format(max_entity[0], metric, max_entity[1])
        resp_3 = "With a {} of {} I'd have to go with {}. It is alright if you have a different opinion as long as you don't mind being wrong".format(metric, max_entity[1], max_entity[0])
        resp_list = [resp_1, resp_2, resp_3]
        return random.choice(resp_list)

    def extract_name(self):
        # TODO 
        return "Lebron James"
    
    def extract_metric(self):
        # TODO 
        return "shooting"
    
    def get_stat(self, name, metric):
        # TODO 
        return random.randint(0, 10)