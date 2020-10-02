import pickle
from sklearn.externals import joblib
from modules.transformer import predictors, query_tokenizer
from inference.ranknode import RankNode
from inference.statnode import StatNode

class InferenceNetwork(object):

    def __init__(self, query):
        self.query = query

        # Query classification 
        model_file = "inference/models/query_classifier.pkl"
        query_clf = joblib.load(model_file)
        self.node_type = query_clf.predict([query.lower()])[0]
    
    def response(self):
        if self.node_type == "rank":
            node = RankNode()
        elif self.node_type == "stat":
            node = StatNode()
        node.load_query(self.query)
        return node.response()
