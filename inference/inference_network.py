import pickle
import joblib
from modules.transformer import predictors, query_tokenizer
from modules.analysis import isNBA
from inference.ranknode import RankNode
from inference.statnode import StatNode
from inference.infonode import InfoNode
from data.text_data import unsure, non_nba


class InferenceNetwork(object):
    """
    A class to facilitate the inference of a query.

    This class will classify if a query is NBA related, as well as the
    "type" of a query, be that info, rank, or stat. After classifying
    the query, it generated a response using the appropriate node
    and returns that response to the user.

    Attributes
    ----------
    query: string
        the query or question passed in by the user

    Methods
    -------
    response()
        Returns the query response from the appropriate node
    """

    def __init__(self, query):
        self.query = query
        # Query classification
        model_file = "inference/models/classifiers/query_classifier.pkl"
        query_clf = joblib.load(model_file)
        self.node_type = query_clf.predict([query.lower()])[0]

    def response(self):
        """
        Function to return the the response bases on the query.

        This function checks the query passed in by the user, and returns the
        response from the appopriate query. The query should have already been
        passed in when creating the "InferenceNetwork" object.
        ----------
        self    : none

        Returns
        -------
        response  : string
            The appropriate response to the user's input query
        """
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
