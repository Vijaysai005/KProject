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

import matplotlib.pyplot as plt
import gmplot

import urllib
import matplotlib.image as mpimg

def vplot(main_dict,n_cluster,tit, lat_cen=18,long_cen=74,size=800,zoom=10):
	
	gmap = gmplot.GoogleMapPlotter(18, 74, 10)
	fig = plt.figure()
	fig.suptitle(str(tit)+" No.of clusters: "+str(n_cluster))
	ax=fig.add_subplot(111)
	
	ax.set_xlabel("Latitude")
	ax.set_ylabel("Longitude")
	
	colors = ["r","b","g","k"]

	url = "http://maps.googleapis.com/maps/api/staticmap?center="+str(lat_cen)+","+str(long_cen)+"&size="+str(size)+"x"+str(size)+"&zoom="\
		+str(zoom)+"&sensor=false"

	gmap_static_file = urllib.request.urlopen(url)

	with open('./gmap_static.png','wb') as output:
	  output.write(gmap_static_file.read())

	im = plt.imread('./gmap_static.png')
	implot = plt.imshow(im, extent=[17,19,73,75])

	for i in range(1,n_cluster+1):
		lat_cl = [] ; long_cl = []
		for j in range(len(main_dict[i])):
			lat_cl.append(main_dict[i][j][1])
			long_cl.append(main_dict[i][j][2])
		ax.plot(lat_cl, long_cl, 'o', markerfacecolor=colors[i],markeredgecolor='k', markersize=14)
		gmap.scatter(lat_cl, long_cl, '#3B0B39', size=200, marker=False)
		gmap.scatter(lat_cl, long_cl, 'r', marker=True)
		plt.hold(True)
	lat_ol = [] ; long_ol = []
	for k in range(len(main_dict["outlier"])):
		lat_ol.append(main_dict["outlier"][k][1])
		long_ol.append(main_dict["outlier"][k][2])
	col = [0, 0, 0, 1]
	ax.plot(lat_ol, long_ol, 'o', markerfacecolor=tuple(col),
                         markeredgecolor='k', markersize=6)
	
	gmap.scatter(lat_ol, long_ol, '#3B0B39', size=50, marker=False)
	gmap.scatter(lat_ol, long_ol, 'k', marker=True)
	
	d = "PLOTS3/"+str(tit)
	#implot.title(str(tit)+" No.of clusters: "+str(n_cluster))
	fig.savefig(d)
	plt.close()

	gmap.draw("MAP/mymap_"+str(tit)+".html")

	return

def centroid(lati=[],longi=[]):
	x = sum(lati) / len(lati)
	y = sum(longi) / len(longi)
	return x,y

if __name__ == "__main__":
	
	# INPUT DATA
	# listOfDict = [{'unit_id':1410656,'latitude':18.092, 'longitude':74.065},{'unit_id':1410657,'latitude':18.053, 'longitude':74.066},\
	# 	{'unit_id':1410658,'latitude':18.054, 'longitude':74.067}]

	client = MongoClient('localhost', 27017)
	db = client.maximus_db
	coll = db.device_data

	startday = 25 ; endday = 26
	year = 2017 ; month = 3
	for day in range(startday,endday+1):
		for hr in range(2,15):
			for mins in range(60):
				if mins < 59:
					items = coll.find({"$and" :[{"ignition_status":1},{"gps_validity":1},{"packettimestamp":{"$gte":datetime(year,month,day,hr,mins,0)}},{"packettimestamp":{"$lte":datetime(year,month,day,hr,mins+1,0)}}]},\
						{"unit_id":1,"latitude":1,"longitude":1,"_id":0}).sort([("packettimestamp", -1)])
					
					data = [] ; item_id = []
					for item in items:
						if item["unit_id"] not in item_id:
							item_id.append(item["unit_id"])
							data.append(item)
					try:
						listOflist = cl.DictToList(data)
						data = cl.loadData(listOflist, "unit_id", "latitude", "longitude", start_column=1)
						main_dict,n_cluster = cl.cluster(data[0], data[1], 0.045, 2)

						print (day, hr)
						
						if n_cluster == 0:
							lat_cen = [] ; long_cen = []
							for i in range(len(main_dict["outlier"])):	
								lat_cen.append(main_dict["outlier"][i][1])
								long_cen.append(main_dict["outlier"][i][2])
							cent_x,cent_y = centroid(lat_cen,long_cen)
						else:
							lat_cen = [] ; long_cen = []
							mid = int(n_cluster / 2) + 1
							for i in range(len(main_dict[mid])):	
								lat_cen.append(main_dict[mid][i][1])
								long_cen.append(main_dict[mid][i][2])
							cent_x,cent_y = centroid(lat_cen,long_cen)
						
						IST_hr = hr + 5
						IST_min = mins + 30
						if IST_min >= 60:
							IST_hr = hr + 6
							IST_min = mins - 30 

						vplot(main_dict,n_cluster,str(day)+"-"+str(month)+"-"+str(year)+"_"+str(IST_hr)+":"+str(IST_min),lat_cen=cent_x,long_cen=cent_y,size=800, zoom=10)
						#print (cent_x,cent_y)
					except KeyError:
						pass


				
	
