# Cluster API
import math
import statistics

from sklearn.cluster import KMeans
import numpy as np
from sklearn.preprocessing import MinMaxScaler


class ClusterStore(object):

    def __init__(self, data, entity_map):
        self.original_data = data
        self.entity_map = entity_map
        self.clusters = None
        self.total_cluster = 0
        self.clustered = False
        self.avg_similarity = 0.0
        self.avg_distance = 0.0

    '''
    Build optimal k-means clusters based on minimum WCSS (Maximize distance) of clusters
    :store: Total number of cluster, storing same cluster entity in a dictionary 
            (ex: cluster0: [entity1, entity10, entity50......])
    :update: clustered flag
    '''
    def build_optimal_kmeans_clusters(self):
        X = self.original_data
        mms = MinMaxScaler()
        mms.fit(X)
        data_transformed = mms.transform(X)
        wcss = []
        prev_inertia = 0
        cur_inertia = 0
        for i in range(1,len(data_transformed)):
            kmeans = KMeans(n_clusters=i,init='k-means++', max_iter=300, n_init=10, random_state=0)
            kmeans.fit(data_transformed)
            if(i>1):
                prev_inertia = wcss[-1]
            cur_inertia = kmeans.inertia_
            wcss.append(cur_inertia)
            if(abs(prev_inertia-cur_inertia) < 1):   # Cut off inertia
                break
        self.total_cluster = i
        y_kmeans = kmeans.predict(data_transformed)
        self.clusters = {}
        for i in range(self.total_cluster):
            self.clusters[i] = []
        for i in range(len(y_kmeans)):
            self.clusters[y_kmeans[i]].append(i)
        self.clustered = True

    '''
    :param k: number of cluster
    :store: Total number of cluster, storing same cluster entity in a dictionary 
            (ex: cluster0: [entity1, entity10, entity50......])
    :update: clustered flag
    '''
    def build_kmeans_clusters(self, k):
        X = self.original_data
        mms = MinMaxScaler()
        mms.fit(X)
        data_transformed = mms.transform(X)
        kmeans = KMeans(n_clusters=k, init='k-means++', max_iter=300, n_init=10, random_state=0)
        kmeans.fit(data_transformed)
        self.total_cluster = k
        y_kmeans = kmeans.predict(data_transformed)
        self.clusters = {}
        for i in range(self.total_cluster):
            self.clusters[i] = []
        for i in range(len(y_kmeans)):
            self.clusters[y_kmeans[i]].append(i)
        self.clustered = True

    # Function to run agglomerative clustering on current data
    # This function should return the optimal number of clusters
    # based on some kind of metric 
    def build_optimal_agglomerative_clusters(self):
        # TODO 
        pass

    # Function to run agglomerative clustering 
    # with specified number of cluster: c -> int
    def build_agglomerative_clusters(self, c):
        # TODO
        pass

    # Function to calculate the average similarity of current clusters 
    def average_similarity(self):
        # TODO 
        pass

    '''
    :param entity1: X
    :param entity2: Y
    :return: euclidian distance between two entity vector X and Y
    '''
    def euclidian_dist(self,entity1, entity2):
        X = self.original_data[entity1]
        Y = self.original_data[entity2]
        return np.linalg.norm(X-Y)

    '''
    :param k1: cluster1
    :param k2: cluster2
    :return: average distance between two cluster
    :formula: dist(Ki,Kj) = mean(dist(eil,ejm)) where every eil belongs to Ki not belongs to Kj
                                                and every ejk belongs to Kj not belongs to Ki
    '''
    def avg_distance_between_two_cluster(self,k1,k2):
        dist = []
        for k1_entity in k1:
            for k2_entity in k2:
                dist.append(self.euclidian_dist(k1_entity,k2_entity))
        return statistics.mean(dist)

    # :return: average distance of all clusters store in avg_distance
    def average_distance(self):
        dist = []
        for i in range(self.total_cluster):
            for j in range(i+1, self.total_cluster):
                dist.append(self.avg_distance_between_two_cluster(self.clusters[i],self.clusters[j]))
        self.avg_distance = statistics.mean(dist)

    # map cluster with entity name and return the clusters
    def get_clusters_on_entity_map(self):
        return_ = self.clusters
        for cluster in range(self.total_cluster):
            entitys = [self.entity_map[x] for x in self.clusters[cluster]]
            return_[cluster]= entitys
        return return_

    # :reset: clustered flag, total_cluster, avg_distance
    # :delete: clusters data
    def reset(self):
        self.clustered = False
        self.total_cluster = 0
        self.clusters = None
        self.avg_distance = 0.0
