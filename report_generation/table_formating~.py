# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 09:20:52 2018

@author: matt.slevin
"""

"""
Script for the automatic generation of tables. (First Draft) 
"""

import pandas as pd
import os

###############################################################################
#
# Get a list of all the files.
#
###############################################################################

def get_fnames():
    path=os.getcwd()
    all_files=os.listdir(path) #All files in directory

    all_csv=list()
    
    for file in all_files:
        name,ext=file.split(".")
        
        if (ext == "csv" and name[0]=="P"):
            all_csv.append(file)
    
    return all_csv          
###############################################################################
#
# Read in the file
#
###############################################################################

#We will focus first on 3db bw measurment as an example
#Item we want to isolate
def get_item(all_csv,item):
    item_per_port=list()
    
    for i in all_csv:
        #Read in data
        p1=pd.read_csv(i)
        p1=p1.set_index("index")
    
        #Drop Avg, Max and Min
        p1=p1.drop(['Average', 'Max','Min'])
    
        #Isolate column from port file
        p1_item=p1[item]
        p1_item=p1_item.rename( i.split(" ")[0] )
        
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


#Just list here all the values you want to isolate
all_csv=get_fnames()

bw_3db= get_item(all_csv,"Az Co 3db BW")
F_b_ratio=get_item(all_csv, "Front to Back Ratio")
az_squint= get_item(all_csv,"Squint of 3dB Midpoint")
cross_pol= get_item(all_csv, "X Pol at sector")


""" To save to excel 
writer = pd.ExcelWriter('output.xlsx')
sub_table.to_excel(writer,'Sheet1')
writer.save()
"""

