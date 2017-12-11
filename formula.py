# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 09:21:40 2017

@author: matt.slevin
"""

import numpy as np
import pandas as pd

###############################################################################
#
#   Find Peak amplitude & angle
#
###############################################################################
def find_az_peak(co,cr):                                                                      # Function to find peak of azimuth
    az_peak_amp = co.max()                                                              # find peak valie in each column
    az_peak_pos = co.idxmax()                                                           # find index no of peak value
    az_peak = pd.concat([az_peak_amp,az_peak_pos], axis = 1)                            # join az_peak_amp & az peak_pos
    az_peak = pd.concat([az_peak_amp,az_peak_pos], axis = 1)                            # join az_peak_amp & az peak_pos
    az_peak.columns = ['amplitude','angle']
    return az_peak

###############################################################################
#
#   normalise co & cr together
#
###############################################################################
def normalise(co,cr):
    az_peak_amp = co.max()      
    normalise_co = co - az_peak_amp
    normalise_cr = cr - az_peak_amp
    normalised_az = pd.concat([normalise_co,normalise_cr], axis = 1)
    return normalised_az

###############################################################################
#
#   Azimuth Cross Polar Discrimiation @ sector
#
###############################################################################
def sector_xpol(co,cr):
    sector = 180 # define sector as 180
    xpol_at_sector = co.iloc[sector] - cr.iloc[sector] # co at sector - cr at sector
    xpol_at_sector = xpol_at_sector.to_frame()
    xpol_at_sector.columns = ['X Pol at sector']
    return xpol_at_sector

###############################################################################
#
#   Front to back ratio 
#
###############################################################################
def front_to_back(co,cr):
    sector = 180                                                                        # define sector angle
    back_sight1 = sector - 180                                                          # define the backsight(back of antenna). eg 0 & 360 degrees
    back_sight2 = sector + 180
    fbr_range = 30                                                                      # define +/- range to check for FBR

    fbr_search1 = back_sight1 + (fbr_range+1)                                           # this is search range 1 eg 0 - 30 degrees
    fbr_search2 = back_sight2 - (fbr_range+1)                                           # this is search range 2 eg 30 - 360 degrees

    fbr1, _, fbr2 = np.split(co,[fbr_search1,fbr_search2], axis = 0)                    # Split Co dataframe into 3 segements   

    fbr_max = pd.concat([fbr1,fbr2], axis = 0)                                          # join fbr1 & fbr2

    # Output#
    az_peak_amp = co.max()      
    fbr = az_peak_amp - fbr_max.max()                                                   # Find fbr = az peak - peak value in search range
    fbr = fbr.to_frame()
    fbr.columns = ['Front to Back Ratio']
    return fbr

###############################################################################
#
#   3db beamwidth calculations
#
###############################################################################

#TODO: aDD COMMENT
def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return idx

#"Stretch" the axis to have xfactor more datapoints
def stretch_axis(x,y,factor):
    #create a new angle axis with smaller increment size
    x_strch = np.linspace(0, len(x)-len(x)/(len(x)*factor), factor*len(x))

    #interpolate ("stretch") the y_axis to match x_axis. 
    y_strch = np.interp(x_strch, x, y)
    return x_strch, y_strch

def find_3db_intersection(wave):
    a=0
    b=0
    return a,b

#TODO: Make into a function that will find the 3db beamwidth for all frequencies

#TODO: Add support for detecting the number of peaks. (For case when we have 
#       A twin-peak in amp plot). This a unique feature and thus a low priority


#Function to find the 3db intersection points of a wave
def find_3db_intersection_angles(wave_str):
    
    #Convert into correct format
    wave = wave_str.convert_objects(convert_numeric=True)

    #Find the peak of the wave
    peak_amp=wave.max()
    peak_angle=wave.idxmax()

    #Interpolate both axis 
    factor=100
    angle,amp = stretch_axis(np.arange(0,360),wave.as_matrix(),factor)

    #section into left and right
    peak_idx=find_nearest(angle,peak_angle)
    wave_left=amp[0:peak_idx]
    wave_right=amp[peak_idx:len(angle)-1]

    #Find left and right intersection
    left_intxn=find_nearest(wave_left,peak_amp-3)
    right_intxn=find_nearest(wave_right,peak_amp-3) +len(wave_left)
        
    return angle[left_intxn], angle[right_intxn]


#Function to find the 3db beamwidths for a given graph
def find_3db_bw(az_co):
    
    #Collect keys    
    key_list=az_co.keys()
    #Initalise list
    bw_3db=list()

    #Cycle through each frequency column
    for i in key_list:
        #Work with each column individually 
        lowwer_angle, upper_angle =find_3db_intersection_angles(az_co[i])
        #Calculate 3db bw
        bw_3db.append( np.abs(lowwer_angle-upper_angle) )
        
            
    return bw_3db
        
###############################################################################
#
#   Squint calculation 
#
###############################################################################

def find_squint(az_co):
    #Collect keys
    key_list=az_co.keys()
    #Initalise list
    sqt=list()
    
    #Cycle through each frequency column
    for i in key_list:
        #Work with each column individually 
        lowwer_angle, upper_angle =find_3db_intersection_angles(az_co[i])
        #Culculate squint
        x = cal_squint(lowwer_angle,upper_angle)
        sqt.append( x )
        
    return sqt
    

#function to calculate squint. Inputs are 3db intersection points
def cal_squint(r_int,l_int):
    midpoint=(r_int+l_int)/2.0
    boresight=180.0 #this is our ideal value 
    squint=midpoint-boresight
    return squint