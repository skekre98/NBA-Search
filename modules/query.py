from modules.analysis import isNBA
from data.text_data import unsure, non_nba
from inference.inference_network import InferenceNetwork

class Query(object):

    def __init__(self, query):
        self.text = query

    # Method to process query 
    def process(self):
        flag = isNBA(self.text)
        if flag == -1:
            return non_nba
        elif flag == 0:
            return unsure
        else:
            network = InferenceNetwork(self.text)
            return network.response()
