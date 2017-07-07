# usr/bin/env python

"""
Created on Fri Jun 23
@author : Vijayasai S
"""

from createdictionary import CreateDictionary
from getdata import GetData
from poi import POI

if __name__ == "__main__":
	filename = raw_input("Enter the filename: ") 
	time = float(raw_input("Enter the limit-time for the pitstops: "))	
		
	dict = CreateDictionary(filename)
	data = GetData(dict,filename)	
	POI(time, data)
