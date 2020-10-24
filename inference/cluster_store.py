# Cluster API
import math
import statistics

from sklearn.cluster import KMeans
import numpy as np
from sklearn.preprocessing import MinMaxScaler


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
        X = self.clusters
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
            if(abs(prev_inertia-cur_inertia) < 1):
                break
        print(wcss)
        print('Total clusters:', i)
        self.total_cluster = i
        y_kmeans = kmeans.predict(data_transformed)
        print(y_kmeans)
        '''
        cluster entity map
        storing same cluster entity in a dictionary
        ex: cluster0: [entity1, entity10, entity50......]
        '''
        self.original_data = self.clusters
        self.kmeans_clusters = {}
        for i in range(self.total_cluster):
            self.kmeans_clusters[i] = []
        for i in range(len(y_kmeans)):
            self.kmeans_clusters[y_kmeans[i]].append(i)
        print(self.kmeans_clusters)
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
        :return: euclidian distance between two entity point (3D)
        '''
        X = self.clusters[entity1]
        Y = self.clusters[entity2]
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
                dist.append(self.avg_distance_between_two_cluster(self.kmeans_clusters[i],self.kmeans_clusters[j]))
        self.avg_distance = statistics.mean(dist)
    # Function to reset clusters back to original data 
    def reset(self):
        # TODO
        pass

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
    print(c_ob.avg_distance)