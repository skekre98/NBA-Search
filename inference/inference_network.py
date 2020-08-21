import pickle
from sklearn.externals import joblib
from modules.transformer import predictors, query_tokenizer

class InferenceNetwork(object):

    def __init__(self, query):
        self.query = query

        # Query classification 
        model_file = "inference/models/query_classifier.pkl"
        query_clf = joblib.load(model_file)
        self.node_type = query_clf.predict([query.lower()])[0]
    
    def response(self):
        if self.node_type == 1:
            return "This is a rank question!"
        elif self.node_type == 2:
            return "This is a stat question!"
