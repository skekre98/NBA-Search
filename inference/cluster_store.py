# Cluster API
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
        total_cluster = i
        y_kmeans = kmeans.predict(data_transformed)
        print(y_kmeans)
        '''
        cluster entity map
        storing same cluster entity in a dictionary
        ex: cluster0: [entity1, entity10, entity50......]
        '''
        clusters = {}
        for i in range(total_cluster):
            clusters[i] = []
        for i in range(len(y_kmeans)):
            clusters[y_kmeans[i]].append(i)
        print(clusters)

    # Function to run agglomerative clustering on current data 
    def build_agglomerative_clusters(self):
        # TODO 
        pass

    # Function to calculate the average similarity of current clusters 
    def average_similarity(self):
        # TODO 
        pass

    # Function to calculate average distance of current clusters 
    def average_distance(self):
        # TODO
        pass

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
    print(entity_map)
    c_ob= ClusterStore(data,entity_map)
    c_ob.build_kmeans_clusters()