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
import numpy as np


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


#Function to automatically ananlise directory and determine all the files in the 
# directory and which port that they belong in.

#TODO:Error checks for the fdir
    #Different model
    #Naming convention wrong
    #Different lenghts
    #Differnt number of measurments per port
def get_file_names_in_dir(path):

    all_files=os.listdir(path) #All files in directory
    
    #Tokenize file names into a list
    all_files_tokenized=list()
    
    for line in all_files:
        line = line.strip()
        if len(line) > 0:
            words = line.split(" ")
            all_files_tokenized.append(words)
    
    #Put into a data frame
    panda=pd.DataFrame(all_files_tokenized)
    
    #This might be needed at a later date. It creates a dict with all ports 
    # and tilts
    
    #Find all of ports
    port_idx=4
    all_ports=panda[port_idx]
    all_ports=all_ports.drop_duplicates()
    number_of_ports=len(all_ports)
    
    #Find the number of the tilts
    tilt_idx=6
    all_tilts=panda[tilt_idx]
    all_tilts=all_tilts.drop_duplicates()
    number_of_tilts=len(all_tilts)
    
     
    #Organise panda into a dictionary for each port 
    n_ports = dict()    
    for i in all_ports:
        n_ports[i] = panda[panda[port_idx] == i]
    
    #Edit all elements in the dictionary so that they are a string and change index 
    for i in all_ports:
        #Isolate port measurment
        pn=n_ports[i]
        #Create index
        pn_index=pn[7] + " " + pn[6] + " " + pn[8]
        
        #Merge all strings into one
        pn=pn[np.arange(0,len(n_ports[i].columns))].apply(lambda x: ' '.join(x), axis=1) 
        
        #Change the index
        frame=[pn,pn_index]
        pn = pd.concat(frame,axis=1)
        pn=pn.set_index(pn[1])
        pn=dict(pn[0])
    
        #Update n_ports
        n_ports[i] = pn 

    return n_ports

#Function to read in data for one port
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
            data[port][file]=read_to_panda(path+f_names[port][file])

    #dump the data
    #pickle.dump( p1_data, open( "p1_data.p", "wb" ) )

    return data
