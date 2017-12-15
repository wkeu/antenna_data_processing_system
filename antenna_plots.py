# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 09:46:34 2017

@author: matt.slevin
"""

from formula import *
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

###############################################################################
#
#   Functions for ploting
#
###############################################################################

#Cartisian plot of normalised test data
def plot_norm_cart(az_co,az_cr,fname):
    
    #Turn off plot so that it only saves it and dosnt show it
    plt.ioff() 
    
    #normalise 
    normalised_az = normalise(az_co,az_cr)
    
    #Get Freq list of column headers
    headers_az_co = list(az_co.dtypes.index)
    
    #Create plot
    fig1 = plt.figure(figsize=[13,7])
    ax1 = fig1.add_subplot(111)
    ax1.plot(normalised_az,linewidth=0.75,alpha=0.5)  
    
    #Set axis parameters
    ax1.grid(alpha=0.25)
    ax1.set_ylim([-40,0.5])
    ax1.set_xlim([0,360])
    x_tick_spacing = 20
    y_tick_spacing = 3
    ax1.xaxis.set_major_locator(ticker.MultipleLocator(x_tick_spacing))
    ax1.yaxis.set_major_locator(ticker.MultipleLocator(y_tick_spacing))
   
    #Set Plot title & axis titles
    ax1.set_title(fname)
    ax1.set_ylabel('dBi')
    ax1.set_xlabel('Angle')
   
    #Add legends
<<<<<<< HEAD
    legend1 = ax1.legend(headers_az_co,fancybox = True, bbox_to_anchor=(1.05, 1),framealpha=0.75,title='freq',prop={'size':10})
=======
    legend1 = ax1.legend(headers_az_co,fancybox = True, framealpha=0.5,title='freq',prop={'size':10})
>>>>>>> fbd7d9fb656c2d68a2ff0af724d42de6ad8116b2
 
    ax1.add_artist(legend1)

    #Export Plot
    plt.savefig(fname+'.png', dpi=600)  
    plt.ion() 
    
#Polar plot of normalised test data    
def plot_norm_polar(az_co,az_cr,fname):
    
    plt.ioff()
    #Normalise
    normalised_az = normalise(az_co,az_cr)

    #Add roll around
    normalised_az=pd.concat([normalised_az,normalised_az.loc[[0]]])
    
    #Get Freq list of column headers
    headers_az_co = list(az_co.dtypes.index)

    #isolate wave 
    angle_deg=np.arange(0,361,1)
    angle_rad=np.deg2rad(angle_deg)

    #Create plot
    fig2 = plt.figure(figsize=[13,7])
    ax2 = fig2.add_subplot(111,projection='polar')
    ax2.set_title(fname)
    ax2.plot(angle_rad, normalised_az,linewidth=0.75,alpha=0.5)
    ax2.grid(alpha=0.25) #Set transparency of grid to 25%
    ax2.set_ylim([-40,0])
<<<<<<< HEAD
    legend1 = ax2.legend(headers_az_co, bbox_to_anchor=(-0.1, 0.9),fancybox = True, framealpha=0.75,title='freq',prop={'size':10})
=======
    legend1 = ax2.legend(headers_az_co, bbox_to_anchor=(-0.1, 0.9),fancybox = True, framealpha=0.5,title='freq',prop={'size':10})
>>>>>>> fbd7d9fb656c2d68a2ff0af724d42de6ad8116b2

    ax2.add_artist(legend1)

    plt.savefig(fname+'.png', dpi=600) 
    plt.ion() 
    