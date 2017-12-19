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
import os
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

###############################################################################
#
#   Results table
#
###############################################################################
#Results table for azimuth measurments
def results_table_az(az_co,az_cr):
    
    #Convert to usable format
    az_co = az_co.convert_objects(convert_numeric=True)
    az_cr = az_cr.convert_objects(convert_numeric=True)
    
    #Calculate
    xpol_at_sector = sector_xpol(az_co,az_cr)                                              # import function sector_xpol                     
    fbr = front_to_back(az_co)                                                          # import function front_to_back
    az_bw_3db = find_3db_bw(az_co,"Az Co 3db BW")
    squint=find_squint(az_co)
    
    #Put into a dataframe
    results = pd.DataFrame()
    results = pd.concat([az_bw_3db,squint,xpol_at_sector,fbr],axis = 1)
    
    return results

#Results table for elevation measurments
#TODO: Add tilt devation 
def results_table_el(el_co,fname="EL TX"):

    el_co = el_co.convert_objects(convert_numeric=True)
    
    el_bw_3db = find_3db_bw(el_co,"3db BW "+fname)
    first_usl= find_first_usl(el_co,"first_usl "+fname)
    usl_range= find_usl_in_range(el_co,measurement_type="usl_range "+fname)
    peak_dev = peak_tilt_dev(el_co,fname)
    tilt_dev = find_tilt_dev(el_co,fname)    
    
    #Put into a dataframe
    results = pd.DataFrame()
    results = pd.concat([el_bw_3db,first_usl,usl_range,peak_dev,tilt_dev],axis = 1)
    
    return results


#Merge AZ and EL into one results table. And final formatting
def results_final(az_results_table,el_results_table,port_name,save_dir): 
    
    #Merge Tables
    final_results_table=pd.concat([az_results_table,el_results_table],axis=1)
    
    #Add average min and max
    final_results_table.loc['Average'] = final_results_table.mean()                                             #add row named average to table calulating average of each column
    final_results_table.loc['Max'] = final_results_table.max()                                                  #add row named max to table calulating max of each column
    final_results_table.loc['Min'] = final_results_table.min()                                                  #add row named min to table calulating min of each column
    
    #Round all the values to 2 significant figures
    final_results_table=final_results_table.round(2)
    
    #Save to a file
    final_results_table.to_csv( save_dir + port_name+" results.csv" )                                                    # Function to output results of calc to table
    
    return final_results_table


###############################################################################
#
#   Function which will generate results table for a given port 
#
###############################################################################

#Function to do calculations based on the port and tilts. It generates all 
#tables for az calculations and then el calculations. It the merges and returns 
#results table.     
def calulated_based_per_port(P1,port_name,save_dir):
    
    P1=dict(P1) #Keep this! Ensures a copy was made.
    
    ###############################################################################
    # Azimuth (Calculations and Plots)
    ############################################################################### 
    
    #Do Azimuth Calculations first, removing them from P1 in the process
    az_co=P1.pop("AZ T0 CO")
    az_cr=P1.pop("AZ T0 CR")
    
    az_co=az_co["amplitude"]
    az_cr=az_cr["amplitude"]
    
    #Generates r esults table
    az_results_table=results_table_az(az_co,az_cr)
    
    #Plots
    plot_norm_cart(  az_co,az_cr  ,  fname=port_name +" AZ Cart", save_dir=save_dir)
    plot_norm_polar(  az_co,az_cr  , fname=port_name+" AZ Polar", save_dir=save_dir )
    
    ###############################################################################
    # Elevation (Calculations and Plots) 
    ###############################################################################
    
    #list to store tables    
    list_of_rt=list()
    
    #Generate plots and results per el_co file
    for file in P1:
        #Isolate the file
        el_co= P1[file]["amplitude"]
        list_of_rt.append(results_table_el(el_co,file))
        
        #Plots
        plot_norm_cart(  el_co,el_co  , fname=port_name + " " +file+" Cart", save_dir=save_dir )
        plot_norm_polar( el_co,el_co  , fname=port_name + " " +file+" Polar", save_dir=save_dir)
    
    #Put into one table
    el_results_table=pd.concat(list_of_rt,axis=1)
    
    ###############################################################################
    # Merge into final results table
    ###############################################################################

    final_results_table=results_final(az_results_table,el_results_table, port_name,save_dir)
    
    return final_results_table

###############################################################################
#
# Main 
#
###############################################################################

#import data
#Alternatively we can use sub dir=\\raw_data\\
all_ports=read_in_data_all_ports(    sub_dir = "\\raw_data_2\\"     )
save_dir= "\\processed_data\\"
save_path=os.getcwd()+save_dir
#os.makedirs(save_dir)

results_per_port=list()

#Generate table per port
for port_name in all_ports:

    print("Starting "+  port_name  +"....")
    results_per_port.append(calulated_based_per_port(all_ports[port_name],port_name,save_path))
    print("Finished "+  port_name  )

print("o.O.o")



