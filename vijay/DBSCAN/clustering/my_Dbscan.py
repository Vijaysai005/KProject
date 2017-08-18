# usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 13:15:05 2017

@author: Vijayasai S
"""
# Use python3

import numpy as np
from pymongo import MongoClient
from haversine import distance

from datetime import datetime
from dateutil import tz

import pandas as pd
import json

from_zone = tz.tzutc()
to_zone = tz.tzlocal()


def _connect_mongo(host, port, username, password, db):
    """ A util for making a connection to mongo """

    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)

    return conn[db]


def read_mongo(db, collection, query={}, host='localhost', port=27017, username=None, password=None, no_id=True):
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    db = _connect_mongo(host=host, port=port, username=username, password=password, db=db)

    # Make a query to the specific DB and Collection
    cursor = db[collection].find(query)

    # Expand the cursor and construct the DataFrame
    df =  pd.DataFrame(list(cursor))

    # Delete the _id
    if no_id:
        del df['_id']

    return df

def persist_to_mongo(db, collection, df, host='localhost', port=27017):

	client = MongoClient(host, port)
	coll = client.db[collection]

	ld = df.values.tolist()

	for i in range(df.shape[0]):
		#print (df["unit_id"][i])
		#coll.insert([{"distance/interval":df["distance/interval"][i], "unit_id":df["unit_id"][i], "rank":df["rank"][i],"timestamp":df["timestamp"][i],\
				#"flag":df["flag"][i],"dist_diff":df["pair"][i],"cluster_number":df["clus_n"][i]}])
		coll.insert([{"distance_by_interval":ld[i][0], "unit_id":ld[i][3], "rank":ld[i][1],"timestamp":ld[i][2],\
				"flag":ld[i][4],"dist_diff":ld[i][5],"cluster_number":ld[i][6]}])
	return

def isNaN(num):
    return num != num

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
	curr_time_stamp = df["timestamp"][0] ; j = 0
	
	for i in range(df.shape[0]):

		if curr_time_stamp == df["timestamp"][i]:
			curr_time_stamp = df["timestamp"][i]
			continue
		elif curr_time_stamp != df["timestamp"][i]:
			curr_time_stamp = df["timestamp"][i]

		sorted_df = df[j:i].sort_values(by=["rank"], ascending=True)
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
			coll.insert([{"distance_by_interval":ld[a][0], "unit_id":ld[a][3], "rank":ld[a][1],"timestamp":ld[a][2],\
					"flag":ld[a][4],"dist_diff":ld[a][5],"cluster_number":ld[a][6]}])
		#print (cluster_number)
		j = i
	return sorted_df


if __name__  == "__main__":
	
	table_to_read = "tapola_rank_15_curr" 

	client = MongoClient("localhost", 27017)
	coll = client.maximus_db.tapola_rank_15_manual_clustering
	
	df = read_mongo("maximus_db", table_to_read)
	manual_DBSCAN(df, coll, 5.0)