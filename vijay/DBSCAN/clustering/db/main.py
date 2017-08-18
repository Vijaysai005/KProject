# usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 13:15:05 2017

@author: Vijayasai S
"""
# Use python3

import my_dbscan as mydb
import alert_update as au
import generate_data as gd

from pymongo import MongoClient
import pandas as pd

def _connect_mongo(host, port, username, password, db):
    """ A util for making a connection to mongo """

    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)

    return conn[db]


def read_mongo(db, collection, query={}, host='localhost', port=27017, username=None, password=None, no_id=True):
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    db = _connect_mongo(host=host, port=port, username=username, password=password, db=db)

    # Make a query to the specific DB and Collection
    cursor = db[collection].find(query)

    # Expand the cursor and construct the DataFrame
    df =  pd.DataFrame(list(cursor))

    # Delete the _id
    if no_id:
        del df['_id']

    return df

if __name__  == "__main__":

    client = MongoClient('localhost', 27017)
    db = client.maximus_db

    ##########################################################################
    # COLLECTING DATA FROM DATABASE  										 #
    ##########################################################################
    
    get_coll = db.device_data
    set_coll1 = db.tapola_rank_15_curr
    set_coll2 = db.tapola_rank_15_total

    time_delay = 15 # in minutes

    year = 2017 ; month = 3        # year = datetime.now().year		month = datetime.now().month
			    
    startday = 25 ; endday = 26	   # startday = datetime.now().day  endday =    
    starthr = 0 ; endhr = 23	   # starthr = datetime.now().hour
    startmin = 0 ; endmin = 59
    
    gd.Generate_data(get_coll, set_coll1, set_coll2, time_delay, year, month, startday, endday, starthr, endhr, startmin, endmin)         
