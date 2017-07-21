# usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 13:15:05 2017

@author: Vijayasai S
"""
# Use python3

import Cluster as cl
from pymongo import MongoClient

import numpy as np
from datetime import datetime

def centroid(lati=[],longi=[]):
	x = sum(lati) / len(lati)
	y = sum(longi) / len(longi)
	return x,y


def mongoCluster(get_col, set_col, year, month, startday, endday):
	for day in range(startday,endday+1):
		for hr in range(24):
			for mins in range(59):
				items = get_col.find({"$and" :[{"packettimestamp":{"$gte":datetime(year,month,day,hr,mins,0)}},{"packettimestamp":{"$lte":datetime(year,month,day,hr,mins+1,0)}}]},{"unit_id":1,"latitude":1,"longitude":1,"_id":0}).sort([("packettimestamp", -1)])
				
				data = [] ; item_id = []
				for item in items:
					if item["unit_id"] not in item_id:
						item_id.append(item["unit_id"])
						data.append(item)
				try:
					listOflist = cl.DictToList(data)
					data = cl.loadData(listOflist, "unit_id", "latitude", "longitude", start_column=1)
					main_dict,n_cluster = cl.cluster(data[0], data[1], 0.045, 2)
					
					for i in range(len(main_dict)):
						try:
							for j in range(len(main_dict[i])):
								set_col.insert([{"cluster_number": i, "unit_id": int(main_dict[i][j][0]), "latitude": main_dict[i][j][1],"longitude": main_dict[i][j][2], "timestamp":datetime(year,month,day,hr,mins)}])
						except Exception:
							for k in range(len(main_dict["outlier"])):
								set_col.insert([{"cluster_number": "outlier", "unit_id": int(main_dict["outlier"][k][0]), "latitude": main_dict["outlier"][k][1],"longitude": main_dict["outlier"][k][2], "timestamp":datetime(year,month,day,hr,mins)}])
								

					print (day,hr,mins)					
					if n_cluster == 0:
						lat_cen = [] ; long_cen = []
						for i in range(len(main_dict["outlier"])):	
							lat_cen.append(main_dict["outlier"][i][1])
							long_cen.append(main_dict["outlier"][i][2])
						cent_x,cent_y = centroid(lat_cen,long_cen)
					else:
						cent_x = [] ; cent_y = []
						for i in range(n_cluster):
							lat_cen = [] ; long_cen = []
							for j in range(main_dict[i]):
								lat_cen.append(main_dict[i][j][1])
								long_cen.append(main_dict[i][j][2])
							_x,_y = centroid(lat_cen,long_cen)
							cent_x.append(_x)
							cent_y.append(_y)
					#print (cent_x,cent_y)
				except KeyError:
					pass

	

	return main_dict, n_cluster, cent_x, cent_y

if __name__ == "__main__":

	client = MongoClient('localhost', 27017)
	db = client.maximus_db
	get_coll = db.device_data
	set_coll = db.clus

	startday = 25 ; endday = 26
	year = 2017 ; month = 3

	main_dict, n_cluster, cent_x, cent_y = mongoCluster(get_coll, set_coll, year, month, startday, endday) 			
	

