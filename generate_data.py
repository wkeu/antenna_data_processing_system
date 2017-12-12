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
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

###############################################################################
#
#   Functions for ploting
#
###############################################################################

#TODO: Title and legend
#Catisian plot of normalised test data
def plot_norm_cart(az_co,az_cr):
    #normalise 
    normalised_az = normalise(az_co,az_cr)
    
    #Get Freq list of column headers
    headers_az_co = list(az_co.dtypes.index)
    headers_az_cr = list(az_cr.dtypes.index)     
    
    #Create plot
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    ax1.plot(normalised_az)  
    
    
    #Set axis parameters
    ax1.grid()
    ax1.set_ylim([-40,0])
    ax1.set_xlim([0,360])
    x_tick_spacing = 20
    y_tick_spacing = 3
    ax1.xaxis.set_major_locator(ticker.MultipleLocator(x_tick_spacing))
    ax1.yaxis.set_major_locator(ticker.MultipleLocator(y_tick_spacing))
   
    #Set Plot title & axis titles
    ax1.set_title('P1 Azimuth')
    ax1.set_ylabel('dBi')
    ax1.set_xlabel('Angle')
   
    #Add legends
    legend1 = ax1.legend(headers_az_co,loc=('upper left'), bbox_to_anchor=(-0.13, 1.0),fancybox = True, framealpha=0.5,title='Co',prop={'size':10})
    legend2 = ax1.legend(headers_az_cr,loc=('upper right'), bbox_to_anchor=(1.1, 1.0),fancybox = True, framealpha=0.5,title='Cr',prop={'size':10})
    
    ax1.add_artist(legend1)
    ax1.add_artist(legend2)
    
    #Export Plot
    
    plt.savefig('P1 AZ Cartesian.png')
    
    
    
#TODO: Needs formating 
#Polar plot of normalised test data    
def plot_norm_polar(az_co,az_cr):
    #Normalise
    normalised_az = normalise(az_co,az_cr)
    
    #Get Freq list of column headers
    headers_az_co = list(az_co.dtypes.index)
    headers_az_cr = list(az_cr.dtypes.index)
   
    #isolate wave 
    angle_deg=np.arange(0,360,1)
    angle_rad=np.deg2rad(angle_deg)

    #Create plot
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111,projection='polar')
    ax2.plot(angle_rad, normalised_az)
    ax2.set_ylim([-40,0])
    legend1 = ax2.legend(headers_az_co,loc=('upper left'), bbox_to_anchor=(-0.2, 1.0),fancybox = True, framealpha=0.5,title='Co',prop={'size':10})
    legend2 = ax2.legend(headers_az_cr,loc=('upper right'), bbox_to_anchor=(1.2, 1.0),fancybox = True, framealpha=0.5,title='Cr',prop={'size':10})
    
    ax2.add_artist(legend1)
    ax2.add_artist(legend2)
    
###############################################################################
#
#   Results table
#
###############################################################################

def results_table(az_co,az_cr,el_co): 
    #Perform our calculations                                                          # Function to output results of calc to table
    xpol_at_sector = sector_xpol(az_co,az_cr)                                              # import function sector_xpol                     
    fbr = front_to_back(az_co)                                                          # import function front_to_back
    bw_3db = find_3db_bw(az_co)
    first_usl=find_first_usl(el_co)
    usl_range=find_usl_in_range(el_co)
    squint=find_squint(az_co)
    
    #Put into a dataframe
    results = pd.DataFrame()
    results = pd.concat([bw_3db,squint,xpol_at_sector,fbr,first_usl,usl_range],axis = 1)
    
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
port_s1=read_in_port_data()

# define dataframe pages
az_co = port_s1["az_co"]["amplitude"]
az_cr = port_s1["az_cross"]["amplitude"]
el_co = port_s1["el_co"]["amplitude"]

# convert pandas string values to float values
az_co = az_co.convert_objects(convert_numeric=True)
az_cr = az_cr.convert_objects(convert_numeric=True)
el_co = el_co.convert_objects(convert_numeric=True)

#Generate summary table for data    
Results = results_table(az_co,az_cr,el_co)  
#Save data to a CSV
Results.to_csv('P1 results.csv')

#Cart Plot
plot_norm_cart(az_co,az_cr)
plot_norm_polar(az_co,az_cr)


#writer = pd.ExcelWriter('output.xlsx')
#Results.to_excel(writer,'Sheet1')
#writer.save()

