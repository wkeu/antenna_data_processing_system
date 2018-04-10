# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 12:05:38 2018

@author: matt.slevin
"""

# This is a working progress. We need to talk with Cao about a better way
# to automate this. 

from generate_data import * 

#read in the data
all_ports=read_in_data_all_ports(    sub_dir     )
save_dir= "\\processed_data\\patterns\\planet\\"
save_path=os.getcwd()+save_dir

#Aim is to find T5 from a guess

el_t0=all_ports["P1"]["EL T0 CO"]["amplitude"]
el_t5=all_ports["P1"]["EL T5 CO"]["amplitude"]
el_t10=all_ports["P1"]["EL T10 CO"]["amplitude"]

el_t0 = el_t0["1800.00"].convert_objects(convert_numeric=True)
el_t5 = el_t5["1800.00"].convert_objects(convert_numeric=True)
el_t10 = el_t10["1800.00"].convert_objects(convert_numeric=True)


el_t0_np = np.asarray(el_t0)
el_t10_np = np.asarray(el_t10)

#Roll so that both mamimums are at 180 degrees
el_t0_np=np.roll(el_t0_np, -2)
el_t10_np=np.roll(el_t10_np, -11)

el_t5_guess=(el_t0_np+el_t10_np)/2

el_t5_guess=np.roll(el_t5_guess, 5)