import pickle
from sklearn.externals import joblib
from modules.transformer import predictors, query_tokenizer
from inference.ranknode import RankNode

node_map = {
    1 : "rank",
    2 : "stat"
}

class InferenceNetwork(object):

    def __init__(self, query):
        self.query = query

        # Query classification 
        model_file = "inference/models/query_classifier.pkl"
        query_clf = joblib.load(model_file)
        self.node_type = node_map[query_clf.predict([query.lower()])[0]]
    
    def response(self):
        if self.node_type == "rank":
            node = RankNode(self.query)
        elif self.node_type == "stat":
            node = RankNode(self.query)
        
        return node.response()
