##############################################################
# Script to run test on generate_data (Full backend test)
##############################################################

from generate_data import Generate_data
from file_merge import read_in_data_all_ports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from antenna_plots import *
import pandas as pd
from file_merge import *
from file_merge2 import *
from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt
import os as os
'''def rotate_all_ports(all_ports,rotate_angle=45):

    all_ports_rotated=all_ports.copy()
    
    #Port
    for port in all_ports:
        
        #Mesurment
        for measurement in all_ports[port]:
        
            #Rotate Panda
            pd_waves = all_ports[port][measurement]["amplitude"]
            pd_waves_rotated=rotate_panda(pd_waves, rotate_angle)
            all_ports_rotated[port][measurement]["amplitude"]=pd_waves_rotated
    
    return all_ports_rotated

    
def rotate_panda(pd_waves, rotate_angle):
    
    #Transpose to make easier to dice and splice
    
    a=pd_waves[0:rotate_angle]
    b=pd_waves[rotate_angle:len(pd_waves)]
    
    frames=[b,a]
    result = pd.concat(frames)
    result = result.reset_index()
    result = result.drop(['index'], axis=1)
    
    return result'''
    


def formatting_on_golden_ref(ref_golden):
    
    ref_golden = ref_golden.convert_objects(convert_numeric=True)
    ref_golden["Freq(MHz)"] = ref_golden["Freq(MHz)"].astype(float)
    ref_golden = ref_golden.round(1)
    
    ref_golden = ref_golden.set_index("Freq(MHz)")
    
    return ref_golden

def find_df_peak(df):  
    
    #Functions to find peaks 
    df = df.convert_objects(convert_numeric=True)
    peak_amp = df.max()  
    peak_angle = df.idxmax()

    #Convert to a frame
    peak_amp = peak_amp.to_frame()

    return peak_amp

def find_max_amp(measurements):
    
    peaks=list()

    #Function to mind the maximum amplitude of either az or el     
    for measurement in measurements:
        peaks.append(find_df_peak(measurement["amplitude"])) 
    
    # convert list to df 
    peaks = pd.concat(peaks,axis=1)
    
    peaks = peaks.max(axis=1)
    peaks = peaks.to_frame()
    
    return peaks

def formatting_on_panda(amp_df,measuremet):
    #Function to formats panda
    amp_df['index'] = amp_df.index
    amp_df = amp_df.convert_objects(convert_numeric=True)
    amp_df = amp_df.round(1)
    amp_df = amp_df.set_index("index")
    amp_df.columns = [measuremet]
    
    return amp_df

def open_golden_ref(golden_ref_path,ref_ant):
    #Open excel document
    xl = pd.ExcelFile(golden_ref_path)
    ref_golden = xl.parse(ref_ant)
    ref_golden = formatting_on_golden_ref(ref_golden)
    
    return ref_golden

def find_bounds(ref_amp,ref_golden):
    
    ref_amp_max = max(ref_amp.index)
    ref_amp_min = min(ref_amp.index)
    
    ref_golden_max = max(ref_golden.index)
    ref_golden_min = min(ref_golden.index)
    
    upper_lim = min(ref_amp_max,ref_golden_max)
    lowwer_lim = max(ref_amp_min,ref_golden_min)

    if (ref_golden_max<ref_amp_max): 
        print("Warning: For gain, missing data. Refrence antenna frequency is out of frequency bounds. (Too High) ")
 
    if (ref_golden_min>ref_amp_min):
        print("Warning: For gain, missing data. Refrence antenna frequency is out of frequency bounds. (Too Low) ")
    
    return upper_lim,lowwer_lim

def find_aut_max_amps(ant_measurment):
    #Find all peaks in measurements 
    
    #Do for all measurements on nested loop  
    for pol in ant_measurment:
        for tilt in ant_measurment[pol].keys():
            for port in ant_measurment[pol][tilt]:
                peaks = find_max_amp(  ant_measurment[pol][tilt][port]  )
                peaks = formatting_on_panda(peaks,'AUT')
                ant_measurment[pol][tilt][port] = peaks
                
    return ant_measurment

def find_ref_max_amps(ant_measurment):
    #Find all peaks in measurements 
    
    #Do for all measurements on nested loop  
    for pol in ant_measurment:
        for tilt in ant_measurment[pol].keys():
            for port in ant_measurment[pol][tilt]:
                peaks = find_max_amp(  ant_measurment[pol][tilt][port]  )
                peaks = formatting_on_panda(peaks,'REF')
        
        
        ant_measurment[pol] = peaks        
                
    return ant_measurment

# Function which will calculate gain 
def calc_gain(aut_measurment, ref_measurment, ref_golden ):
    
    gain_pol_results = dict()
    
    for pol in aut_measurment:
        
            gain_tilt_results = dict()
            
            for tilt in aut_measurment[pol].keys():
                
                gain_per_port = list()
                
                for port in aut_measurment[pol][tilt]:
                    
                    #TODO: this can probably be refactored 
                    master_table = pd.concat(
                            [aut_measurment[pol][tilt][port],ref_measurment[pol] ,ref_golden[pol]  ],
                            axis=1)
                    
                    # Define the limits of the panda
                    upper_lim,lowwer_lim = find_bounds(ref_measurment[pol],ref_golden[pol])
                    # Discard values outside of range
                    master_table=master_table.loc[lowwer_lim:upper_lim] 
                    # Interpolate
                    master_table=master_table.interpolate(method='linear', axis=0)
                    
                    #Calculate gain
                    gain = master_table[pol] - (master_table["REF"] - master_table["AUT"])
                    gain = gain.to_frame()
                    gain.columns = [port]
                    
                    gain_per_port.append(gain)
                    
                gain_per_port = pd.concat( gain_per_port ,axis=1)
                    
                gain_tilt_results[tilt] = gain_per_port
             
            #Overall result
            gain_pol_results[pol] = gain_tilt_results
            
    return gain_pol_results
    
