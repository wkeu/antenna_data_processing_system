
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 15:14:12 2018

@author: matt.slevin
"""
from generate_data import * 

#read in the data
all_ports=read_in_data_all_ports(    sub_dir     )

#isolate horizontal and vertical data
horz_data_all=all_ports["P1"]["AZ T0 CO"]["amplitude"]
vert_data_all=all_ports["P1"]["EL T0 CO"]["amplitude"]

for freq in horz_data_all:
    horz_data = horz_data_all[freq].convert_objects(convert_numeric=True)
    vert_data = vert_data_all[freq].convert_objects(convert_numeric=True)
    
    #Normalise
    test_ant=Sector("test")
    horz_data_norm, _ =test_ant.normalise2(horz_data,horz_data)
    vert_data_norm, _ =test_ant.normalise2(vert_data,vert_data)
    
    
    #Convert data to planent string format
    def convert_data_to_str(data):
        string=""
        
        for i in data:
            string += str(round(i,1)) + "\n" 
        
        return string
    
    #Horizontal
    horz_final=convert_data_to_str(abs(horz_data_norm))
    
    #Vertical
    vert_final=convert_data_to_str(abs(vert_data_norm))
    
    #Construct Final String 
    final_planet = horz_final + vert_final 
    final_planet = final_planet.rstrip('\n')
    
    f = open('test'+str(freq)+'.ant','w')
    f.write(final_planet)
    f.close()
    
    print("o.O.o")

print("o.O.0.O.o")


