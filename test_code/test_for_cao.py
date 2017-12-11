# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 09:43:45 2017

@author: matt.slevin
"""

from file_merge import * 
from formula import *
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from peakdetect import peakdetect
import pandas as pd

#TODO:  Create an interactive plot for defining the number of data points that we
#       use on our graph for each frequency to determine each of our side lobes. 
        
port_s1=read_in_port_data()
el_co = port_s1["el_co"]["amplitude"]

#Convert the data so that it is stored in a more appropriate format
el_co = el_co.convert_objects(convert_numeric=True)

#TODO: Loop for each wave.
#Isolate one wave

key_list=el_co.keys()

#Convert to numpy matrix
#def find_1st_usl()
j=0
for i in key_list:
    
    wave=el_co[i] 
    wave_np=wave.as_matrix()
    
    factor=100
    angle, amp = stretch_axis(np.arange(0, 360),wave_np,factor)

    #Smooth the signal, so that we can detect peaks easier. 
    amp_smooth=savgol_filter(amp, 75, 3)

    peaks, troughs = peakdetect(amp_smooth, lookahead=300)

    df_peaks = pd.DataFrame(data=peaks,columns=["angle","amp"])
    df_troughs = pd.DataFrame(data=troughs,columns=["angle","amp"])

    idx_max=df_peaks.idxmax()

    amp_of_peak=df_peaks["amp"][idx_max["amp"]]
    amp_of_1stlobe=df_peaks["amp"][idx_max["amp"]-1]

    first_usl=amp_of_peak-amp_of_1stlobe
    
    plt.figure(j)
    plt.title(i)
    
    for i in range(0, len(peaks) ):
        plt.plot(angle[peaks[i][0]],peaks[i][1],"ro")

    for i in range(0, len(troughs)):
        plt.plot(angle[troughs[i][0]],troughs[i][1],"mo")

    plt.plot(angle,amp_smooth,"c")
    
    j+=1
