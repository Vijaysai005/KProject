# usr/bin/env python

"""
Created on Fri Jun 23
@author : Vijayasai S
"""

import csv

from timedate import DateTimeYear , HoursMinutesSeconds
from ignitionstatus import IgnitionStatus


def distance_daily_basis(data):
	date, month, year = DateTimeYear(data)
	hours, minutes, seconds = HoursMinutesSeconds(data)

	current_date = date[0] ;current_month = month[0] ; current_year = year[0]

	sum_dist = 0.0
	dist = []

	latitude = [] ; longitude = []
	no_of_days = 0

	new_date = [] ; new_month = [] ; new_year = []
	for index in range(len(data["packettimestamp"]) - 1):
		if IgnitionStatus(data["ignition_status"][index]) is True:
			
			new_year.append(year[index])
			new_month.append(month[index])
			new_date.append(date[index])

			latitude.append(data["latitude"][index])
			longitude.append(data["longitude"][index])
			
	for j in range(len(latitude)-1):
		with open("distance/Distance_"+str(current_year)+"-"+str(current_month)+"-" +str(current_date)+".txt", "w") as doc:
			writer = csv.writer(doc, delimiter=',',quotechar=" ")
			sum_dist = sum_dist + distance(latitude[j], latitude[j+1], longitude[j], longitude[j+1])

			if new_date[j] != current_date or new_month[j] != current_month or new_year[j] != current_year:

				writer.writerow([str(sum_dist -  (distance(latitude[j], latitude[j+1], \
					longitude[j], longitude[j+1])))])
				
				if year[j] >= 2017:
					if month[j] >= 6:
						if date[j] >= 9: 
							no_of_days += 1
							print "Distance travelled on " + str(new_date[j-1]) + "-" + str(new_month[j-1]) + "-" + str(new_year[j-1]) + ": ",\
								str(sum_dist -  (distance(latitude[j], latitude[j+1], \
									longitude[j], longitude[j+1])))

				dist.append(sum_dist -  (distance(latitude[j], latitude[j+1], \
					longitude[j], longitude[j+1])))

				current_date = new_date[j]
				current_month = new_month[j]
				current_year = new_year[j]

				sum_dist = 0.0

			if new_date[j] == new_date[-1] and new_month[j] == new_month[-1] and new_year[j] == new_year[-1]:

				writer.writerow([str(sum_dist -  (distance(latitude[j], latitude[j+1], \
					longitude[j], longitude[j+1])))])

				dist.append(sum_dist -  (distance(latitude[j], latitude[j+1], \
					longitude[j], longitude[j+1])))

			if j == len(latitude) - 2:
				print "Distance travelled on " + str(new_date[j]) + "-" + str(new_month[j]) + "-" + str(new_year[j]) + ": " + \
					str(sum_dist -  (distance(latitude[j], latitude[j+1], \
						longitude[j], longitude[j+1]))) + " till " + str(hours[-1]) + ":" + str(minutes[-1])
				no_of_days += 1

	TotalDistance = FindingDistance(data)
	print "\nTotal distance travelled: " + str(TotalDistance) + " km"
	print "Average distance travelled: " + str(TotalDistance/float(no_of_days)) + " km"
	maxSpeed, AvgSpeed = Speed(data)
	print "Maximum speed achieved: " + str(maxSpeed) + " km/hr"
	print "Average speed of the bike: " + str(AvgSpeed) + " km/hr\n"
	
	return
