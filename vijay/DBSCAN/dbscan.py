# usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 06 13:15:05 2017

@author: Vijayasai S
"""
# Use python3


import csv, time, numpy as np, pandas as pd, matplotlib.pyplot as plt

from sklearn.cluster import DBSCAN
from load_data import load_files



def loadData(filename,col1, col2):
    # Loading data from csv files
    with open(filename, "r") as csv_file:
        data_file = csv.reader(csv_file)
        df = pd.DataFrame(list(data_file), columns=[col1,col2])

    nrow = len(df["latitude"])
    ncol = len(df.columns)

    data = load_files(filename,nrow, ncol)
    ret = data.data
    return ret


def algorithm(data, eps, min_samples):
    # Implementation of DBSCAN Algorithm
    print ("Implementing DBSCAN algorithm")
    time.sleep(1) 
    db = DBSCAN(eps=eps, min_samples=min_samples).fit(data)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    pl = input("Do you want to know number of clusters?(Y/n) ") 
    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    if pl == "Y" or pl == "y":
        print ("Number of clusters: ", n_clusters_)
    else:
        time.sleep(0.01)
    # Black removed and is used for noise instead.
    unique_labels = set(labels)
    colors = [plt.cm.Spectral(each)
              for each in np.linspace(0, 1, len(unique_labels))]
    return n_clusters_, labels, unique_labels, colors, core_samples_mask

def ClusterPlot(data, n_clusters_, labels, unique_labels, colors, core_samples_mask):
    
    outlier = [] ; cluster = []
    for k,col in zip(unique_labels, colors):
        part_cluster = []
        if k == -1:
            col = [0, 0, 0, 1]
        class_member_mask = (labels == k)
        xy = data[class_member_mask & core_samples_mask]
        plt.plot(xy[:, 1], xy[:, 0], 'o', markerfacecolor=tuple(col),
                         markeredgecolor='k', markersize=14)
        if k != -1:
            part_cluster.append(xy)
        cluster.append(part_cluster)
        xy = data[class_member_mask & ~core_samples_mask]
        plt.plot(xy[:, 1], xy[:, 0], 'o', markerfacecolor=tuple(col),
                         markeredgecolor='k', markersize=6)
        if k == -1:
            outlier.append(xy)

    plt.title('Estimated number of clusters: %d' % n_clusters_)
    plt.xlabel("x-coordinate/Longitude")
    plt.ylabel("y-coordinate/Latitude")
    
    pl = input("Do you want to show the plot?(Y/n) ")
    if pl == "Y" or pl == "y":
        plt.show()
    else:
        time.sleep(0.01)
    
    return cluster, outlier

def dataInDict(cluster, outlier, main_dict={}):
    lat_dict = {} ; long_dict = {}
    pn1 = input("Do you want to  print the cluster data?(Y/n) ")
    if pn1 == "Y" or pn1 == "y":
        print ("Cluster Data: ")
        print ("cls","\t","latitude","\t","longitude")
    else:
        time.sleep(0.01)

    for i in range(len(cluster)-1):
        lat_dict[str(i+1)] = []
        long_dict[str(i+1)] = []
        for j in range(len(cluster[i])):
            m = 0
            for k in range(len(cluster[i][j])):
                if  m == 0:
                    lat_dict[str(i+1)].append(cluster[i][j][k][0])
                    long_dict[str(i+1)].append(cluster[i][j][k][1])
                else:
                    lat_dict[str(i+1)].append(cluster[i][j][k][0])
                    long_dict[str(i+1)].append(cluster[i][j][k][1])
                    
                if pn1 == "Y" or pn1 == "y":
                    if  m == 0:
                        print (str(i+1) , "\t" , cluster[i][j][k][0], "\t", cluster[i][j][k][1])
                    else:
                        print (" " , "\t" , cluster[i][j][k][0], "\t", cluster[i][j][k][1])
                else:
                    time.sleep(0.01)
                m += 1      

    lat_dict["outlier"] = [] ; long_dict["outlier"] = []
    for i in range(len(outlier[0])):
        lat_dict["outlier"].append(outlier[0][i][0])
        long_dict["outlier"].append(outlier[0][i][1])

    main_dict["latitude"] = lat_dict
    main_dict["longitude"] = long_dict 

    return main_dict

def distance(cluster_lat, cluster_long, outlier_lat, outlier_long):
    return np.linalg.norm(np.array((cluster_lat, cluster_long))-np.array((outlier_lat, outlier_long)))


def FindingCluster(main_dict,outlier_index):
    dist = 10**12 ; dist_i = []
    for i in range(len(main_dict["latitude"]) - 1):
        for j in range(len(main_dict["latitude"][str(i+1)])):
            pair_wise = distance(main_dict["latitude"][str(i+1)][j] , main_dict["longitude"][str(i+1)][j] , \
                main_dict["latitude"]["outlier"][outlier_index] ,main_dict["longitude"]["outlier"][outlier_index])
            if pair_wise < dist:
                dist = pair_wise
                dist_i.append(str(i+1))
    return dist_i[-1]


if __name__ == "__main__":
    data = loadData("POI_only_lat_long.csv","latitude", "longitude")
    eps = float(input("Enter the value maximum distance for forming cluster: "))
    n_clusters, labels, unique_labels, colors, core_samples_mask = algorithm(data, eps, 2.0)
    cluster, outlier = ClusterPlot(data, n_clusters, labels, unique_labels, colors, core_samples_mask)
    main_dict = dataInDict(cluster,outlier,{})

    pn2 = input("Do you want to  print the outlier data?(Y/n) ")
    if pn2 == "Y" or pn2 == "y":
        print ("The ID's outside the cluster: ")
        print ("ID's","\t","latitude","\t","longitude","\t", "Near by cluster")
    else:
        time.sleep(0.01)
    for i in range(len(main_dict["latitude"]["outlier"])):
        cluster_number = FindingCluster(main_dict,i)
        if pn2 == "Y" or pn2 == "y":
            print (str(i+1),"\t",main_dict["latitude"]["outlier"][i],"\t",main_dict["longitude"]["outlier"][i],"\t",cluster_number) 
        else:
            time.sleep(0.01) 
    
