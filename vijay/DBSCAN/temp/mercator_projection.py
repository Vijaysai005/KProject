# usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 10:10:35 2017

@author: Vijayasai S
"""

"""
mercator_proj is a function which converts latitude and longitude 
to x and y coordinate system.
lat and long should be mentioned in degrees
"""

import numpy as np

def mercator_proj(lat, long):
    radius = 6371.0 # mean radius of the earth (in KM)
    long_0 = 0 # central meridian (Greenwich with longitude zero degree)
    X = (radius * (long - long_0) * np.pi) / 180.0
    Y = radius * np.log(np.tan(np.radians(45 + (lat * 0.5))))
    return X, Y
    
def reverse_mercator_proj(X, Y):
    radius = 6371.0 # mean radius of the earth (in KM)
    long_0 = 0 # central meridian (Greenwich with longitude zero degree)
    long = np.degrees(long_0 + (X/radius))
    lat = np.degrees(2 * np.arctan(np.exp(Y/radius))) - 90
    return lat, long
    
# X, Y = mercator_proj(-23.53,74.85)
# lat, long = reverse_mercator_proj(X, Y)    
    
    

