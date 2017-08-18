# usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 13:15:05 2017

@author: Vijayasai S
"""
# Use python3

from haversine import distance

from datetime import datetime
from dateutil import tz

from_zone = tz.tzutc()
to_zone = tz.tzlocal()

def Generate_data(get_col, set_col1, set_col2, time_delay, year, month, startday, endday, starthr, endhr, startmin, endmin):
	id_dist = [] ; item_id_dist = []
	main_curr_rank = {} ; tot_rank_curr = {}
	count = 0

	set_col1.drop()
	set_col2.drop()
	
	for day in range(startday,endday+1): 
		for hr in range(starthr,endhr+1):
			for mins in range(startmin,endmin+1,time_delay):
				mins_next = mins + time_delay
				hr_next = hr
				if time_delay + mins > 59:
					mins_next = (time_delay + mins) - 60
					hr_next += 1
					if hr_next > 23:
						hr_next = 0
						day += 1
				#print (hr,mins)
				items = get_col.find({"$and" :[{"packettimestamp":{"$gte":datetime(year,month,day,hr,mins,0)}},{"packettimestamp":{"$lte":datetime(year,month,day,hr_next,mins_next,0)}}]},{"unit_id":1,"latitude":1,"longitude":1,"_id":0}).sort([("packettimestamp", -1)])
				
				utc = datetime(year,month,day,hr,mins)
				utc = utc.replace(tzinfo=from_zone)
				# Convert time zone
				ist = utc.astimezone(to_zone)

				data = [] ; item_id = []
				for item in items:
					if item["unit_id"] not in item_id:
						item_id.append(item["unit_id"])
						data.append(item)
					if item["unit_id"] not in item_id_dist:
						item_id_dist.append(item["unit_id"])
						id_dist.append(item)
				u_id = [ids["unit_id"] for ids in id_dist]

				count += 1
				if count > 0:
					
					rank_curr = {} ; lat_curr = {} ; long_curr = {}
					for item in item_id:
						if item in u_id:
							for i in range(len(id_dist)):
								if item == id_dist[i]["unit_id"]:
									for j in range(len(data)):
										if item == data[j]["unit_id"]:
											dist = distance(id_dist[i]["latitude"],data[j]["latitude"],id_dist[i]["longitude"],data[j]["longitude"])
											id_dist[i]["latitude"] = data[j]["latitude"]
											id_dist[i]["longitude"] = data[j]["longitude"]
											rank_curr[item] = dist
											lat_curr[item] = id_dist[i]["latitude"]
											long_curr[item] = id_dist[i]["longitude"]
											try:
												tot_rank_curr[item] = dist + main_curr_rank[item]
												main_curr_rank[item] = dist + main_curr_rank[item]
											except Exception:
												tot_rank_curr[item] = dist
												main_curr_rank[item] = dist
											#print (item, dist)
					rank_current_sorted = sorted(rank_curr.values(), reverse=True)
					tot_rank_current_sorted = sorted(tot_rank_curr.values(), reverse=True)
					#rank,r_id,dist_rank = [],[],[]
					for item in item_id:
						if rank_curr[item] in rank_current_sorted:
							set_col1.insert([{"latitude":lat_curr[item], "longitude":long_curr[item], "distance_by_interval":rank_curr[item], "unit_id":item, "rank":rank_current_sorted.index(rank_curr[item])+1,"timestamp":ist}])
							set_col2.insert([{"latitude":lat_curr[item], "longitude":long_curr[item], "distance_by_interval":tot_rank_curr[item], "unit_id":item, "rank":tot_rank_current_sorted.index(tot_rank_curr[item])+1,"timestamp":ist}])
				
	return	
	
