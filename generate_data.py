# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 15:33:12 2018

@author: matt.slevin
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 10:37:37 2017

@author: matt.slevin

Before running this file. Make sure that you set the working directory to the 
working git repository. 
"""

###############################################################################
#
#   Import Libaries
#
###############################################################################

from file_merge import * 
from antennas import *
from antenna_plots import *
import pandas as pd
import os
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

"""
#Parse In arguments
parser = argparse.ArgumentParser(description='Process test data of Antenna.')

parser.add_argument('sub_dir', type=str, default="raw_data_2",
                    help='The directory of the antenna test files, ex raw_data_5')

args = parser.parse_args()

print(str(args.sub_dir))


#Set to true to turn the images on. Flase for off

sub_dir = "\\"+args.sub_dir+"\\"
"""

sub_dir="\\raw_data_2\\"
IMAGES=True

###############################################################################
#
#   Results table
#
###############################################################################
#Results table for azimuth measurments
def results_table_az(az_co,az_cr):
    
    az_co = az_co.convert_objects(convert_numeric=True)
    az_cr = az_cr.convert_objects(convert_numeric=True)
    
    test_antenna=Sector("test")
    
    #Convert to usable format
    
    #Calculate
    xpol_at_sector = test_antenna.sector_xpol(az_co,az_cr)                                           # import function sector_xpol                     
    fbr = test_antenna.front_to_back(az_co)                                                          # import function front_to_back
    az_bw_3db = test_antenna.find_3db_bw(az_co,"Az Co 3db BW")
    squint= test_antenna.find_squint(az_co)
    
    #Put into a dataframe
    results = pd.DataFrame()
    results = pd.concat([az_bw_3db,squint,xpol_at_sector,fbr],axis = 1)
    
    return results

#Results table for elevation measurments
def results_table_el(el_co,fname="EL TX"):

    el_co = el_co.convert_objects(convert_numeric=True)
    
    t_ant = Sector("test")
    
    el_bw_3db = t_ant.find_3db_bw(el_co,"3db BW "+fname)
    first_usl= t_ant.find_first_usl(el_co,"first_usl "+fname)
    usl_range = t_ant.find_usl_in_range(el_co,measurement_type="usl_range "+fname)
    usl_range_bs = t_ant.find_usl_in_range(el_co, measurement_type="usl_range bs"+fname, Boresight=True)
    peak_dev = t_ant.peak_tilt_dev(el_co,'Peak dev of Peak'+fname,fname)
    tilt_dev = t_ant.find_tilt_dev(el_co,'Tilt dev of Peak'+fname,fname)    
    
    #Put into a dataframe
    results = pd.DataFrame()
    results = pd.concat([el_bw_3db,first_usl,usl_range,usl_range_bs,peak_dev,tilt_dev],axis = 1)
    
    return results


#Merge AZ and EL into one results table. And final formatting
def results_final(final_results_table,port_name,save_dir): 
    
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

# Function which returns the names of the Azmuth measurements. It is assumed 
# that there will only be one co and one cross measurment. 
def find_az_co_cr(P1):

    #If co and cross are not detected then return false for the strings.
    co_str=False
    cr_str=False
    
    #Loop for 
    for i in P1:    
    
        #Check if it is a A
        if (i.split(" ")[0]=="AZ"):
            
            if (i.split(" ")[2]=="CR"):
                cr_str=i
                
            else:
                co_str=i
    
    return co_str,cr_str

#Function to do calculations based on the port and tilts. It generates all 
#tables for az calculations and then el calculations. It the merges and returns 
#results table.  

#TODO if AZ is not present. It will break the results table. This is not ideal. 
    
def is_empty(any_structure):
    if any_structure:
        return False
    else:
        return True

def calulated_based_per_port(P1,port_name,save_dir):
    P1=dict(P1) #Keep this! Ensures a copy was made.
    
    ###############################################################################
    # Azimuth (Calculations and Plots)
    ############################################################################### 
    
    #Do Azimuth Calculations first, removing them from P1 in the process
    
    az_co_str, az_cr_str = find_az_co_cr(P1)
    
    #Co and Cross not detected
    if (az_co_str == False) and (az_cr_str == False):
        print ("Notification: AZ_CO and CO_CR were not detected.")
    
    #Only Co detected
    elif ( isinstance(az_co_str,str)) and (az_cr_str == False):
        print ("Notification: Only AZ_CO was detected.")
        
        az_co=P1.pop(az_co_str)
        az_co=az_co["amplitude"]
        az_cr=az_co
        
        #Generates r esults table
        az_results_table=results_table_az(az_co,az_co)
       
    #Both Cr and Co detected
    else:
        print ("Notification: AZ Co and Cross detected.")
        az_co=P1.pop(az_co_str)
        az_cr=P1.pop(az_cr_str)
        
        az_co=az_co["amplitude"]
        az_cr=az_cr["amplitude"]
        
        #Generates r esults table
        az_results_table=results_table_az(az_co,az_cr)
    
    #Plots
    if (IMAGES and isinstance(az_co_str,str)):
        plot_norm_cart(  az_co,az_cr  ,  fname=port_name +" AZ Cart", save_dir=save_dir)
        plot_norm_cart_interacive_az(  az_co,az_cr  ,  fname=port_name +" AZ Cart", save_dir=save_dir)
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
        if(IMAGES):
            plot_norm_cart(  el_co,el_co  , fname=port_name + " " +file+" Cart", save_dir=save_dir )
            plot_norm_polar( el_co,el_co  , fname=port_name + " " +file+" Polar", save_dir=save_dir)
            plot_norm_cart_interacive_el(  el_co, fname=port_name + " " +file+" Cart", save_dir=save_dir)
    
    #Put into one table
    if is_empty(not(list_of_rt)):
        el_results_table=pd.concat(list_of_rt,axis=1)
    
    ###############################################################################
    # Merge into final results table
    ###############################################################################
    
    #Both
    if isinstance(az_co_str,str) and is_empty(not(list_of_rt)) :
        merged_table=pd.concat([az_results_table,el_results_table],axis=1)

    #Only AZ
    elif(isinstance(az_co_str,str)):
        merged_table=az_results_table

    #Only EL
    else:
        merged_table=el_results_table

    

    final_results_table=results_final(merged_table, port_name,save_dir)
    
    return final_results_table

###############################################################################
#
# Master Results table Generation 
#
###############################################################################
    
#TODO: Move the results table generation to a seperate file. 
    
#Get a clean list of all measurements. 
def get_list_of_measurements(results_per_port):
    P1=results_per_port[0]

    key_list=list(P1.keys())

    #Clean up keys list. Remove all @ Angle
    while "@ Angle" in key_list:
        key_list.remove("@ Angle")
    
    return key_list

#Function to generate a table for a summary table for a given item. 
def generate_table_per_item(results_per_port,item):
    #Ported from old code
    item_per_port=list()
      
    port=1
    
    for i in results_per_port:
        #Read in data
        p1=i
    
        #Drop Avg, Max and Min
        p1=p1.drop(['Average', 'Max','Min'])
    
        #Isolate column from port file
        p1_item=p1[item]
        p1_item=p1_item.rename( str(port) )
        port+=1
        
        #Append to a list
        item_per_port.append(p1_item)
    
    #Create the sub_table
    sub_table=pd.DataFrame(item_per_port)
    sub_table= sub_table.T
    
    #Create summary table
    max_val=    [sub_table.values.max()]*len(sub_table)
    min_val=    [sub_table.values.min()]*len(sub_table)
    mean_val=   [sub_table.values.mean()]*len(sub_table)
    
    summary_table = pd.DataFrame({"max":max_val,"min":min_val,"mean":mean_val}, sub_table.index)
    summary_table = round(summary_table,2)
    
    #Create one table
    final_table = pd.concat([sub_table,summary_table],axis=1)
    
    return final_table

#Function to generate a master table 
def generate_master_table(results_per_port,save_path):
    
    #Get a clean list of results
    measurements_lst = get_list_of_measurements(results_per_port)
    list(range(0,len(measurements_lst)))
    
    final_tables=list()
    
    #
    for item in measurements_lst:

        final_tables.append(  generate_table_per_item(results_per_port,item)  )
        
    #Save to an excel sheet
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(save_path+'master_table.xlsx', engine='xlsxwriter')

    for i in range(0,len(final_tables)):
        # Write each dataframe to a different worksheet.
        final_tables[i].to_excel(writer, sheet_name=measurements_lst[i])
        
    writer.save()



###############################################################################
#
# Main 
#
###############################################################################

if __name__ == "__main__":
    #import data
    #Alternatively we can use sub dir=\\raw_data\\
    
    all_ports=read_in_data_all_ports(    sub_dir     )
    save_dir= "\\processed_data\\"
    save_path=os.getcwd()+save_dir
    #os.makedirs(save_dir)
    
    results_per_port=list()
    
    #Generate table per port
    for port_name in all_ports:    
        print("Starting "+  port_name  +"....")
        results_per_port.append(calulated_based_per_port(all_ports[port_name],port_name,save_path))
        print("Finished "+  port_name)
    
    generate_master_table(results_per_port,save_path)
    
    print("o.O.o")