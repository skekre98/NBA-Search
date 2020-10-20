from inference.inference_network import InferenceNetwork

class Query(object):

    def __init__(self, query):
        self.text = query

    # Method to process query 
    def process(self):
        network = InferenceNetwork(self.text)
        return network.response()
