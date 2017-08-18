# -*- coding: utf-8 -*-
"""
Created on Fri Jul 07 12:53:37 2017

@author: Vijayasai S
"""

def bikerid(no_of_bikers):
	bikers_id = {}
	for i in range(no_of_bikers):
		bikers_id[i] = []
	return bikers_id

def generate_lat_long(no_of_bikers, change, max_grp_string, lat=[],long=[]):
	j = 0
	for i in range(no_of_bikers):
		if j%10 == 0:
			change = change + 0.01*change + 0.01*change**2
		if j < max_grp_string:
			lat.append(lat[i]+change)
			long.append(long[i]+change)
		else:
			lat.append(lat[i-max_grp_string]+change)
			long.append(long[i-max_grp_string]+change)	
		j += 1
	return lat, long

def generate_data(lat,long,no_of_bikers):
	bikers_id = bikerid(no_of_bikers)
	for i in range(no_of_bikers):
		bikers_id[i].append(lat[i])
		bikers_id[i].append(long[i])
	return bikers_id

def timeData(lat1,long1,no_of_bikers,max_grp_string, time):
	time_dict = {}
	for i in range(time):
		lat,long = generate_lat_long(no_of_bikers, 0.00012345, max_grp_string, [lat1], [long1])
		bikers_id = generate_data(lat,long, no_of_bikers)
		time_dict[i] = bikers_id
		lat1 = lat1 + 0.001
		long1 = long1 + 0.001
	return time_dict

from DBSCAN import dbscan
#from DBSCAN import db_scan as ds

lat1 = 18.052 ; long1 = 74.552
no_of_bikers = 200
max_grp_string = 10
time = 10
time_dict = timeData(lat1, long1, no_of_bikers, max_grp_string, time)
#print (time_dict)

for i in range(time):
	data = []
	for j in range(no_of_bikers):
		with open("DBSCAN/time_"+str(i)+".csv", "a") as csv_file:
			csv_file.write(str(time_dict[i][j][0]) + "," + str(time_dict[i][j][1]) + "\n")


eps = float(input("Enter the value maximum distance for forming cluster: "))
for i in range(time):
	data = dbscan.loadData("time_" + str(i) + ".csv", "latitude", "longitude")
	n_clusters, labels, unique_labels, colors, core_samples_mask = dbscan.algorithm(data, 0.02, 2.0)
	cluster, outlier = dbscan.ClusterPlot(data, n_clusters, labels, unique_labels, colors, core_samples_mask)
	main_dict = dbscan.dataInDict(cluster,outlier,{})
