# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 09:48:26 2017

@author: matt.slevin

Functions to read in raw ascii datafiles, it then stores the files into a
one dictionary.  
"""

"""
TODO:
    Add support for different tilts. 
    the challange is that we dont nessarily know how many tilts there are for
    a particular antenna and not every tilt will have an az_co and az_cross. It
    could be solved by have Tilt dictionary. 

TODO:
    Add support for different ports. We dont know how many ports each antenna 
    will have the same tilts for every port.

TODO:
    Save the final dictionary as a pickel as a master file. Half set up

"""

import pandas as pd
import os
import pickle

#function to read in an ascii test file and generate a dictionary. Which 
#contains the amplitude and phase tables for a particular measurment.  
def read_to_panda(f_name):
    """
    Function to read in ascii data files from Midas. 
    P1= read_to_panda(f_name)
    """
    
    #Read in the file as a string
    f=open(f_name, 'r')
    string=f.read()
    f.close()
    
    #Split the file based on the frequency. Using the word 'frequency' as delimiter 
    data_per_frequency =string.split("Frequency") 
    
    #Initalise amplitude and phase dataframes
    df_amplitude=pd.DataFrame()
    df_phase=pd.DataFrame()
    
    #Initalise lists for each column
    amplitude=list()
    phase=list()

    #Loop to iterate through each frequency. Capturing each column appropriatly.      
    for j in range(1,len(data_per_frequency)):
        
        frequency_val= data_per_frequency[j].split("\t")[1] # Capture the frequency value
    
        #Get rid of the header file
        data_one_frequency=data_per_frequency[j].split("\t\n\t\t\t\n") 
    
        # data_per_f is now just our angle amplitude phase 
        phase.clear()
        amplitude.clear()
        
        #Seperate each row. 
        data_per_row=data_one_frequency[1].split("\n")
    
        #loop to sort each row into approiate list
        for i in range(0,len(data_per_row)-1):
            _, amplitude_val ,phase_val ,_ =data_per_row[i].split("\t")
            
            #Apend values onto end of list
            amplitude.append(amplitude_val)
            phase.append(phase_val)
    
        #put array into a panda    
        df_amplitude[frequency_val]= amplitude
        df_phase[frequency_val]= phase
        
    #create a dict with amp and phase tables as data frames
    data_frame_amp_phase={"amplitude":df_amplitude,"phase":df_phase}
        
    return data_frame_amp_phase

#Function to read in data for one port
def read_in_port_data():
    #File names    
    fname_az_copolar="OD AW3645 V1 R1 P1 N45 AZ CO PATT.txt"
    fname_az_cross="OD AW3645 V1 R1 P1 P45 AZ CR PATT.txt"
    fname_el_copolar="OD AW3645 V1 R1 P1 N45 EL CO PATT.txt"

    #Setting up path to subdir
    sub_dir = "\\RAW_DATA\\RAW_DATA\\"
    path=os.getcwd()+sub_dir

    #Read in each file
    az_co=read_to_panda(path+fname_az_copolar)
    az_cross=read_to_panda(path+fname_az_cross)
    el_co=read_to_panda(path+fname_el_copolar)

    #Put all measurments into a dict
    p1_data={"az_co":az_co,"az_cross":az_cross,"el_co":el_co}

    #dump the data
    #pickle.dump( p1_data, open( "p1_data.p", "wb" ) )

    return p1_data
