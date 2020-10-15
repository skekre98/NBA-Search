# Cluster API

class ClusterStore(object):

    def __init__(self, data, entity_map):
        self.clusters = data
        self.entity_map = entity_map
        self.clustered = False
        self.avg_similarity = 0.0
        self.avg_distance = 0.0
    
    # Function to run KMeans clustering on data 
    def build_kmeans_clusters(self):
        # TODO
        pass
