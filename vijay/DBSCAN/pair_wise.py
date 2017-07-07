#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 13:15:05 2017

@author: kpit
"""
#closets poits
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv
from math import radians

from mercator_projection import mercator_proj

def distance(pt_1, pt_2):
    pt_1 = np.array((pt_1[0], pt_1[1]))
    pt_2 = np.array((pt_2[0], pt_2[1]))
    return np.linalg.norm(pt_1-pt_2)

def closest_node(node, nodes):
    pt = []
    dist = 0
    for n in nodes:
        if distance(node, n) > dist:
            dist = distance(node, n)
            pt = n
    return pt

with open('latitude.csv') as f:
    data_1 = list(csv.reader(f))
shape =np.shape(data_1) 
size = np.size(data_1[:])# total number of element in the matrix
cols = shape[1]
rows = shape[0]
print("number of cols=",cols)
print("number of rows=",rows)
data = [[float(data_1[i][0]),float(data_1[i][1])] for i in range(0,rows)]
#data = [[2,4],[2,4],[2,4],[2,4],[3,1000]]

data2 = []
for i in range(rows):
    X,Y = mercator_proj(data[i][0],data[i][1])# X,Y coordinates of lat-long data points(in KM)
    data2.append([X,Y])
print (np.shape(data2))
a = []# array of tuple
for x in range(len(data2)):
    a.append((data2[x][0],data2[x][1]))
print("the coordinates of lat-long")
#rint(a)
Pairwise_D=[]# pairwise distance from all the poits in the array
for p in a:
    #print("the closest point =",tcp)
    Pairwise_D.append([distance(p,a[i]) for i in range(len(a))])
#print(Pairwise_D)
l= len(Pairwise_D)
max_val =[np.max(Pairwise_D[i]) for i in range(l)]# the max vlaue from the pairwise_D
max_ind = [np.argmax(Pairwise_D[i]) for i in range(l)]
print("array of max value in the distance list",max_val)
print("array of index of max values",max_ind)
tcp = closest_node(a[0], a)
print("the farthest point to ",a[0],"is =", tcp)
