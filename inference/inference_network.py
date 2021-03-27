import pickle
from sklearn.externals import joblib
from modules.transformer import predictors, query_tokenizer
from modules.analysis import isNBA
from inference.ranknode import RankNode
from inference.statnode import StatNode
from inference.infonode import InfoNode
from data.text_data import unsure, non_nba

"""
a class used to represent InferenceNetwork

parameters
-------
object: string
return

-------
n/a
"""
class InferenceNetwork(object):

    def __init__(self, query):
        self.query = query

        # Query classification
        model_file = "inference/models/query_classifier.pkl"
        query_clf = joblib.load(model_file)
        self.node_type = query_clf.predict([query.lower()])[0]

    def response(self):
        if self.node_type == "info":
            node = InfoNode()
        else:
            # Check if query is NBA related
            flag = isNBA(self.query)
            if flag == 0:
                return unsure
            elif flag == -1:
                return non_nba

            # Query is definitely NBA related
            if self.node_type == "rank":
                node = RankNode()

            if self.node_type == "stat":
                node = StatNode()

        node.load_query(self.query)
        return node.response()
