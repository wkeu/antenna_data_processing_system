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

co = az_co
cr = az_cr
###############################################################################
#
#   Azimuth Co Pol 3dB beamwidth
#
###############################################################################

az_peak = co.max()                               # find peak valie in each column

az_peak_pos = co.idxmax()                        # find index no of peak value

value = az_peak - 3

###############################################################################
#
#   Azimuth Cross Polar Discrimiation @ sector
#
###############################################################################
sector = 180 # define sector as 180

xpol_at_sector = co.iloc[sector] - cr.iloc[sector] # co at sector - cr at sector


###############################################################################
#
#   normalise co & cr together
#
###############################################################################
normalise_co = co - az_peak 
normalise_cr = cr - az_peak


###############################################################################
#
#   Plot normalised cartesian graph
#
###############################################################################

plt.plot(normalise_co)
plt.plot(normalise_cr)



plt.grid()
plt.show()
