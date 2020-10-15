# Cluster API

class ClusterStore(object):

    def __init__(self, data, entity_map):
        self.clusters = data
        self.entity_map = entity_map
        self.clustered = False
        self.avg_similarity = 0.0
        self.avg_distance = 0.0
    
    # Function to run kmeans clustering on data 
    def build_kmeans_clusters(self):
        # TODO
        pass

    # Function to run agglomerative clustering on current data 
    def build_agglomerative_clusters(self):
        # TODO 
        pass

    # Function to calculate the average similarity of current clusters 
    def average_similarity(self):
        # TODO 
        pass