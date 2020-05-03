class Query(object):

    def __init__(self,category, s):
        self.category = category
        self.string = s
        self.conf = None
        self.region = None

# Method to process query 
def process(query):
    # TODO