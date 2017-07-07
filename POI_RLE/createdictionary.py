# usr/bin/env python

"""
Created on Fri Jun 23
@author : Vijayasai S
"""

import csv
import os

def CreateDirectory(filepath):
	directory = os.path.dirname(filepath)
	if not os.path.exists(directory):
		os.makedirs(directory) 
	return

def HeaderName(filename):
	title = []
	with open(filename,"r") as doc:
		readerFile = csv.reader(doc, delimiter=',')
		index = 0
		for row in readerFile:
			index += 1
			if index == 1:
				title = row
			else:
				break
	return title

def CreateDictionary(filename):
	dict = {}
	title = HeaderName(filename)
	for index in range(len(title)):
		dict[title[index]] = []
	return dict
