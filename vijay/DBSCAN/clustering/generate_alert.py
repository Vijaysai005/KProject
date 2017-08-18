# usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 13:15:05 2017

@author: Vijayasai S
"""
# Use python3

import numpy as np

from pymongo import MongoClient
from datetime import datetime
from operator import itemgetter
from haversine import distance
from mongo_update import centroid

def TimeInMinutes(hours, minutes, seconds):
	return 60*int(hours) + int(minutes) + (int(seconds) / 60)

def ClusterCenter(cen_lat, cen_long, max_cluster):
	lat_x = [[] for i in range(max_cluster)] ; long_x = [[] for i in range(max_cluster)]
	for m in range(len(cen_lat)):
		for n in range(len(cen_lat[m])):
			try:
				x_lat,x_long = centroid(cen_lat[m][n],cen_long[m][n])
				lat_x[n].append(x_lat)
				long_x[n].append(x_long)
			except ZeroDivisionError:
				lat_x[n].append(None)
				long_x[n].append(None)
	return lat_x, long_x

def DistanceArray(lat_x, long_x, max_cluster):
	TotDist = [[] for i in range(max_cluster)]
	for i in range(max_cluster):
		for j in range(len(lat_x[i]) - 1):
			if lat_x[i][j] == None or lat_x[i][j+1] == None:
				TotDist[i].append(0)
			else:
				TotDist[i].append(distance(lat_x[i][j], lat_x[i][j+1], long_x[i][j], long_x[i][j+1]))
	return TotDist

def normal_distance(x1,x2,y1,y2):
	return np.sqrt((x2 - x1)**2 + (y2-y1)**2)

def direction(TotDist, max_cluster, lat_x, long_x, OutClus_lat, OutClus_long, latest_data, time_stamp, l):
	#print (lat_x)
	#print (OutClus_lat)
	for i in range (max_cluster):
		for j in range(len(TotDist[i])):
			if TotDist[i][j] == 0:
				continue
			else:
				try:
					#print (time_stamp[j+1],OutClus_lat[time_stamp[j+1]])
					clus_dist = normal_distance(lat_x[i][j],lat_x[i][j+1],long_x[i][j],long_x[i][j+1])
					out_dist = normal_distance(lat_x[i][j],OutClus_lat[time_stamp[j+1]][l],long_x[i][j],OutClus_long[time_stamp[j+1]][l])
					if (clus_dist - out_dist) > 0:
						return True
					else:
						return False

				except Exception:
					pass
					

def Generate_Alert(ride_id, cluster_instance, threshold_minute):

	"""
	Parameters
    ----------
    ride_id : int, required
        The id number given for particular ride.
    cluster_instance : int, required
        No. of latest cluster instances should be taken.
    threshold_minute : int, required
        The minute required to check whether the biker is outside the
        	cluster or not
	"""

	client = MongoClient("localhost", 27017)
	collection = client.maximus_db.clus

	current_time = datetime(2017,3,26,14,10)

	#############################################################################
	if ride_id is None:
		items = collection.find({"timestamp":{"$lte":current_time}},{"timestamp":1,"cluster_number":1,"unit_id":1,"latitude":1,"longitude":1,"_id":0}).sort([("timestamp", -1)])
	elif ride_id is not None:
		items = collection.find({"$and": [{"timestamp":{"$lte":current_time}},{"ride_id":ride_id}]},{"timestamp":1,"cluster_number":1,"unit_id":1,"latitude":1,"longitude":1,"_id":0}).sort([("timestamp", -1)])

	data = [item for item in items]
	latest_data = sorted(data[:cluster_instance], key=itemgetter('timestamp'))

	#print (latest_data)
	try:
		max_cluster = int(max([latest_data[i]["cluster_number"] for i in range(cluster_instance) if latest_data[i]["cluster_number"] != "outlier"]))
	except ValueError:
		max_cluster = 1

	#############################################################################
	# INITIALIZED ARRAY DATA VARIABLES
	#############################################################################

	FixClus = [[] for i in range(max_cluster)]
	OutClus = {} ; timeFixClus = []
	OutClus_lat = {} ; OutClus_long = {}

	current_time_stamp = latest_data[0]["timestamp"]
	OutClus[current_time_stamp] = [] ; OutClus_lat[current_time_stamp] = []
	OutClus_long[current_time_stamp] = []

	cluster_centre_lat = [[] for i in range(max_cluster)] ; cluster_centre_long = [[] for i in range(max_cluster)]
	cen_lat = [] ; cen_long = [] ; 	time_stamp = []

	#############################################################################
	# SAVIND THE DATA IN THEIR RESPACTIVE ARRAY
	#############################################################################

	for i in range(cluster_instance):
		#print (latest_data[i]["latitude"], latest_data[i]["longitude"])
		if latest_data[i]["timestamp"] != current_time_stamp:
			
			cen_lat.append(cluster_centre_lat)
			cen_long.append(cluster_centre_long)
	
			timeFixClus.append(FixClus) 
			
			try:
				FixClus = [[] for i in range(max_cluster)]
				cluster_centre_lat = [[] for i in range(max_cluster)]
				cluster_centre_long = [[] for i in range(max_cluster)]
			except ValueError:
				pass

			time_stamp.append(current_time_stamp)
			current_time_stamp = latest_data[i]["timestamp"]
			OutClus[current_time_stamp] = []
			OutClus_lat[current_time_stamp] = []
			OutClus_long[current_time_stamp] = []

		if latest_data[i]["cluster_number"] != "outlier":

			FixClus[latest_data[i]["cluster_number"] - 1].append(latest_data[i]["unit_id"])
			cluster_centre_lat[latest_data[i]["cluster_number"] - 1].append(latest_data[i]["latitude"])
			cluster_centre_long[latest_data[i]["cluster_number"] - 1].append(latest_data[i]["longitude"])
			
			for j in range(max_cluster):
				if j != latest_data[i]["cluster_number"] - 1:
					try:
						FixClus[j].remove(latest_data[i]["unit_id"])
					except ValueError:
						pass
		
		if latest_data[i]["cluster_number"] == "outlier":
			OutClus[current_time_stamp].append(latest_data[i]["unit_id"])
			OutClus_lat[current_time_stamp].append(latest_data[i]["latitude"])
			OutClus_long[current_time_stamp].append(latest_data[i]["longitude"])

	timeFixClus.append(FixClus)
	cen_lat.append(cluster_centre_lat)
	cen_long.append(cluster_centre_long)
	time_stamp.append(current_time_stamp)

	lat_x, long_x = ClusterCenter(cen_lat,cen_long,max_cluster)
	TotDist = DistanceArray(lat_x,long_x,max_cluster)

	#############################################################################
	# GENERATING THE ALERT
	#############################################################################
	current_time_stamp = latest_data[0]["timestamp"]
	date_index = 0
	for i in range(cluster_instance):
		if latest_data[i]["timestamp"] != current_time_stamp:
			
			diff = abs(current_time_stamp - latest_data[i]["timestamp"])
			diff = TimeInMinutes(str(diff)[0:1], str(diff)[2:4], str(diff)[5:7])
			for l in range(len(OutClus[current_time_stamp])):
				
				sum_min = 0 ; PreClus = 1
				for m in range(date_index+1):
					for n in range(max_cluster):

						if OutClus[current_time_stamp][l] in timeFixClus[m][n]:
							try:
								dist = distance(OutClus_lat[current_time_stamp][l],lat_x[n][date_index-1],OutClus_long[current_time_stamp][l],long_x[n][date_index-1])
							except TypeError:
								pass
							sum_min += diff
							PreClus = n + 1
			
				if sum_min >= threshold_minute:
					for p in range(max_cluster):
						if OutClus[current_time_stamp][l] in timeFixClus[date_index-1][p]:
							if direction(TotDist, max_cluster, lat_x, long_x, OutClus_lat, OutClus_long, latest_data, time_stamp, l) is True:
								print ("Alert (",current_time_stamp,") :",OutClus[current_time_stamp][l],"is outside of cluster",PreClus, "and the biker is fallen behind by ",dist, "km")
							elif direction(TotDist, max_cluster, lat_x, long_x, OutClus_lat, OutClus_long, latest_data, time_stamp, l) is False:
								print ("Alert (",current_time_stamp,") :",OutClus[current_time_stamp][l],"is outside of cluster",PreClus, "and the biker is move ahead by ",dist, "km")

			current_time_stamp = latest_data[i]["timestamp"]
			date_index += 1

if __name__ == "__main__":
	Generate_Alert(None, 200, 1)



