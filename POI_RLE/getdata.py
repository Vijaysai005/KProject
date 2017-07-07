# usr/bin/env python

"""
Created on Fri Jun 23
@author : Vijayasai S
"""
import csv
from createdictionary import HeaderName

def GetData(dict,filename):
	title = HeaderName(filename)
	with open(filename, "r") as doc:
		readerFile = csv.reader(doc, delimiter=',', quotechar=" ")
		index = 0
		for row in readerFile:
			index += 1
			if index == 1:
				continue
			else:
				for col in range(len(title)):
					dict[title[col]].append((row[col])) 
	return dict