def generate_plots(gain, save_dir):
    
    for pol in gain:
        print(pol)
        for tilt in gain[pol]:
            plot_gain(gain[pol][tilt],save_dir,pol,tilt)

    print("gain plots generated")

def plot_gain(gain_df,save_dir,pol,tilt):

    plt.ioff()
    
    labels= list(gain_df.keys())
    
    fig1 = plt.figure(figsize=[13,7])
    ax1 = fig1.add_subplot(111)
    ax1.plot(gain_df,linewidth=2,alpha=0.75)  
    
    #Set axis parameters
    ax1.grid(alpha=0.25)
    ax1.set_ylim(
            [0,
             int(gain_df.max()[0]+5)]
            )
    
    ax1.set_title("Gain")
    ax1.legend(labels,framealpha=0.75)
    ax1.set_ylabel('dBi')
    ax1.set_xlabel('Frequency (MHz)')
    
    plt.savefig(
            save_dir+ "\\images\\GAIN\\"+pol+ " " +tilt+'.png',
            dpi=300
            )     
    plt.close('all') 
    
    plt.ion()

###############################################################################
# Main
###############################################################################
def run_gain(ref_golden_model,aut_path,ref_path):

    #Read in golden refrence data    
    golden_ref_path = os.getcwd() + "\\antenna_raw_data\\golden_ref_gain\\gain_standards_golden_refrence.xlsx"
    ref_golden = open_golden_ref(golden_ref_path, ref_golden_model)
    
    aut_measurment = read_in_gain_files(aut_path)
    aut_measurment = find_aut_max_amps(aut_measurment)
    
    ref_measurment = read_in_gain_files(ref_path)
    ref_measurment = find_ref_max_amps(ref_measurment)
    
    gain_results = calc_gain(aut_measurment, ref_measurment, ref_golden )
    
    return gain_results

def export_to_excel(gain,save_dir,fname,resample_factor=1):
    names_of_measurments = list()
    final_tables= list()
    
    #
    for pol in gain:
        for tilt in gain[pol].keys():
            a = gain[pol][tilt].iloc[::resample_factor, :]
            final_tables.append(  a  )
            names_of_measurments.append(pol+" "+tilt)
        
    #Save to an excel sheet
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(save_dir+'//'+fname+'.xlsx', engine='xlsxwriter')
    
    for i in range(0,len(final_tables)):
        # Write each dataframe to a different worksheet.
        final_tables[i].to_excel(writer, sheet_name=names_of_measurments[i])
        
    writer.save()


#TODO: Move this to antenna_plots.py 
def gain_main(save_dir,source_dir,ref_golden_model):
    #Gain refrence model
    ref_golden_model = "AW3023"
    aut_path = source_dir + "\\aut_ant"
    ref_path = source_dir + "\\ref_ant"
    
    gain = run_gain(ref_golden_model,aut_path,ref_path)
    generate_plots(gain, save_dir)
    
    fname1="master_gain_table"
    export_to_excel(gain,save_dir,fname1,resample_factor=1)
    fname2="gain_table"
    export_to_excel(gain,save_dir,fname2,resample_factor=5)




source_dirA="C:/Users/mj.mcassey/Documents/trial/antenna_data_processing_system-master/antenna_raw_data/sector_data/AW3649/aut_ant"
#source_dirB="C:/Users/mj.mcassey/Documents/trial/antenna_data_processing_system-master/antenna_raw_data/sector_data/AW3014"
save_path="C:/Users/mj.mcassey/Documents/trial/antenna_data_processing_system-master/result"

all_ports=read_in_data_all_ports(    source_dirA + "/"    )

control = all_ports["P1"]["AZ T0 CO"]["amplitude"]
plot_norm_cart_interacive_el(control, "control", save_path)

rotate_angle= 45 #degrees, note ensure that this is a postivie angle 
                 #this angle rotates back
                 
#all_ports_rotated = rotate_all_ports(all_ports,rotate_angle) #Always rotating to the left

#test = all_ports_rotated["P1"]["AZ T0 CO"]["amplitude"]
#plot_norm_cart_interacive_el(test, "test_rotated", save_path)


horz_data=all_ports["P1"]["AZ T0 CO"]["amplitude"]
vert_data=all_ports["P1"]["EL T0 CO"]["amplitude"]

def export_to_planet(all_ports,header,fname="test",path):
    
    #Function to convert file
    def convert_data_to_str(data):
        string=""
        a=0.0
        
        for i in data:
            string += str(a) + " " + str(round(i,1)) + "\n" 
            a+=1.0
            
        return string
        
    #Header
    header_final=("NAME "+header["NAME"]+"\n"
    "MAKE Alpha Wireless Ltd\n"
    "FREQUENCY "+header["FREQUENCY"]+"\n"
    "H_WIDTH "+ header["H_WIDTH"]+"\n"
    "V_WIDTH "+ header["V_WIDTH"]+"\n"
    "GAIN "+header["GAIN"]+"\n"
    "TILT ELECTRICAL\n"
    )
    
    #Horizontal
    horz_header = "HORIZONTAL  360\n"
    horz_final=horz_header+convert_data_to_str(abs(horz_data))
    
    #Vertical
    vert_header = "VERTICAL  360\n"
    vert_final=vert_header+convert_data_to_str(abs(vert_data))
    
    final_planet= header_final + horz_final + vert_final
    
    f = open(path+fname+".planet.txt",'w')
    f.write(final_planet)
    f.close()
