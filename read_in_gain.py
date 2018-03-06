# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 09:54:40 2018

@author: MJ.McAssey
"""

from pandas import DataFrame, read_csv
import pandas as pd
import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as sp
import pylab
from file_merge import *
  
#def get_file_names_in_dir(path):




sub_dir="\\Gain\\raw_data"
path=os.getcwd()+sub_dir

def get_file_names_in_dir(path):
    all_files=os.listdir(path) #All files in directory
    
    #Tokenize file names into a list
    all_files_tokenized=list()
    
    for line in all_files:
        
        line=line.split(".")[0]
        if len(line) > 0:
            words = line.split(" ")
            all_files_tokenized.append(words)
    
    #Put into a data frame
    panda=pd.DataFrame(all_files_tokenized)
    
    #Find all of ports
    port_idx=4
    all_ports=panda[port_idx]
    all_ports=all_ports.drop_duplicates()
    number_of_ports=len(all_ports)
    
    #Find Polarisation of all files
    pol_idx = 5
    all_pols = panda[pol_idx]
    all_pols=all_pols.drop_duplicates()
    number_of_pol=len(all_pols)
        
    #Find the number of the tilts
    tilt_idx=6
    
    all_tilts=panda[tilt_idx]
    all_tilts=all_tilts.drop_duplicates()
    number_of_tilts=len(all_tilts)
    
    #Organise panda into a dictionary for each polarisation
    n_pol = dict()
    for i in all_pols:
        n_pol[i] = panda[panda[pol_idx] == i]
    
    #Edit all elements in the dictionary so that they are a string and change index 
    for i in all_pols:
        #Isolate port measurment
        pn=n_pol[i]
        #Create index
        pn_index=pn[6]
        
        #Merge all strings into one
        pn=pn[np.arange(0,len(n_pol[i].columns))].apply(lambda x: ' '.join(x), axis=1) 
        
        #Change the index
        frame=[pn,pn_index]
        pn = pd.concat(frame,axis=1)
        pn=pn.set_index(pn[0])
        pn=dict(pn[0])
    
        #Update n_ports
        n_pol[i] = pn 
        
    return n_pol
#############################################################

def read_in_data_all_ports(sub_dir):
    
    path=os.getcwd()+sub_dir
    f_names=get_file_names_in_dir(path)

    #Copy fnames for storing data
    data=f_names

    #Nested loop for reading in each file
    for port in f_names:
        print(port)
        for file in f_names[port].keys():
            print(file)
            #print("\t"+f_names[port][file])
            data[port][file]=read_to_panda(path+"\\"+f_names[port][file]+".dat")

    #dump the data
    #pickle.dump( p1_data, open( "p1_data.p", "wb" ) )

    return data



#################################################
def read_to_panda(f_name):
    

    f=open(f_name, 'r')
    data_str=f.read()
    f.close()

    data_list=data_str.split("\n")

    #Get rid of first three line and last line
    data_list=data_list[3:-1]

    #Loop to create list for frequency and amp

    amp_list=list()
    freq_list=list()

    for i in data_list:
        freq = i.split(",")[0]
        amp = i.split(",")[1]
    
        freq_list.append(float(freq)/1e6)
        amp_list.append(float(amp))
    

    df = pd.DataFrame(amp_list,freq_list)

    df.rename(columns={0:'Amp'},inplace = True)
    df.rename_axis = ('freq')
    
    
    return(df)

#define get tilit
def get_tilt(fname):
    # Function to extract the tilt from fname
    a = fname.split()

    for b in a:
        if "T" in b:
            _, tilt_angle = b.split("T")

    return ("T"+tilt_angle)

def get_port(fname):
    # Function to extract the tilt from fname
    a = fname.split(" ")
    a = a[4].split("P")

    return ("P"+a[1])




def sort_by_tilt(directory):

    #To use exsiting nested data structure 
    new_directory = directory.copy() #Keep this line. It prevents changes to the orginal
    
    #Cylce through each pol
    for pol in directory:
        
        #All tilt in pol
        tilt_list=list()
        
        #Find all tilts in pol
        for i in directory[pol].keys():
            tilt=get_tilt(i)
            
            if tilt not in tilt_list:
                tilt_list.append(tilt)
    
        #Formating on the data structe
        new_directory[pol] = {tilt: dict() for tilt in tilt_list}
        
        #Copys data into new data structure 
        for j in directory[pol].keys():
            
            tilt=get_tilt(j)
            port=get_port(j)
            
            new_directory[pol][tilt][port]=directory[pol][j]
            
    return new_directory

directory = read_in_data_all_ports(sub_dir)
  
#Clean up
directory = sort_by_tilt(directory)
    
#Create an emply 


'''
aut_ant= read_to_panda("AW3629 N45 P1 T0.dat")
ref_ant= read_to_panda("REF GAIN N45.dat")


gain = read_to_panda('FR6509.txt')

calc_gain = gain - (ref_ant - aut_ant)

calc_gain = calc_gain.interpolate()


calc_gain.to_csv('out.csv', sep =',')
plt.plot(calc_gain)
plt.savefig('plot.png')
'''


