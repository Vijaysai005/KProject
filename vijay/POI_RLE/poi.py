# usr/bin/env python

"""
Created on Fri Jun 23
@author : Vijayasai S
"""
import csv
import gmplot

from getdata import GetData
from timedate import DateMonthYear, HoursMinutesSeconds
from createdictionary import CreateDirectory, CreateDictionary
from rle import FindIndex
from nearby_places import nearby
from datetime import datetime

start_time = datetime.now()

gmap = gmplot.GoogleMapPlotter(25, 70, 5)

def POI(time, data):

	def TimeInMinutes(hours, minutes, seconds):
		return 60*hours + minutes + (seconds/60.0)
	
	date, month, year = DateMonthYear(data)
	hours, minutes, seconds = HoursMinutesSeconds(data)
	
	data1 = data["ignition_status"]
	output = FindIndex(data1)
	time_data = [] 
	lat_10 = [] ; long1_10 = []
	lat_20 = [] ; long1_20 = []
	lat_30 = [] ; long1_30 = []
	lat_more = [] ; long1_more = []
	filepath = "POI/POI.csv"
	CreateDirectory(filepath)
	filepath2 = "POI/POI_only_lat_long.csv"
	CreateDirectory(filepath2)

	with open(filepath, "w") as doc:
		doc.write(str("Latitude") + "," + str("Longitude") + "," + str("Duration") + "\n")
		with open(filepath2, "w") as doc2:
			doc2.write(str("Latitude") + "," + str("Longitude") + "\n")
			for i in range(len(output)):
				time_value = []
				for j in range(len(output[i])):
					time_value.append(TimeInMinutes(int(hours[output[i][j]]), int(minutes[output[i][j]]), float(seconds[output[i][j]])))
				
				time_data.append(time_value[1] - time_value[0]) 
				if time_value[1] - time_value[0] > 0 and time_value[1] - time_value[0] < 10.0:
					lat_10.append(float(data["latitude"][output[i][0]]))
					long1_10.append(float(data["longitude"][output[i][0]]))
				if time_value[1] - time_value[0] > 10.0 and time_value[1] - time_value[0] < 20.0:
					lat_20.append(float(data["latitude"][output[i][0]]))
					long1_20.append(float(data["longitude"][output[i][0]]))
				if time_value[1] - time_value[0] > 20.0 and time_value[1] - time_value[0] < 30.0:
					lat_30.append(float(data["latitude"][output[i][0]]))
					long1_30.append(float(data["longitude"][output[i][0]]))
				if time_value[1] - time_value[0] > 30.0:
					lat_more.append(float(data["latitude"][output[i][0]]))
					long1_more.append(float(data["longitude"][output[i][0]]))

				doc.write(str(data["latitude"][output[i][0]]) + "," + str(data["longitude"][output[i][0]] \
					+ "," + str(time_value[1] - time_value[0]) + "\n"))	
				doc2.write(str(data["latitude"][output[i][0]]) + "," + str(data["longitude"][output[i][0]] + "\n"))
	
	lat_near, long_near = nearby("POI/POI_only_lat_long.csv", 200.0)
	#gmap.plot(lat, long1, 'cornflowerblue', edge_width=10)
	gmap.scatter(lat_10, long1_10, '#3B0B39', size=200, marker=False)
	gmap.scatter(lat_10, long1_10, 'r', marker=True)
	
	gmap.scatter(lat_20, long1_20, '#3B0B39', size=200, marker=False)
	gmap.scatter(lat_20, long1_20, 'b', marker=True)
	
	gmap.scatter(lat_30, long1_30, '#3B0B39', size=200, marker=False)
	gmap.scatter(lat_30, long1_30, 'g', marker=True)
	
	gmap.scatter(lat_more, long1_more, '#3B0B39', size=200, marker=False)
	gmap.scatter(lat_more, long1_more, 'y', marker=True)
	#gmap.heatmap(lat, long1)
	#gmap.plot(lat_near, long_near, 'cornflowerblue', edge_width=10)
	#gmap.scatter(lat_near, long_near, '#3B0B39', size=200, marker=False)
	gmap.scatter(lat_near, long_near, 'k', marker=True)
	#gmap.heatmap(lat_near, long_near)

	gmap.draw("mymap.html")
	return time_data

if __name__ == "__main__":
	filename = "1410656_9_16.csv" #raw_input("Enter the filename: ") 
	time = 30.0 #float(raw_input("Enter the limit-time for the pitstops: "))	
		
	dict = CreateDictionary(filename)
	data = GetData(dict,filename)	
	time_data = POI(time, data)

end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))
# gmap.scatter(more_lats, more_lngs, '#3B0B39', size=40, marker=False)
# gmap.scatter(marker_lats, marker_lngs, 'k', marker=True)
# gmap.heatmap(heat_lats, heat_lngs)

# gmap.draw("mymap.html")
