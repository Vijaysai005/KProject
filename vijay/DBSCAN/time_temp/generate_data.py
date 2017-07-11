# -*- coding: utf-8 -*-
"""
Created on Fri Jul 07 12:53:37 2017

@author: Vijayasai S
"""
import numpy as np

def bikerid(no_of_bikers):
	bikers_id = {}
	for i in range(no_of_bikers):
		bikers_id[i] = []
	return bikers_id

def generate_lat_long(no_of_bikers, change, fractional_change, mod_number, max_grp_string, lat=[],long=[]):
	j = 0
	for i in range(no_of_bikers):
		if j % mod_number == 0:
			change = change + fractional_change * change + fractional_change * change**2
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

def timeData(lat1, long1, no_of_bikers, change, fractional_change, time_change, mod_number, max_grp_string, time):
	time_dict = {}
	for i in range(time):
		lat,long = generate_lat_long(no_of_bikers, change, fractional_change, mod_number, max_grp_string, [lat1], [long1])
		bikers_id = generate_data(lat,long, no_of_bikers)
		time_dict[i] = bikers_id
		lat1 = lat1 + time_change + (time_change)**2
		long1 = long1 + time_change
	return time_dict

import load_data, dbscan

lat1 = 18.052 ; long1 = 74.552
no_of_bikers = 100 ; max_grp_string = 10
time = 20 ; time_change = 1
change = 0.012345 ; fractional_change = 0.5
mod_number = max_grp_string

time_dict = timeData(lat1, long1, no_of_bikers, change, fractional_change, time_change, mod_number, max_grp_string, time)

for i in range(time):
	data = []
	with open("time_"+str(i)+".csv", "w") as csv_file:
		for j in range(no_of_bikers):
			csv_file.write(str(time_dict[i][j][0]) + "," + str(time_dict[i][j][1]) + "\n")


eps = (float(input("Enter the value maximum distance for forming cluster in km: ")) * 180. ) / (6371. * np.pi)
for i in range(time):
	data = dbscan.loadData("time_" + str(i) + ".csv", "latitude", "longitude")
	n_clusters, labels, unique_labels, colors, core_samples_mask = dbscan.algorithm(data, eps, 2.0)
	cluster, outlier = dbscan.ClusterPlot(data, n_clusters, labels, unique_labels, colors, core_samples_mask, \
		i, [long1, long1+40], [lat1, lat1+40])
	main_dict = dbscan.dataInDict(cluster,outlier,{})
