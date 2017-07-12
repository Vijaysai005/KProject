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


def loadData(filename, *args, **kwargs):

	dict = {}
	for key,value in kwargs.items():
		dict[key]=value

	try:
		with open(filename, "r") as csv_file:
			data_file = list(csv.reader(csv_file))
			df = pd.DataFrame(data_file, columns=[*args])
			#print (data_file)
	except FileNotFoundError:
		raise FileNotFoundError("First argument should be a file!")

	try:
		nrow = len(df[args[0]])
	except Exception:
		raise Exception("Aleast one argument should be there!")

	try:
		ncol = len(df.columns)- dict["start_column"]
	except KeyError:
		raise KeyError("Mention the column number to start (0,1,2,...n) as keyword argument (eg.,start_column=0)")

	data = np.empty((nrow, ncol))
	for i, j in enumerate(data_file):
		data[i] = np.asarray(j[dict["start_column"]:], dtype=np.float)

	if "unit_id" in args:
		return [CreateDict(data=data).data,df]
	else:
		raise KeyError("unit_id is missing")


listOfDict = [{'unit_id':1410656,'latitude':18.052, 'longitude':74.065},{'unit_id':1410657,'latitude':18.053, 'longitude':74.066},\
	{'unit_id':1410658,'latitude':18.054, 'longitude':74.067}]

def DictToList(listOfDict):
	varName = []
	for dict in listOfDict:
		for key,value in dict.items():
			if key not in varName:
				varName.append(key)
	df = pd.DataFrame(listOfDict)
	if 'unit_id' in varName:
		if 'latitude' in varName:
			if 'longitude' in varName:
				listOflist = [[df['unit_id'][i],df['latitude'][i],df['longitude'][i]] for i in range(len(df['unit_id']))]
	else:
		raise KeyError("Thera is no key like (\"unit_id\",\"latitude\",\"longitude\")")
	return listOflist

def _DBSCAN(data, dataframe, eps, min_samples):

    db = DBSCAN(eps=eps, min_samples=min_samples).fit(data)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    print (n_clusters_)
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
        print (xy)
        if k == -1:
            outlier.append(xy)

    main_dict = {} ; lat_dict = {} ; long_dict = {} 
    lat_id = {} ; long_id = {} ; id = {}

    for i in range(len(cluster)-1):
        lat_dict[str(i+1)] = []
        long_dict[str(i+1)] = []
        id[str(i+1)] = []
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
                for l in range(len(dataframe["unit_id"])):
                	if float(cluster[i][j][k][0]) == float(dataframe["latitude"][l]) and \
                		float(cluster[i][j][k][1]) == float(dataframe["longitude"][l]):
                		id[str(i+1)].append(dataframe["unit_id"][l])

    try:
    	lat_dict["outlier"] = [] ; long_dict["outlier"] = []
    	for i in range(len(outlier[0])):
    		lat_dict["outlier"].append(outlier[0][i][0])
    		long_dict["outlier"].append(outlier[0][i][1])
    except Exception:
    	print ("No outlier datas")

    main_dict["latitude"] = lat_dict
    main_dict["longitude"] = long_dict
    main_dict["id"] = id
    
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
    data = loadData("data.csv", "unit_id", "latitude", "longitude", start_column=1)
    main_dict = _DBSCAN(data[0], data[1], 0.02, 2.0)
    for id in range(len(main_dict["latitude"]["outlier"])):
        cluster_number = FindCluster(main_dict, id)













