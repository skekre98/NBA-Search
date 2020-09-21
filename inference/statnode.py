import spacy

class StatNode(object):

    def __init__(self, query):
        self.query = query
        self.nlp = spacy.load("en_core_web_sm")

    def response(self):
        # TODO
        return "resp"