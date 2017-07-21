# usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 13:15:05 2017

@author: Vijayasai S
"""
# Use python3

import pymongo
from pymongo import MongoClient
import pprint

client = MongoClient('localhost', 27017)
db = client.maximus_db
dict = db.device_data

data = []
for dict in dict.find({},{"unit_id":1,"latitude":1,"longitude":1,"_id":0}).limit(100):
	data.append(dict)

print (data)
