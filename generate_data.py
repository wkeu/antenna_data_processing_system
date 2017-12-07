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

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# define dataframe pages
az_co = port_s1["az_co"]["amplitude"]
az_cr = port_s1["az_cross"]["amplitude"]
el_co = port_s1["el_co"]["amplitude"]

# convert pandas string values to float values
co = az_co.convert_objects(convert_numeric=True)
cr = az_cr.convert_objects(convert_numeric=True)


###############################################################################
#
#   Find Peak amplitude & angle
#
###############################################################################

az_peak_amp = co.max()                                                              # find peak valie in each column

az_peak_pos = co.idxmax()                                                           # find index no of peak value

az_peak = pd.concat([az_peak_amp,az_peak_pos], axis = 1)                            # join az_peak_amp & az peak_pos
az_peak.columns = ['amplitude','angle']


###############################################################################
#
#   Azimuth Cross Polar Discrimiation @ sector
#
###############################################################################
normalise_co = co - az_peak 
normalise_cr = cr - az_peak

###############################################################################
#
#   Front to back ratio 
#
###############################################################################
def front_to_Back_ratio():
    return fbr

sector = 180                                                                        # define sector angle

back_sight1 = sector - 180                                                          # define the backsight(back of antenna). eg 0 & 360 degrees
back_sight2 = sector + 180
fbr_range = 30                                                                      # define +/- range to check for FBR

fbr_search1 = back_sight1 + (fbr_range+1)                                           # this is search range 1 eg 0 - 30 degrees
fbr_search2 = back_sight2 - (fbr_range+1)                                           # this is search range 2 eg 30 - 360 degrees

fbr1, _, fbr2 = np.split(co,[fbr_search1,fbr_search2], axis = 0)                    # Split Co dataframe into 3 segements   

fbr_max = pd.concat([fbr1,fbr2], axis = 0)                                          # join fbr1 & fbr2

# Output#
fbr = az_peak_amp - fbr_max.max()                                                   # Find fbr = az peak - peak value in search range


###############################################################################
#
#   Plot normalised cartesian graph
#
###############################################################################

#plt.plot(normalise_co)
#plt.plot(normalise_cr)


#plt.grid()
#plt.show()





