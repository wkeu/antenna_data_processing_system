# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 09:46:34 2017

@author: matt.slevin
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd 
from antennas import *

###############################################################################
#
#   Functions for ploting
#
###############################################################################

###############################################################################
#
# Normal PNG plots
#
###############################################################################

#Cartisian plot of normalised test data
def plot_norm_cart(az_co,az_cr,fname,save_dir):
    
    az_co = az_co.convert_objects(convert_numeric=True)
    az_cr = az_cr.convert_objects(convert_numeric=True)
    
    #Turn off plot so that it only saves it and dosnt show it
    plt.ioff() 
    
    #normalise 
    normalised_az = Sector.normalise("",az_co,az_cr)
    
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
    ax1.set_title('P2 Azimuth')

    ax1.set_title(fname)

    ax1.set_ylabel('dBi')
    ax1.set_xlabel('Angle')
   
    #Add legends
    legend1 = ax1.legend(headers_az_co,fancybox = True, loc=1, bbox_to_anchor=(1.1, 1.05),framealpha=0.75,title='freq',prop={'size':10})
    ax1.add_artist(legend1)

    #Export Plot
    plt.savefig(save_dir+fname+'.png', dpi=300)     
    plt.close('all')  
    plt.ion() 
    
#Polar plot of normalised test data    
def plot_norm_polar(az_co,az_cr,fname,save_dir):
    
    az_co = az_co.convert_objects(convert_numeric=True)
    az_cr = az_cr.convert_objects(convert_numeric=True)
    
    plt.ioff()
    #Normalise
    normalised_az = Sector.normalise("",az_co,az_cr)

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
    legend1 = ax2.legend(headers_az_co, bbox_to_anchor=(-0.1, 0.9),fancybox = True, framealpha=0.5,title='freq',prop={'size':10})


    ax2.add_artist(legend1)

    plt.savefig(save_dir+fname+'.png', dpi=300) 
    plt.close('all')
    plt.ion() 

###############################################################################
#
# Interactive Plots
#
###############################################################################

import mpld3
from mpld3 import plugins
    
def plot_norm_cart_interacive_el(el_co, fname, save_dir):

    plt.ioff()

    #normalise
    el_co = el_co.convert_objects(convert_numeric=True)

    normalised_el_co,_ = Sector.normalise2("",el_co, el_co)

    #Get Freq list of column headers
    headers_el_co = list(el_co.dtypes.index)

    #Create plot
    fig, ax = plt.subplots(figsize=(12,7))
    fig.subplots_adjust(right=.8)
    labels = headers_el_co

    line_collections = ax.plot(normalised_el_co, lw=1.5, alpha=0.9)
    interactive_legend = plugins.InteractiveLegendPlugin(line_collections, labels, alpha_unsel=0.1, alpha_over=1.5, start_visible=False)
    plugins.connect(fig, interactive_legend)


    ###########################################################################
    # Figure Settings

    #Set axis parameters
    ax.grid(alpha=0.25)
    ax.set_ylim([-40,0.5])
    ax.set_xlim([0,360])
    x_tick_spacing = 20
    y_tick_spacing = 3
    ax.xaxis.set_major_locator(ticker.MultipleLocator(x_tick_spacing))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(y_tick_spacing))
    
    #Set Plot title & axis titles

    ax.set_ylabel('dBi')
    ax.set_xlabel('Angle')

    ax.set_ylim([-40,0.5])
    ax.set_xlim([0,360])
    
    ax.set_title(fname)
    
    #Save the figure as a html 
    mpld3.save_html(fig,save_dir+fname+".html")
    
    plt.close('all')
    plt.ion() 

    
def plot_norm_cart_interacive_az(az_co,az_cr,fname,save_dir):
    
    plt.ioff()
    
    #Defining a list of colors
    colours=list( ["blue", "green", "red", "cyan", "magenta",
             "yellow", "black", "tan", "firebrick",
             "plum", "aqua", "darkblue", "crimson", "pink",
             "chocolate", "darkgrey", "blue", "green", "red",
             "cyan", "magenta", "yellow", "black", "tan", 
             "firebrick", "plum", "aqua", "darkblue",
             "crimson", "pink", "chocolate", "darkgrey" ]  )

    #Convert data so that we can use it
    az_co = az_co.convert_objects(convert_numeric=True)
    az_cr = az_cr.convert_objects(convert_numeric=True)
    
    az_co,az_cr = Sector.normalise2("",az_co,az_cr)
    
    #X axis
    x1 = np.arange(0, 360, 1)
    
    #List of all frequencies
    key_list=list(az_co.keys())
    
    
    fig, ax = plt.subplots(figsize=(12,7))
    fig.subplots_adjust(right=.8)
    
    #List of all lines
    ln=list()
    
    #Loop plotting both the co and cross for each frequency
    for i in range(len(key_list)):
    
        co = az_co[key_list[i]]  
        cr = az_cr[key_list[i]]
        
        y1 = np.array([ co.as_matrix() ,  cr.as_matrix() ])
        
        ln.append(ax.plot(x1,
                     y1.T, 
                     lw=1.6, 
                     alpha=0.9,
                     label=key_list[i]))
                     #,c=colours[i]))
        
    #Link up interactive legend
    plugins.connect(fig, plugins.InteractiveLegendPlugin(ln, key_list, alpha_unsel=0.05, alpha_over=1.5, start_visible=False))
    
    ###########################################################################
    # Figure Settings
    
    #Set axis parameters
    ax.grid(alpha=0.25)
    ax.set_ylim([-40,0.5])
    ax.set_xlim([0,360])
    x_tick_spacing = 20
    y_tick_spacing = 3
    ax.xaxis.set_major_locator(ticker.MultipleLocator(x_tick_spacing))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(y_tick_spacing))
        
    #Set Plot title & axis titles
    ax.set_ylabel('dBi')
    ax.set_xlabel('Angle')
    
    ax.set_ylim([-40,0.5])
    ax.set_xlim([0,360])
        
    #ax.set_title(fname)
    ax.set_title(fname)
    
    #Save the figure as a html 
    mpld3.save_html(fig,save_dir+fname+".html")
    
    plt.close('all')
    plt.ion() 
    
