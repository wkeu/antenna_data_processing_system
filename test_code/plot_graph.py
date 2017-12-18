# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 14:12:36 2017

@author: MJ.McAssey
"""

import numpy as np                                                               
import matplotlib.pyplot as plt                                                                                                                                 

fig = plt.figure()                                                               
ax = fig.add_subplot(1,1,1)                                                      

# major ticks every 20, minor ticks every 5                                      
major_ticks = np.arange(0, 101, 20)                                              
minor_ticks = np.arange(0, 101, 5)                                               

ax.set_xticks(major_ticks)                                                       
ax.set_xticks(minor_ticks, minor=True)                                           
ax.set_yticks(major_ticks)                                                       
ax.set_yticks(minor_ticks, minor=True)                                           

# and a corresponding grid                                                       

ax.grid(which='both')                                                            

# or if you want differnet settings for the grids:                               
ax.grid(which='minor', alpha=0.2)                                                
ax.grid(which='major', alpha=0.5)                                                

plt.show()