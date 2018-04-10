"""

Functions for rading in files for gain purposes. It is very similar to 
file_megre.py. As gain calculations are different it requires the data to be read
in differently.

"""

import pandas as pd
import os
import copy

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

def list_to_tokenized_panda(all_files):    
        #Tokenize file names into a list
        all_files_tokenized=list()
        
        for line in all_files:
            line = line.strip()
            if len(line) > 0:
                words = line.split(" ")
                all_files_tokenized.append(words)
        
        #Put into a data frame
        df=pd.DataFrame(all_files_tokenized)
        
        return df

def group_by_item(all_files, item_idx):
    #Function to group a list into a dict

    df=list_to_tokenized_panda(all_files)

    all_items = df[item_idx]
    all_items = all_items.drop_duplicates()

    #Group into nested structure
    dict_grouped = dict()
    for i in all_items:
        dict_grouped[i] = df[df[item_idx] == i]

    #Merge coulumns into o string
    for i in dict_grouped:
        dict_grouped[i]= (    
                dict_grouped[i][0] + " " +
                dict_grouped[i][1] + " " +
                dict_grouped[i][2] + " " +
                dict_grouped[i][3] + " " +
                dict_grouped[i][4] + " " +
                dict_grouped[i][5] + " " +  
                dict_grouped[i][6] + " " +
                dict_grouped[i][7] + " " +
                dict_grouped[i][8] + " " +
                dict_grouped[i][9] 
                    )
        
        #Convert df to list
        dict_grouped[i] = dict_grouped[i].tolist()
            
    return dict_grouped

#Function to automatically ananlise directory and determine all the files in the 
# directory and which port that they belong in.

#TODO:Error checks for the fdir
    #Different model
    #Naming convention wrong
    #Different lenghts
    #Differnt number of measurments per port
def get_file_names_in_dir(path):
    
    all_files = os.listdir(path) #All files in directory
    
    #Group by pol
    pol_idx = 5    
    nested_data_structure = group_by_item(all_files, pol_idx)

    #Group by tilt
    tilt_idx = 6
    for i in nested_data_structure:
        nested_data_structure[i]  = group_by_item(nested_data_structure[i], tilt_idx)

    #Group by port
    port_idx = 4
    for pol in nested_data_structure:
        for tilt in nested_data_structure[pol]:
            nested_data_structure[pol][tilt]= group_by_item(nested_data_structure[pol][tilt], port_idx)
    
    return nested_data_structure
   
#Function to import gain files
def read_in_gain_files(path):    
    
    f_names=get_file_names_in_dir(path)
    
    #Copy fnames for storing data
    data = copy.deepcopy(f_names)
    
    #Nested loop for reading in each file
    for pol in f_names:
        print(pol)
        for tilt in f_names[pol].keys():
            print("\t"+tilt)
            
            for port in f_names[pol][tilt].keys():
                print("\t\t"+port)
                
                for i in range(0,len(f_names[pol][tilt][port])):
                    data[pol][tilt][port][i]=read_to_panda(path+"\\"+f_names[pol][tilt][port][i])  
    return data
