##############################################################
# Script to run test on generate_data (Full backend test)
##############################################################

from generate_data import Generate_data
from file_merge import read_in_data_all_ports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from antenna_plots import *

def rotate_all_ports(all_ports,rotate_angle=45):

    all_ports_rotated=all_ports.copy()
    
    #Port
    for port in all_ports:
        
        #Mesurment
        for measurement in all_ports[port]:
        
            #Rotate Panda
            pd_waves = all_ports[port][measurement]["amplitude"]
            pd_waves_rotated=rotate_panda(pd_waves, rotate_angle)
            all_ports_rotated[port][measurement]["amplitude"]=pd_waves_rotated
    
    return all_ports_rotated

    
def rotate_panda(pd_waves, rotate_angle):
    
    #Transpose to make easier to dice and splice
    
    a=pd_waves[0:rotate_angle]
    b=pd_waves[rotate_angle:len(pd_waves)]
    
    frames=[b,a]
    result = pd.concat(frames)
    result = result.reset_index()
    result = result.drop(['index'], axis=1)
    
    return result

source_dirA="C:/Users/Matt Slevin/Documents/GitHub/antenna_data_processing_system/antenna_raw_data/sector_data/IR468_V2_test"
source_dirB="C:/Users/Matt Slevin/Documents/GitHub/antenna_data_processing_system/antenna_raw_data/sector_data/AW3014"
save_path= "C:/Users/Matt Slevin/Documents/GitHub/antenna_data_processing_system/"

all_ports=read_in_data_all_ports(    source_dirA + "/"    )

control = all_ports["P11"]["AZ T0 CO"]["amplitude"]
plot_norm_cart_interacive_el(control, "control", save_path)

rotate_angle= 45 #degrees, note ensure that this is a postivie angle 
                 #this angle rotates back
                 
all_ports_rotated = rotate_all_ports(all_ports,rotate_angle) #Always rotating to the left

test = all_ports_rotated["P11"]["AZ T0 CO"]["amplitude"]
plot_norm_cart_interacive_el(test, "test_rotated", save_path)

