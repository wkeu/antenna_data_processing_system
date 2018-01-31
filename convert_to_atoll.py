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
header_final="""Name;Gain (dBi);Manufacturer;Comments;Pattern;Pattern Electrical Tilt (°);BeamWidth;FMin;FMax;Frequency;V_WIDTH;FRONT_TO_BACK;Tilt;H_WIDTH;FAMILY;DIMENSIONS HxWxD(INCHES);Weight (LBS)
AWXXX;17.7;Alpha Wireless;;2 0 0 360 """

footer_final="0;181;57;;;3550;7;41;;57;;;"

middle = "1 0 360 "

#Convert data to planent string format
def convert_data_to_str(data):
    string=""
    a=0
    
    for i in data:
        string += str(a) + " " + str(round(i,1)) +" "
        a+=1 
        
    return string

#Horizontal
horz_final=convert_data_to_str(abs(horz_data_norm))

#Vertical

vert_final=convert_data_to_str(abs(vert_data_norm))

final_planet= header_final + horz_final + middle + vert_final + footer_final

f = open('test1.Atoll.Txt','w')
f.write(final_planet)
f.close()

print("o.O.o")
