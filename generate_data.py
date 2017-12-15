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
#   Import Libaries
#
###############################################################################

from file_merge import * 
from formula import *
from antenna_plots import *
import pandas as pd

###############################################################################
#
#   Results table
#
###############################################################################

def results_table(az_co,az_cr,el_co): 
    #Perform our calculations                                                          # Function to output results of calc to table
    xpol_at_sector = sector_xpol(az_co,az_cr)                                              # import function sector_xpol                     
    fbr = front_to_back(az_co)                                                          # import function front_to_back
    az_bw_3db = find_3db_bw(az_co,"Az Co 3db BW")
    el_bw_3db = find_3db_bw(el_co,"El Co 3db BW")
    first_usl=find_first_usl(el_co)
    usl_range=find_usl_in_range(el_co)
    squint=find_squint(az_co)
    
    #Put into a dataframe
    results = pd.DataFrame()
    results = pd.concat([az_bw_3db,el_bw_3db,squint,xpol_at_sector,fbr,first_usl,usl_range],axis = 1)
    
    #Add average min and max
    results.loc['Average'] = results.mean()                                             #add row named average to table calulating average of each column
    results.loc['Max'] = results.max()                                                  #add row named max to table calulating max of each column
    results.loc['Min'] = results.min()                                                  #add row named min to table calulating min of each column

    return results
                                                    #assign variable Results to the reuslts table

###############################################################################
#
#   Reading in data and doing calculations
#
###############################################################################

#import data
#Alternatively we can use sub dir=\\raw_data\\
all_ports=read_in_data_all_ports(    sub_dir = "\\raw_data_3\\"     )
port_s1=all_ports["P2"]

# define dataframe pages
az_co = port_s1["AZ T0 CO"]["amplitude"]
az_cr = port_s1["AZ T0 CR"]["amplitude"]
el_co = port_s1["EL T0 CO"]["amplitude"]

# convert pandas string values to float values
az_co = az_co.convert_objects(convert_numeric=True)
az_cr = az_cr.convert_objects(convert_numeric=True)
el_co = el_co.convert_objects(convert_numeric=True)

#Generate summary table for data    
results = results_table(az_co,az_cr,el_co)  
#Round down Results
results=results.round(2)
#Save data to a CSV
results.to_csv('P1_results.csv')

#Generate and Save Plots
#Cart
plot_norm_cart(az_co,az_cr,fname="P1 AZ Cart")
plot_norm_cart(el_co,el_co,fname="P1 EL Cart")
#Polar
plot_norm_polar(az_co,az_cr,fname="P1 AZ Polar")
plot_norm_polar(el_co,el_co,fname="P1 EL Polar")
