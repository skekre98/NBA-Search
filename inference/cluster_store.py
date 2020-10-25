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
    
    # Function to run kmeans clustering on data 
    def build_kmeans_clusters(self):
        '''
        Build optimal k-means clusters based on minimum WCSS (Maximize distance) on clusters
        :store: Total number of cluster, Clusters data
        :update: clustered flag
        '''
        X = self.original_data
        mms = MinMaxScaler()
        mms.fit(X)
        data_transformed = mms.transform(X)
        # print(data_transformed)
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
            if(abs(prev_inertia-cur_inertia) < 1):   # inertia diff checking
                break
        # print(wcss)
        # print('Total clusters:', i)
        self.total_cluster = i
        y_kmeans = kmeans.predict(data_transformed)
        # print(y_kmeans)
        ######################################################
        # cluster entity map
        # storing same cluster entity in a dictionary
        # ex: cluster0: [entity1, entity10, entity50......]
        #######################################################
        self.clusters = {}
        for i in range(self.total_cluster):
            self.clusters[i] = []
        for i in range(len(y_kmeans)):
            self.clusters[y_kmeans[i]].append(i)
        # print(self.clusters)
        self.clustered = True

    def build_kmeans_clusters_on_given_number_of_cluster(self, k):
        '''
        :param k: number of cluster
        :store: Total number of cluster, Clusters data
        :update: clustered flag
        '''
        X = self.original_data
        mms = MinMaxScaler()
        mms.fit(X)
        data_transformed = mms.transform(X)
        kmeans = KMeans(n_clusters=k, init='k-means++', max_iter=300, n_init=10, random_state=0)
        kmeans.fit(data_transformed)
        self.total_cluster = k
        y_kmeans = kmeans.predict(data_transformed)
        ######################################################
        # cluster entity map
        # storing same cluster entity in a dictionary
        # ex: cluster0: [entity1, entity10, entity50......]
        #######################################################
        self.clusters = {}
        for i in range(self.total_cluster):
            self.clusters[i] = []
        for i in range(len(y_kmeans)):
            self.clusters[y_kmeans[i]].append(i)
        # print(self.clusters)
        self.clustered = True

    # Function to run agglomerative clustering on current data 
    def build_agglomerative_clusters(self):
        # TODO 
        pass

    # Function to calculate the average similarity of current clusters 
    def average_similarity(self):
        # TODO 
        pass

    def euclidian_dist(self,entity1, entity2):
        '''
        :param entity1: X
        :param entity2: Y
        :return: euclidian distance between two entity vector (3D) X and Y
        '''
        X = self.original_data[entity1]
        Y = self.original_data[entity2]
        return math.sqrt(pow((X[0]-Y[0]),2) + pow((X[1]-Y[1]),2) + pow((X[2]-Y[2]),2))

    def avg_distance_between_two_cluster(self,k1,k2):
        '''
        :param k1: cluster1
        :param k2: cluster2
        :return: average distance between two cluster
        :formula: dist(Ki,Kj) = mean(dist(eil,ejm)) where every eil belongs to Ki not belongs to Kj
                                                    and every ejk belongs to Kj not belongs to Ki
        '''
        dist = []
        for k1_entity in k1:
            for k2_entity in k2:
                dist.append(self.euclidian_dist(k1_entity,k2_entity))
        return statistics.mean(dist)

    # Function to calculate average distance of current clusters 
    def average_distance(self):
        '''
        :return: average distance of all clusters store in avg_distance
        '''
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
            # return_[cluster].replace()
        return return_

    # map cluster with data and return the clusters
    def get_clusters_on_data(self):
        return_ = self.clusters
        for cluster in range(self.total_cluster):
            entitys = [self.original_data[x] for x in self.clusters[cluster]]
            return_[cluster] = entitys
            # return_[cluster].replace()
        return return_
    # Function to reset clusters back to original data 
    def reset(self):
        '''
        :reset: clustered flag, total_cluster, avg_distance
        :delete: clusters data
        '''
        self.clustered = False
        self.total_cluster = 0
        self.clusters = None
        self.avg_distance = 0.0

if __name__=='__main__':
    data = np.random.uniform(0,500, [200,3])
    # print(data)
    entity_map ={}
    for i in range(200):
        entity_map[i] = 'entity'+str(i+1)
    # print(entity_map)
    c_ob= ClusterStore(data,entity_map)
    c_ob.build_kmeans_clusters()
    c_ob.average_distance()
    print('Total Clusters: ', c_ob.total_cluster)
    print(c_ob.get_clusters_on_entity_map())
    print('Avg distance: ',c_ob.avg_distance)
    c_ob.reset()
    print('Total Clusters: ', c_ob.total_cluster)
    print(c_ob.get_clusters_on_entity_map())
    print('Avg distance: ', c_ob.avg_distance)
    c_ob.build_kmeans_clusters_on_given_number_of_cluster(8)
    c_ob.average_distance()
    print('Total Clusters: ', c_ob.total_cluster)
    print(c_ob.get_clusters_on_entity_map())
    print('Avg distance: ', c_ob.avg_distance)
