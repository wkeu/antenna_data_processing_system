# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 15:07:00 2018

@author: Matt Slevin
"""

from generate_data import Generate_data

source_dir="C:/Users/Matt Slevin/Documents/GitHub/antenna_data_processing_system/antenna_raw_data/sector_data/AW3014"
save_path= "C:/Users/Matt Slevin/Documents/GitHub/antenna_data_processing_system"

#Create a Generate_data object. With aLL methods and function calls
gen_data = Generate_data(source_dir, 
                         save_path, 
                         antenna_type="Sector", 
                         Images=True, 
                         Report=True, 
                         Pattern_Files=True)

gen_data.clear_processed_data()

#Test by runing the program 
gen_data.run()
