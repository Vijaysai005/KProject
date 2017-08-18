# usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 13:15:05 2017

@author: Vijayasai S
"""
# Use python3

import pandas as pd

def manual_DBSCAN(df, coll, maximum_distance):

	#print (df)

	"""
	Parameters
    ----------
    df : dataframe, required
        The dataframe for cluster creation.
    coll : collection table, required.
    	Give the table name to store the data in database.
    maximum_distance : float, required
        Give the maximum distance between two points in a cluster.
	"""
	
	coll.drop()

	df["timestamp"] = pd.to_datetime(df["timestamp"])
	sorted_df = df.sort_values(by=["timestamp"], ascending=True)
	curr_time_stamp = df["timestamp"][0] 

	sorted_df = df[0:df.shape[0]].sort_values(by=["rank"], ascending=True)
	sorted_df = sorted_df.reset_index(drop=True)

	pair_dist = [None] ; flag_dist = [None]
	for k in range(sorted_df.shape[0] - 1):
		pair_dist.append(sorted_df["distance_by_interval"][k] - sorted_df["distance_by_interval"][k+1])
		if pair_dist[k+1] > maximum_distance:
			flag_dist.append(1)
		elif pair_dist[k+1] <= maximum_distance:
			flag_dist.append(0)

	pair = pd.Series(pair_dist)
	flag = pd.Series(flag_dist)
	sorted_df = sorted_df.assign(pair=pair.values, flag=flag.values)

	cluster_number = [0 for m in range(sorted_df.shape[0])] ; clus_num = 1

	######################################################################################################
	# CLUSTER NUMBER PREDICTION
	######################################################################################################

	for n in range(sorted_df.shape[0]-1):
		if n == 1 and sorted_df["flag"][n] == 1:
			cluster_number[n-1] = "outlier"
		elif n == 1 and sorted_df["flag"][n] == 0:
			cluster_number[n-1] = clus_num
		if sorted_df["flag"][n] == 1 and sorted_df["flag"][n+1] == 1:
			cluster_number[n] = "outlier"
			#clus_num += 1
		if sorted_df["flag"][n] == 0:
			cluster_number[n] = clus_num
		elif sorted_df["flag"][n] == 1 and sorted_df["flag"][n+1] == 0:
			clus_num += 1
			cluster_number[n] = clus_num
		if n == sorted_df.shape[0] - 2 and sorted_df["flag"][n+1] == 1:
			cluster_number[n+1] = "outlier"
		if n == sorted_df.shape[0] - 2 and sorted_df["flag"][n+1] == 0:
			cluster_number[n+1] = clus_num

	if 1 not in cluster_number:
		for p in range(len(cluster_number)):
			if cluster_number[p] != "outlier":
				if cluster_number[p] > 1:
					cluster_number[p] = cluster_number[p] - 1 
	
	######################################################################################################
	
	clus_n = pd.Series(cluster_number)
	sorted_df = sorted_df.assign(clus_n=clus_n.values)	

	ld = sorted_df.values.tolist()
	
	#print (sorted_df.shape[0])
	for a in range(sorted_df.shape[0]):
		coll.insert([{"distance_by_interval":ld[a][0], "unit_id":ld[a][5], "rank":ld[a][3],"timestamp":ld[a][4],\
				"flag":ld[a][6],"dist_diff":ld[a][7],"cluster_number":ld[a][8], "latitude":ld[a][1], "longitude":ld[a][2]}])

	#print (cluster_number)
	
	return 
