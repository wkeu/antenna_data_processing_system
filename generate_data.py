# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 10:37:37 2017

@author: matt.slevin
"""

"""
Before running this file. Make sure that you set the working directory to the 
working git repository. 
"""

from file_merge import * 

###############################################################################
#
#   Import Data
#
###############################################################################

#Read in data 
port_s1=read_in_port_data()

"""
port_s1 now contains all port1 test data in the following format:

az_co
    -amp
    -phase
    
az_cross
    -amp
    -phase
    
el_co
    -amp
    -phase
    
"""

###############################################################################
#
#   Calculations
#
###############################################################################