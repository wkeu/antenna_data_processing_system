# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 10:37:37 2017

@author: matt.slevin
"""

"""
Before running this file. Make sure that you set the working directory to the 
working git repository. 
"""


###############################################################################
#
#   Import Data
#
###############################################################################


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

#Read in data 


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

#import custom scripts
from file_merge import * 
from formula import *

#import libs
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#import data
port_s1=read_in_port_data()

# define dataframe pages
az_co = port_s1["az_co"]["amplitude"]
az_cr = port_s1["az_cross"]["amplitude"]
el_co = port_s1["el_co"]["amplitude"]

# convert pandas string values to float values
co = az_co.convert_objects(convert_numeric=True)
cr = az_cr.convert_objects(convert_numeric=True)

az_peak=find_az_peak(co,cr)                                                          # import function find az_peaks

normalised_az = normalise(co,cr)                                                     # import function normalise
    
xpol_at_sector = sector_xpol(co,cr)                                                 # import function sector_xpol                     

fbr = front_to_back(co,cr)                                                          # import function front_to_back

#Calculate bw_3db

bw_3db = find_3db_bw(az_co)
###############################################################################
#
#   Plot normalised cartesian graph
#
###############################################################################


plt.plot(normalise(co,cr))


#plt.grid()
#plt.show()
#plt.savefig('P1 AZ.png')

###############################################################################
#
#   Results table
#
###############################################################################


def results_table(co,cr):                                                           # Function to output results of calc to table
    fbr = front_to_back(co,cr)
    sector_at_xpol = sector_xpol(co,cr)
    results = pd.DataFrame()
    results = pd.concat([front_to_back(co,cr),sector_xpol(co,cr)],axis = 1)
    return results

Results = results_table(co,cr)                                                      #assign variable Results to the reuslts table
Results.loc['Average'] = Results.mean()                                             #add row named average to table calulating average of each column
Results.loc['Max'] = Results.max()                                                  #add row named max to table calulating max of each column
Results.loc['Min'] = Results.min()                                                  #add row named min to table calulating min of each column


Results.to_csv('P1 results.csv')
#writer = pd.ExcelWriter('output.xlsx')
#Results.to_excel(writer,'Sheet1')
#writer.save()
















