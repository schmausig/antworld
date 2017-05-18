#!/usr/bin/env python3

import os
import itertools

__all__= [	'get_file_dir'		, 'get_uis_dir', 
				'get_worlds_dir'	]

def get_file_dir():

	return os.path.dirname(os.path.realpath(__file__))+os.sep
 
def get_uis_dir():

	return get_file_dir()+"uis"+os.sep

def get_worlds_dir():

	return get_file_dir()+"worlds"+os.sep


