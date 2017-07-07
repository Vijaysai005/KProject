# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 11:24:11 2017

@author: Vijayasai S
"""

from mercator_projection import mercator_proj
import csv

filename = input("Enter the filename: ") #data1.csv, data2.csv, ...
with open(filename, "r") as csv_file:
    data_file = csv.reader(csv_file)
    X,Y = [],[]
    for row in data_file:
        x,y = mercator_proj(float(row[0]), float(row[1]))
        X.append(x)
        Y.append(y)
outfile = "xy.csv"
with open(outfile, "w") as csv_file:    
    for i in range(len(X)):
        csv_file.write(str(X[i]) + "," + str(Y[i]) + "\n")



