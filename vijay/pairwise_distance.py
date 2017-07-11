# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 12:53:37 2017

@author: Vijayasai S
"""

def pairwise_dist(a):
    output = []
    j = 0
    for i in range(len(a)):
        out = []
        if j != len(a):
            while (a[i] != a[j]) or (a[i] == a[j]):
                if (a[i] == a[j]) and i < len(a) - 1:
                    j += 1
                out.append(abs(a[i] - a[j]))
                j +=1 
                if j == len(a):
                    j = 0
                    break
            output.append(out)
    output[-1].pop(-1)
    return output
    
    
a = [3,8,5,7,9,14,15]
out = pairwise_dist(a)

max_array = []
for i in range(len(out)):
    max_array.append(max(out[i]))

print ("Maximum pairwise distance: ", max(max_array))
    
