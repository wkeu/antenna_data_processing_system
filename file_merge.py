# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 09:48:26 2017

@author: matt.slevin
"""
import pandas as pd
import os as os 
import numpy as np
#Script one, for organising data storage. Raw input is the csv files.  

#
#   Import all our data files to pandas
#

def read_to_panda(f_name):
    """
    Function to read in ascii data files from Midas. 
    amplitude, phase = read_to_panda(f_name)
    """
    
    
    #Read in the file 
    f=open(f_name, 'r')
    string=f.read()
    
    #Split the file based on the frequency,
    a =string.split("Frequency") 
    
    #Initalise amplitude and phase dataframes
    df_amplitude=pd.DataFrame()
    df_phase=pd.DataFrame()
    
    angle=list()
    amplitude=list()
    phase=list()
    
    for j in range(1,len(a)-1):
        frequency= a[j].split("\t")[1] # Capture the frequency value
    
        b=a[j].split("\t\n\t\t\t\n") #Get rid of the header file
    
        # b[1] is now just our angle amplitude phase 
        angle.clear()
        phase.clear()
        amplitude.clear()
    
        c=b[1].split("\n")
    
        for i in range(0,len(c)-1):
            d,e,f,g=c[i].split("\t")
    
            angle.append(d)
            amplitude.append(e)
            phase.append(f)
    
        #Convert a list to a numpy array 
        angle_np = np.asarray(angle, dtype=np.float32)
        amplitude_np = np.asarray((amplitude), dtype=np.float32)
        phase_np = np.asarray(phase, dtype=np.float32)
    
        #
        # Put into a panda
        #
    
        df_amplitude[frequency]= amplitude_np
        df_phase[frequency]= phase_np
        
    return df_amplitude,df_phase

#The working directory is,
#f_dir="C:\Users\matt.slevin\Documents\data acquisition_systme\RAW_DATA\RAW_DATA"

cd "C:\Users\matt.slevin\Documents\data acquisition_systme\RAW_DATA\RAW_DATA"

# TODO: Set up automatic change to our working dir
#os.chdir("Users\matt.slevin\Documents\data acquisition_systme\RAW_DATA\RAW_DATA")

#Port 1
fname_az_copolar="AW3023_V4_R1_AZ_CO_P1_T0.txt"
fname_az_cross="AW3023_V4_R1_AZ_CR_P1_T0.txt"
fname_el_copolar="AW3023_V4_R1_EL_CO_P1_T0.txt"

az_co=read_to_panda(fname_az_copolar)
az_cross=read_to_panda(fname_az_cross)
el_co=read_to_panda(fname_el_copolar)

p1_data=[az_co,az_cross,el_co]
#break line by line
#break into tabs





#Read in csv file as a string
#Put into panda dataframes, or numpy

az_co=pd.read_csv(az_copolar)

#
#   Formating of our panda files (get rid of our unessary data)
#

#Save panda as a json

#For testing purposes read the json f


#
# Micilanious 
#

"""
Functions which could be usefull

os.getcwd() - get the current working directory
os.chdir("f_dir") - change the working dir to f_dir
os.listdir("f_dir") - get a list of files in a specific dir
os.remove("f_name") - delete f_name from the directory
os.mkdir("f_dir") - Create a subdirectory f_dir
"""



