# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 09:21:40 2017

@author: matt.slevin
"""

import numpy as np
import pandas as pd
from scipy.signal import savgol_filter
from peakdetect import peakdetect
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
def front_to_back(co):
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

#Function to find the index of the nearest value in an array
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
def find_3db_bw(az_co, measurement_type="3db Beamwidth"):
    
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
    
    #Format into a data frame
    bw_3db_pd=pd.DataFrame({measurement_type:bw_3db,"index":key_list})
    bw_3db_pd=bw_3db_pd.set_index('index') 
            
    return bw_3db_pd
        
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
    
    sqt_pd=pd.DataFrame({"Squint":sqt,"index":key_list})
    sqt_pd=sqt_pd.set_index('index') 
    return sqt_pd
    

#function to calculate squint. Inputs are 3db intersection points
def cal_squint(r_int,l_int):
    midpoint=(r_int+l_int)/2.0
    boresight=180.0 #this is our ideal value 
    squint=midpoint-boresight
    return squint

###############################################################################
#
# Calculate first USL 
#
###############################################################################

#Function to find the peaks of a wave
def find_peaks(wave,factor=100):

    #Convert to numpy matrix with dtype float
    wave_np=np.asarray(wave,dtype='float64')

    #Stretch the Axis
    angle, amp = stretch_axis(np.arange(0, 360),wave_np,factor)

    #Smooth the signal 
    amp_smooth=savgol_filter(amp, 75, 3)

    #Find the peaks and troughs in wave
    peaks, troughs = peakdetect(amp_smooth, lookahead=300)

    #Put into dataframe
    df_peaks = pd.DataFrame(data=peaks,columns=["angle","amp"])

    #Convert index into angle
    df_peaks.angle=df_peaks.angle/factor

    return df_peaks

#Calulate the 1st USL for a given frequency
def cal_first_usl(wave):
   
    #Find the peaks and troughs
    df_peaks = find_peaks(wave)

    #Find index of peak
    idx_max=df_peaks.idxmax()

    #find amp of peak and 1st usl 
    amp_of_peak=df_peaks["amp"][idx_max["amp"]]
    amp_of_1stlobe=df_peaks["amp"][idx_max["amp"]-1]
    first_usl=amp_of_peak-amp_of_1stlobe
    
    return first_usl


#Calulate the 1st USL for a table
def find_first_usl(el_co):
    #Convert the data so that it is stored in a more appropriate format
    el_co = el_co.convert_objects(convert_numeric=True)    
    
    #Take column index into array 
    key_list=el_co.keys()
    first_usl=list()

    for i in key_list:
        #Add usl to list for given column
        first_usl.append(cal_first_usl(el_co[i]))
        
    #Format to panda
    first_usl_pd=pd.DataFrame({"1st USL":first_usl,"index":key_list})
    first_usl_pd=first_usl_pd.set_index('index')   
        
    return first_usl_pd

###############################################################################
#
#   USL in Range
#
###############################################################################

#TODO:   Add support for wrap around. (ie if we go into a ngative number) the
#        problem arises if we have a peak that is not centred at around 180 
#        degrees
    
#Finds the difference in amplitude between largest side lobe and peaks over a 
#certain frequency range. By default 180 degrees away from the peak. 
def calc_usl_in_range(wave,angle_range=180):
    
    #Find the peaks and troughs
    df_peaks = find_peaks( wave )
    
    #find peak amp,angle and index
    _,peak_amp=df_peaks.max()
    _,peak_idx=df_peaks.idxmax()
    peak_angle=df_peaks["angle"][peak_idx]
    
    #Remove all values not in range 
    df_peaks = df_peaks[(df_peaks.angle < peak_angle) & (df_peaks.angle > peak_angle-angle_range)  ]
    
    #find the peak of largest side lobe in range
    _,peak_sl_amp=df_peaks.max()
    
    #difference in amp
    usl=peak_amp-peak_sl_amp

    if usl<0:
        print("Warning: Check USL Value")
    
    #TODO: Make this a bit more sophisticated. Its a bit hacky
    if np.isnan(usl):
        print("failed to find usl in range")
        
        peak_lobe_itx = peak_angle-angle_range
        print(peak_lobe_itx)
        usl=peak_amp-wave[int(peak_lobe_itx)]
        print (usl) 
    
    return usl

#Calulate the USL for a table with a given angle range
def find_usl_in_range(el_co,angle_range=180):

    #Convert the data so that it is stored in a more appropriate format
    el_co = el_co.convert_objects(convert_numeric=True)    
    
    #Take column index into array 
    key_list=el_co.keys()
    usl_in_range=list()

    for i in key_list:
        #Add usl to list for given column
        usl_in_range.append(    calc_usl_in_range(el_co[i],angle_range)     )
    
    #Format into a dataframe
    usl_pd=pd.DataFrame({"USL in Range":usl_in_range,"index":key_list})
    usl_pd=usl_pd.set_index('index')
        
    return usl_pd    

