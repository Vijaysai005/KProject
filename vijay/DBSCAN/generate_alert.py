# usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 13:15:05 2017

@author: Vijayasai S
"""
# Use python3

from pymongo import MongoClient
from datetime import datetime

from operator import itemgetter

def TimeInMinutes(hours, minutes, seconds):
	return 60*int(hours) + int(minutes) + (int(seconds) / 60)

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

	current_time = datetime(2017,3,26,15,7)

	if ride_id is None:
		items = collection.find({"timestamp":{"$lte":current_time}},{"timestamp":1,"cluster_number":1,"unit_id":1,"latitude":1,"longitude":1,"_id":0}).sort([("timestamp", -1)])
		data = [item for item in items]
		latest_data = sorted(data[:cluster_instance], key=itemgetter('timestamp'))

		print (latest_data)
		current_time_stamp = latest_data[0]["timestamp"]
		sum_min = 0 ; diff = 0
		cluster_number = latest_data[0]["cluster_number"] 

		try:
			max_cluster = int(max([latest_data[i]["cluster_number"] for i in range(cluster_instance) if latest_data[i]["cluster_number"] != "outlier"]))
		except ValueError:
			max_cluster = 1

		curr_clus_id = [[] for i in range(max_cluster)] ; curr_out_id = [] ; fix_clus_id = [[] for i in range(max_cluster)]
		check_clus_list = [[] for i in range(max_cluster)]
		
		for i in range(cluster_instance):
			if latest_data[i]["timestamp"] != current_time_stamp:

				diff = abs(current_time_stamp - latest_data[i]["timestamp"])
				diff = TimeInMinutes(str(diff)[0:1], str(diff)[2:4], str(diff)[5:7])
				current_time_stamp = latest_data[i]["timestamp"]
				curr_out_id = []
				try:
					curr_clus_id[int(cluster_number)-1] = [] 
				except ValueError:
					pass
				

			
			#print (latest_data[i]["cluster_number"])
			if latest_data[i]["cluster_number"] != "outlier":

				cluster_number = latest_data[i]["cluster_number"]
				curr_clus_id[int(cluster_number)-1].append(latest_data[i]["unit_id"])	
				fix_clus_id[int(cluster_number)-1].append(latest_data[i]["unit_id"])
				#print (curr_clus_id)

				
			
			elif latest_data[i]["cluster_number"] == "outlier":
				cluster_number = latest_data[i]["cluster_number"]
				curr_out_id.append(latest_data[i]["unit_id"])

			
			#print (current_time_stamp)
			print (latest_data[i]["timestamp"])
			print (curr_clus_id)
			for a in range(len(curr_clus_id)):
				check_clus_list[a].append(curr_clus_id[a])
				#print (check_clus_list)
				#print (curr_clus_id)

			for j in range(len(curr_out_id)):
				for k in range(len(fix_clus_id)):
					if curr_out_id[j] in list(fix_clus_id)[k]:
						sum_min = sum_min + diff
					elif curr_out_id[j] not in list(fix_clus_id)[k]:
						sum_min = 0
					if sum_min >= threshold_minute:
						print ("unit_id: ",curr_out_id[j],"is outside of cluster number ",k+1)
		#print (check_clus_list)
		#print (check_clus_list)

if __name__ == "__main__":
	Generate_Alert(None, 100, 1)



