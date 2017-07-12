# usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 13:15:05 2017

@author: Vijayasai S
"""
# Use python3

import DBSCAN

if __name__ == "__main__":
	
	# INPUT DATA
	listOfDict = [{'unit_id':1410656,'latitude':18.052, 'longitude':74.065},{'unit_id':1410657,'latitude':18.053, 'longitude':74.066},\
		{'unit_id':1410658,'latitude':18.054, 'longitude':74.067}]

	listOflist = DBSCAN.DictToList(listOfDict)
	data = DBSCAN.loadData(listOflist, "unit_id", "latitude", "longitude", start_column=1)
	main_dict = DBSCAN._DBSCAN(data[0], data[1], 0.02, 2.0)
	print (main_dict)
	for id in range(len(main_dict["latitude"]["outlier"])):
		cluster_number = DBSCAN.FindCluster(main_dict, id)