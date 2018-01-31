# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 15:14:12 2018

@author: matt.slevin
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 12:21:19 2018

@author: matt.slevin
"""

from generate_data import * 

#read in the data
all_ports=read_in_data_all_ports(    sub_dir     )

#isolate horizontal and vertical data
horz_data=all_ports["P1"]["AZ T0 CO"]["amplitude"]
vert_data=all_ports["P1"]["EL T0 CO"]["amplitude"]

horz_data = horz_data["3300.00"].convert_objects(convert_numeric=True)
vert_data = vert_data["3300.00"].convert_objects(convert_numeric=True)

#Normalise
test_ant=Sector("test")
horz_data_norm, _ =test_ant.normalise2(horz_data,horz_data)
vert_data_norm, _ =test_ant.normalise2(vert_data,vert_data)


"""
for i in horz_data_norm

["3550.00"]

["3550.00"]
"""

#def convert_data_to_str()


#Header
header_final="""NAME AW3014
MAKE Alpha Wireless Ltd
FREQUENCY 3550.0
H_WIDTH 65
V_WIDTH 7
FRONT_TO_BACK 30
GAIN 17.7dBi
TILT ELECTRICAL
"""

#Convert data to planent string format
def convert_data_to_str(data):
    string=""
    a=0.0
    
    for i in data:
        string += str(a) + "\t" + str(round(i,1)) + "\n" 
        a+=1.0
        
    return string

#Horizontal
horz_header = "HORIZONTAL  360\n"
horz_final=horz_header+convert_data_to_str(abs(horz_data_norm))

#Vertical
vert_header = "VERTICAL  360\n"
vert_final=vert_header+convert_data_to_str(abs(vert_data_norm))

final_planet= header_final + horz_final + vert_final

f = open('test.msi','w')
f.write(final_planet)
f.close()

print("o.O.o")


