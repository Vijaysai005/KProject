# usr/bin/env python

"""
Created on Fri Jun 23
@author : Vijayasai S
"""

def DateMonthYear(data):
	year = [] ; month = [] ; date = []
	for index in range(len(data["packettimestamp"])):
		year.append(int(data["packettimestamp"][index][0:4]))
		month.append(int(data["packettimestamp"][index][5:7]))
		date.append(int(data["packettimestamp"][index][8:10]))
	return date, month, year

def HoursMinutesSeconds(data):
	hours = [] ; minutes = [] ; seconds = []
	for index in range(len(data["packettimestamp"])):
		hours.append(data["packettimestamp"][index][11:13])
		minutes.append(data["packettimestamp"][index][14:16])
		seconds.append(data["packettimestamp"][index][17:-1])
	return hours, minutes, seconds		

