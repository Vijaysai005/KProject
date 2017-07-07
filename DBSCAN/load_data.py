# /usr/bin/env python

import os
import csv

from os.path import dirname
from os.path import join
import numpy as np


class Bunch(dict):

    def __init__(self, **kwargs):
        dict.__init__(self, kwargs)

    def __setattr__(self, key, value):
        self[key] = value

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __getstate__(self):
        return self.__dict__

def load_files(filename, nrow, ncol):
	module_path = dirname(__file__)
	with open(join(module_path, filename)) as csv_file:
		data_file = csv.reader(csv_file)

		n_samples = int(nrow)
		n_features = int(ncol)

		data = np.empty((n_samples, n_features))

		for i, j in enumerate(data_file):
			data[i] = np.asarray(j[0:], dtype=np.float)
	return Bunch(data=data)

