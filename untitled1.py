# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 12:37:53 2017

@author: MJ.McAssey
"""

from file_merge import * 
from formula import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

normalised_az = normalise(az_co,az_cr)
  
    
    #Create plot
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
ax1.plot(normalised_az)
ax1.grid()
ax1.set_title('P1 Azimuth')
ax1.set_ylabel('dBi')
ax1.set_xlabel('Angle')
legend = ax1.legend(loc='upper left',fancybox = True, framealpha=0.5)
frame = legend.get_frame()
frame.set_face_color('0.90')