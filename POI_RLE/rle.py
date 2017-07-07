# usr/bin/env python

"""
Created on Fri Jun 30
@author : Vijayasai S
"""

from itertools import groupby

def RunLengthEncoding(input_string):
		return [(len(list(j)), i) for i,j in groupby(input_string)]


# input string should consist the value of 0 and 1
def FindIndex(input_string):
	
	rle = RunLengthEncoding(input_string)
	stayTimeIndex = [] ; currentLength = []
	runIndex = 0
	for i in range(len(rle)):
		if rle[i][1] == "0" or rle[i][1] == "1":
			if rle[0][1] == "0":
				currentLength.append(runIndex + 1)
				runIndex = runIndex + rle[i][0]
		if rle[i][1] == "0" or rle[i][1] == "1":
			if rle[0][1] == "1":
				currentLength.append(runIndex + rle[i][0])
				runIndex = runIndex + rle[i][0]
		if i % 2 != 0:
			if rle[0][1] == "1":
				currentLength[0] = currentLength[0] 
				currentLength[1] = currentLength[1]
			if rle[0][1] == "0":
				currentLength[0] = currentLength[0] - 1
				currentLength[1] = currentLength[1] - 1

			stayTimeIndex.append(currentLength)
			currentLength = []
	if rle[-1][1] == "0":
		stayTimeIndex.pop(-1)
	return stayTimeIndex

# input_list = [1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, \
# 	1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1]
# input_string = ''.join(str(i) for i in input_list)
# index = FindIndex(input_string)
# print index