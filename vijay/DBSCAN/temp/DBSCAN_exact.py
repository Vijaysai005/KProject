# usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 06 13:15:05 2017

@author: Vijayasai S
"""
# Use python3

from sklearn.cluster import DBSCAN

import csv

from os.path import dirname
from os.path import join
import numpy as np

import pandas as pd


class CreateDict(dict):

    def __init__(self, **kwargs):
        dict.__init__(self, kwargs)

    def __setattr__(self, key, value):
    	self[key] = value

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __getstate__(self):
    	return self.__dict__

def load_files(filename, nrow, ncol):
    module_path = dirname(__file__)
    with open(join(module_path, filename)) as csv_file:
        data_file = csv.reader(csv_file)

        n_samples = int(nrow)
        n_features = int(ncol)

        data = np.empty((n_samples, n_features))

        for i, j in enumerate(data_file):
            data[i] = np.asarray(j[0:], dtype=np.float)
    return CreateDict(data=data).data


def loadData(filename, col1, col2):
    # Loading data from csv files
    with open(filename, "r") as csv_file:
        data_file = csv.reader(csv_file)
        df = pd.DataFrame(list(data_file), columns=[col1,col2])
    nrow = len(df["latitude"])
    ncol = len(df.columns)
    return load_files(filename,nrow, ncol)


def _DBSCAN(data, eps, min_samples):
 
    db = DBSCAN(eps=eps, min_samples=min_samples).fit(data)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    unique_labels = set(labels)

    outlier = [] ; cluster = []
    for k in unique_labels:

        part_cluster = []
        class_member_mask = (labels == k)
        xy = data[class_member_mask & core_samples_mask]

        if k != -1:
            part_cluster.append(xy)
        cluster.append(part_cluster)
        xy = data[class_member_mask & ~core_samples_mask]

        if k == -1:
            outlier.append(xy)

    main_dict = {} ; lat_dict = {} ; long_dict = {}
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
                m += 1      
    try:
    	lat_dict["outlier"] = [] ; long_dict["outlier"] = []
    	for i in range(len(outlier[0])):
    		lat_dict["outlier"].append(outlier[0][i][0])
    		long_dict["outlier"].append(outlier[0][i][1])
    except Exception:
    	pass

    main_dict["latitude"] = lat_dict
    main_dict["longitude"] = long_dict

    return main_dict

def distance(cluster_lat, cluster_long, outlier_lat, outlier_long):
    return np.linalg.norm(np.array((cluster_lat, cluster_long))-np.array((outlier_lat, outlier_long)))

# FindCluster function determines the nearest cluster of the outlier
def FindCluster(main_dict, _id):
    dist = 10**12 ; dist_i = []
    for i in range(len(main_dict["latitude"]) - 1):
        for j in range(len(main_dict["latitude"][str(i+1)])):
            pair_wise = distance(main_dict["latitude"][str(i+1)][j] , main_dict["longitude"][str(i+1)][j] , \
                main_dict["latitude"]["outlier"][_id] ,main_dict["longitude"]["outlier"][_id])
            if pair_wise < dist:
                dist = pair_wise
                dist_i.append(str(i+1))
    return dist_i[-1]

if __name__ == "__main__":
    data = loadData("POI_only_lat_long.csv", "latitude", "longitude")
    main_dict = _DBSCAN(data, 0.02, 2.0)
    for _id in range(len(main_dict["latitude"]["outlier"])):
        cluster_number = FindCluster(main_dict, _id)













