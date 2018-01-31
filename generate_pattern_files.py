# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 15:15:14 2018

@author: matt.slevin
"""

from convert_to_planet import * 

#def generate_pattern_files(all_ports,results_per_port,antenna_model):
    
save_dir= "\\processed_data\\patterns\\planet\\"
save_path=os.getcwd()+save_dir

horz_data_all=all_ports["P1"]["AZ T0 CO"]["amplitude"]
vert_data_all=all_ports["P1"]["EL T0 CO"]["amplitude"]