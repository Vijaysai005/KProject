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
import datetime


start_time = datetime.datetime(year=2017,month=3,day=25,hour=1,minute=0,second=0)
end_time = datetime.datetime(year=2017,month=3,day=26,hour=1,minute=0,second=0)

if __name__ == "__main__":
	
	# INPUT DATA
	# listOfDict = [{'unit_id':1410656,'latitude':18.092, 'longitude':74.065},{'unit_id':1410657,'latitude':18.053, 'longitude':74.066},\
	# 	{'unit_id':1410658,'latitude':18.054, 'longitude':74.067}]

	client = MongoClient('localhost', 27017)
	db = client.maximus_db
	coll = db.device_data

	and1 = "$and"
	gt1 = "$gte"


	for hr in range(24):
		print (str(hr) +" hrs")
		
		mins = coll.find({"$and": [{"utc_time_hour":hr},{"date_part":"2017-03-25"}]},{"utc_time_min":1,"_id":0})
		
		time_min = []
		for m in mins:
			time_min.append(m["utc_time_min"])


		for time in set(time_min):
			items = coll.find({and1: [{"utc_time_hour":hr},{"utc_time_min":time},{"utc_time_sec":{gt1:48}}\
				,{"date_part":"2017-03-25"}]},{"unit_id":1,"latitude":1,"longitude":1,"_id":0})
			
			listOfDict = [] ; item_id = []
			for item in items:
					listOfDict.append(item)

			print (listOfDict)
			listOflist = cl.DictToList(listOfDict)
			data = cl.loadData(listOflist, "unit_id", "latitude", "longitude", start_column=1)
			main_dict,n_cluster = cl.cluster(data[0], data[1], 0.045, 2)

			#print (n_cluster)
			print (main_dict)

			# for id in range(len(main_dict["outlier"])):
			# 	cluster_number = cl.FindCluster(main_dict, id)