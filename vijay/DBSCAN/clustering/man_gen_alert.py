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

def Generate_alert(df, coll):

	"""
	Parameters
    ----------
    df : dataframe, required
    	The dataframe for cluster creation.
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
		#print (sorted_df)

		alert = [[] for m in range(sorted_df.shape[0])]
		for k in range(sorted_df.shape[0]):
			if sorted_df["cluster_number"][k] == "outlier":
				alert[k].append("You are outside the cluster")
				for c in range(k):
					if "You are outside the cluster" not in alert[c]:
						if sorted_df["rank"][k] == 1:
							alert[c].append("unit_id "+str(sorted_df["unit_id"][k])+" is move ahead of your cluster "+ str(sorted_df["cluster_number"][c]) + " by " +str(sorted_df["dist_diff"][k+1]) + " km" )
						elif sorted_df["rank"][k] == sorted_df.shape[0]:
							alert[c].append("unit_id "+str(sorted_df["unit_id"][k])+" is left behind of your cluster "+ str(sorted_df["cluster_number"][c]) + " by " +str(sorted_df["dist_diff"][k]) + " km")
						elif sorted_df["rank"][k] < sorted_df["rank"][c]:
							alert[c].append("unit_id "+str(sorted_df["unit_id"][k])+" is move ahead of your cluster "+ str(sorted_df["cluster_number"][c]) + " by " +str(sorted_df["dist_diff"][k+1]) + " km")
						elif sorted_df["rank"][k] > sorted_df["rank"][c]:
							alert[c].append("unit_id "+str(sorted_df["unit_id"][k])+" is left behind of your cluster "+ str(sorted_df["cluster_number"][c]) + " by " +str(sorted_df["dist_diff"][k+1]) + " km")

				for b in range(k+1,sorted_df.shape[0]):
					if "You are outside the cluster" not in alert[b]:
						if sorted_df["rank"][k] == 1:
							alert[b].append("unit_id "+str(sorted_df["unit_id"][k])+" is move ahead of your cluster "+ str(sorted_df["cluster_number"][b]) + " by " +str(sorted_df["dist_diff"][k+1]) + " km")
						elif sorted_df["rank"][k] == sorted_df.shape[0]:
							alert[b].append("unit_id "+str(sorted_df["unit_id"][k])+" is left behind of your cluster "+ str(sorted_df["cluster_number"][b]) + " by " +str(sorted_df["dist_diff"][k]) + " km")
						elif sorted_df["rank"][k] < sorted_df["rank"][b]:
							alert[b].append("unit_id "+str(sorted_df["unit_id"][k])+" is move ahead of your cluster "+ str(sorted_df["cluster_number"][b]) + " by " +str(sorted_df["dist_diff"][k+1]) + " km")
						elif sorted_df["rank"][k] > sorted_df["rank"][b]:
							alert[b].append("unit_id "+str(sorted_df["unit_id"][k])+" is left behind of your cluster "+ str(sorted_df["cluster_number"][b]) + " by " +str(sorted_df["dist_diff"][k+1]) + " km")

			elif sorted_df["cluster_number"][k] != "outlier":
				for d in range(k):
					if sorted_df["cluster_number"][d] != "outlier" and sorted_df["cluster_number"][k] != sorted_df["cluster_number"][d]:
						if sorted_df["cluster_number"][k] < sorted_df["cluster_number"][d]:
							if "cluster "+str(sorted_df["cluster_number"][k])+" is move ahead of your cluster "+ str(sorted_df["cluster_number"][d]) not in alert[d]:
								alert[d].append("cluster "+str(sorted_df["cluster_number"][k])+" is move ahead of your cluster "+ str(sorted_df["cluster_number"][d]))
						elif sorted_df["cluster_number"][k] > sorted_df["cluster_number"][d]:
							if "cluster "+str(sorted_df["cluster_number"][k])+" is left behind of your cluster "+ str(sorted_df["cluster_number"][d]) not in alert[d]:
								alert[d].append("cluster "+str(sorted_df["cluster_number"][k])+" is left behind of your cluster "+ str(sorted_df["cluster_number"][d]))

				for e in range(k+1,sorted_df.shape[0]):
					if sorted_df["cluster_number"][e] != "outlier" and sorted_df["cluster_number"][k] != sorted_df["cluster_number"][e]:
						if sorted_df["cluster_number"][k] < sorted_df["cluster_number"][e]:
							if "cluster "+str(sorted_df["cluster_number"][k])+" is move ahead of your cluster "+ str(sorted_df["cluster_number"][e]) not in alert[e]:
								alert[e].append("cluster "+str(sorted_df["cluster_number"][k])+" is move ahead of your cluster "+ str(sorted_df["cluster_number"][e]))
						elif sorted_df["cluster_number"][k] > sorted_df["cluster_number"][e]:
							if "cluster "+str(sorted_df["cluster_number"][k])+" is left behind of your cluster "+ str(sorted_df["cluster_number"][e]) not in alert[e]:
								alert[e].append("cluster "+str(sorted_df["cluster_number"][k])+" is left behind of your cluster "+ str(sorted_df["cluster_number"][e]))


		alert_info = pd.Series(alert)
		sorted_df = sorted_df.assign(alert_info=alert_info.values)
		#print (sorted_df["alert_info"])

		ld = sorted_df.values.tolist()
		
		#print (sorted_df.shape[0])
		for a in range(sorted_df.shape[0]):
			coll.insert([{"distance_by_interval":ld[a][2], "unit_id":ld[a][6], "rank":ld[a][4],"timestamp":ld[a][5],\
					"flag":ld[a][3],"dist_diff":ld[a][1],"cluster_number":ld[a][0], "alert_info":ld[a][7]}])
		j = i

	return

if __name__ == "__main__":

	table_to_read = "tapola_rank_15_manual_clustering"
	ride_id = None 
	df = read_mongo("maximus_db", table_to_read, {"ride_id":ride_id})

	client = MongoClient("localhost", 27017)
	coll = client.maximus_db.tapola_rank_15_manual_clus_alert

	Generate_alert(df, coll)