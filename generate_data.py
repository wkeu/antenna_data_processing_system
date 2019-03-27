###############################################################################
#
#   Import Libraries
#
###############################################################################

#Custom functions & Scripts
from file_merge import read_in_data_all_ports
from antennas import *
from antenna_plots import *
from generate_word_report import *
import gain
#from generate_pattern_files import *

#Standard libraries
import pandas as pd
import os
import sys
import warnings
import shutil
warnings.simplefilter(action='ignore', category=FutureWarning) #Removes Warnings 

#Settings for the program

#Specify the type of antenna. Options are "omni","sector","twin_peak"
antenna_type="sector"

###############################################################################
# Decide on the antenna type
###############################################################################

class Generate_data:

    #def generate_data():
    def __init__ (self, source_dir, save_path, antenna_type, Images, Report, Pattern_Files,Gain, gain_ref_model):
        
        #Set values of the class   
        self.source_dir = source_dir
        self.save_path = save_path
        self.antenna_type = antenna_type
        self.Images = Images
        self.Report = Report
        self.Pattern_Files = Pattern_Files 
        self.Gain = Gain
        self.gain_ref_model = gain_ref_model
        self.save_folder=self.save_path+"/processed data/"
        self.antenna_model=source_dir.split("/")[-1]
    
    def run(self):
        #import data
        #Alternatively we can use sub dir=\\raw_data\\
        
        #clear processed data folder of all data
        #TODO: Setup clear_data to work in a specific sub directory 
        self.clear_processed_data()
        
        #TODO: Set input to read in all ports to be source dir
        all_ports=read_in_data_all_ports(    self.source_dir + "/raw_data/"    )
        
        
        rotate_angle= 0#degrees, note ensure that this is a postivie angle 
                 #this angle rotates back
                 
        all_ports = self.rotate_all_ports(all_ports,rotate_angle) 
        
        #Determine Antenna Type
        #TODO Re-factor so that the functions are more consistent
        self.determine_ant_type()
    
        results_per_port=dict()
           
        #Generate table per port
        for port_name in all_ports:    
            print("Starting "+  port_name  +"....")
            results_per_port[port_name]=(self.calulated_based_per_port(all_ports[port_name],port_name,self.save_path))
            print("Finished "+  port_name)
        
        print("Result per port:")
        self.generate_master_table(results_per_port,self.save_path)
        
        #TODO: Put images generating functions here.So that its more readable
        if self.Images == True:
            print("Generating Images")
        
        if self.Gain == True:
            print("Generating Gain")        
            #Run the gain calculations
            gain.gain_main(self.save_folder,
                           self.source_dir,
                           self.gain_ref_model)
            
        if self.Pattern_Files == True:
            print("Generating a Pattern Files")
            print(self.Pattern_Files)
           #generate_pattern_files(all_ports,results_per_port,antenna_model)

                
        if self.Report == True:
            print("Generating a report")
            print(self.save_folder)
            generate_report(self.save_folder,self.antenna_model)
        
        print("o.O.o")
    
    
    def determine_ant_type(self):
        #Create test antenna object
        if(self.antenna_type=="Omnidirectional"):
            self.test_ant=Omnidirectional("test_ant")
            print("Omni antenna selected")
            
        elif(self.antenna_type=="Sector"):
            self.test_ant=Sector("test_ant")
            print("Sector antenna selected")
        
        elif(self.antenna_type=="twin_peak"):
            self.test_ant=Twin("test_ant")
            print("Twin peak antenna selected")
        
        else:    
            print("Error:Invalid Antenna type")
            sys.exit(0)

    ###############################################################################    

    #function to clear the processed data folder and set up new directory (with subdir)    
    def clear_processed_data(self):

        #Clear Folder
        if not os.path.isdir(self.save_folder):
            os.mkdir(self.save_folder)
        
        shutil.rmtree(self.save_folder,ignore_errors=True)
        
        #TODO: Re-factor this function
        #Set up patterns sub dir
        directory = self.save_folder+"/patterns/"
        
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        folders = ['planet','ant','atoll','msi']
        
        for folder in folders:
            os.mkdir(os.path.join(directory,folder))  
    
        #Set up images sub dir 
        directory = self.save_folder+"/images/"
        
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        folders = ['HTML','CART','POLAR','GAIN']
        
        for folder in folders:
            os.mkdir(os.path.join(directory,folder))  
    
    ###############################################################################
    #
    #   Results table (per_port)
    #
    ###############################################################################
    #Merge AZ and EL into one results table. And final formatting
    def results_final(self,final_results_table,port_name,save_dir): 
        
        #Add average min and max
        final_results_table.loc['Average'] = final_results_table.mean()                                             #add row named average to table calulating average of each column
        final_results_table.loc['Max'] = final_results_table.max()                                                  #add row named max to table calulating max of each column
        final_results_table.loc['Min'] = final_results_table.min()                                                  #add row named min to table calulating min of each column
        
        #Round all the values to 2 significant figures
        final_results_table=final_results_table.round(2)
        
        #Save to a file
        final_results_table.to_csv( self.save_folder + "/" + port_name+" results.csv" )                                                    # Function to output results of calc to table
        
        return final_results_table
   
    
    def az_ascii_file_gen(az_res,port_name,save_dir):
       
        az_res.to_csv(self.save_folder + "/" + port_name+" ascii.csv")
        
        return az_res
    ###############################################################################
    # Function which returns the names of the Azimuth measurements. It is assumed 
    # that there will only be one co and one cross measurement. 
    def find_az_co_cr(self,PN):
    
        #If co and cross are not detected then return false for the strings.
        co_str=False
        cr_str=False
        
        #Loop for 
        for i in PN:    
        
            #Check if it is a A
            if (i.split(" ")[0]=="AZ"):
                
                if (i.split(" ")[2]=="CR"):
                    cr_str=i
                    
                else:
                    co_str=i
        
        return co_str,cr_str 

    ###############################################################################
    #Function to check if a structure is empty
    def is_empty(self,any_structure):
        if any_structure:
            return False
        else:
            return True
    ###############################################################################

    #TODO:  Some serious refactoring is needed in this function if time permits. It is
    #       quite busy
    
    # Plot can definitely be removed into a function, it wont reduce the lines of 
    # but it will make it more readable
    
    # Add functionality to results_table_az so it can deal without any cross
    
    # Separate into detection, plot, generate results table
    
    def calulated_based_per_port(self,P1,port_name,save_dir):
        P1=dict(P1) #Keep this! Ensures a copy was made.
            
        ###############################################################################
        # Azimuth (Calculations and Plots)
        ###############################################################################
        
        
        #Do Azimuth Calculations first, removing them from P1 in the process
        az_co_str, az_cr_str = self.find_az_co_cr(P1)
        
        #Co and Cross not detected
        if (az_co_str == False) and (az_cr_str == False):
            print ("Notification: AZ_CO and AZ_CR were not detected.")
        
        #Only Co detected
        elif ( isinstance(az_co_str,str)) and (az_cr_str == False):
            print ("Notification: Only AZ_CO was detected.")
            
            az_co=P1.pop(az_co_str)
            az_co=az_co["amplitude"]
            az_cr=az_co #Ensures results table runs
            
            #Generates results table
            az_results_table=self.test_ant.results_table_az(az_co,az_cr)
           
        #Both Cr and Co detected
        else:
            print ("Notification: AZ Co and Cross detected.")
            az_co=P1.pop(az_co_str)
            az_cr=P1.pop(az_cr_str)
            
            az_co=az_co["amplitude"]
            az_cr=az_cr["amplitude"]
            
            #Generates results table
            az_results_table=self.test_ant.results_table_az(az_co,az_cr)
        
        #Plots
        if (self.Images and isinstance(az_co_str,str)):
            plot_norm_cart(  az_co,az_cr  ,  fname=port_name , save_dir=self.save_folder+"/images/CART/")
            plot_norm_polar(  az_co,az_cr  , fname=port_name+" Polar", save_dir=self.save_folder+"/images/POLAR/" )
            plot_norm_cart_interacive_az(  az_co,az_cr  ,  fname=port_name +" AZ ", save_dir=self.save_folder+"/images/HTML/")
			
        ###########################################################################
        # Elevation (Calculations and Plots) 
        ###########################################################################
        
        #list to store tables    
        list_of_rt=list()
        
        #Generate plots and results per el_co file
        for file in P1:
            #Isolate the file
            el_co= P1[file]["amplitude"]
            list_of_rt.append(self.test_ant.results_table_el(el_co,file))
            
            #Plots
            if(self.Images):
                plot_norm_cart(  el_co,el_co  , fname=port_name , save_dir=self.save_folder+"/images/CART/" )#+ " " +file
                plot_norm_polar( el_co,el_co  , fname=port_name + " " +file+" Polar", save_dir=self.save_folder+"/images/POLAR/" )
                plot_norm_cart_interacive_el(  el_co, fname=port_name + " " +file+" EL Cart", save_dir=self.save_folder+"/images/HTML/")
        
        #Put into one table
        if self.is_empty(not(list_of_rt)):
            el_results_table=pd.concat(list_of_rt,axis=1)
        
        ###############################################################################
        # Merge into final results table
        ###############################################################################
        
        #Both
        if isinstance(az_co_str,str) and self.is_empty(not(list_of_rt)) :
            merged_table=pd.concat([az_results_table,el_results_table],axis=1)
    
        #Only AZ
        elif(isinstance(az_co_str,str)):
            merged_table=az_results_table
    
        #Only EL
        else:
            merged_table=el_results_table
    
        final_results_table=self.results_final(merged_table, port_name,save_dir)
        
        return final_results_table
    

    
    ###############################################################################
    #
    # Master Results table Generation 
    #
    ###############################################################################
        
    #TODO: Maybe move the results table generation to a separate file. 
        
    #Get a clean list of all measurements. 
    def get_list_of_measurements(self,results_per_port):
        
        port_keys=list(results_per_port.keys())
        P1=results_per_port[port_keys[0]]
    
        key_list=list(P1.keys())
    
        #Clean up keys list. Remove all @ Angle
        while "@ Angle c_pk" in key_list:
            key_list.remove("@ Angle c_pk")
    
        while "@ Angle f_pk" in key_list:
            key_list.remove("@ Angle f_pk")
    
        while "@ Angle" in key_list:
            key_list.remove("@ Angle")
            
        return key_list
    
    ###############################################################################

    #Function to generate a table for a summary table for a given item. 
    def generate_table_per_item(self,results_per_port,item):
        #Ported from old code
        item_per_port=list()
              
        for i in results_per_port:
            #Read in data
            p1=i
        
            #Drop Avg, Max and Min
            p1 = results_per_port[i]#.drop(['Average', 'Max','Min'])
        
            #Isolate column from port file
            p1_item=p1[item]
            p1_item=p1_item.rename( i )
            
            #Append to a list
            item_per_port.append(p1_item)
        
        #Create the sub_table
        sub_table=pd.DataFrame(item_per_port)
        sub_table= sub_table.T
    
        #Create one table
        final_table = pd.concat([sub_table],axis=1)
        
        return final_table
    
    #Function to generate a master table 
    def generate_master_table(self,results_per_port,save_path):
        
       
        #Get a clean list of results
        measurements_lst = self.get_list_of_measurements(results_per_port)
        list(range(0,len(measurements_lst)))
        
        final_tables=list()
        
        #
        for item in measurements_lst:
    
            final_tables.append(  self.generate_table_per_item(results_per_port,item)  )
            
        #Save to an excel sheet
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(self.save_folder+'/master_table.xlsx', engine='xlsxwriter')
    
        for i in range(0,len(final_tables)):
            # Write each dataframe to a different worksheet.
            final_tables[i].to_excel(writer, sheet_name=measurements_lst[i])
            
        writer.save()
        
    def save_ascii(self,az_res,save_path):
            
        writer = pd.ExcelWriter(self.save_folder+'ascii.xlsx', engine='xlsxwriter')
        writer.save()
        
        
        
        
    def rotate_all_ports(self,all_ports,rotate_angle=0):

        if rotate_angle==0:
            all_ports_rotated=all_ports
            
        else:            
            all_ports_rotated=all_ports.copy()
            
            #Port
            for port in all_ports:
                
                #Measurement
                for measurement in all_ports[port]:
                
                    #Rotate Panda
                    pd_waves = all_ports[port][measurement]["amplitude"]
                    pd_waves_rotated=self.rotate_panda(pd_waves, rotate_angle)
                    all_ports_rotated[port][measurement]["amplitude"]=pd_waves_rotated
        
        return all_ports_rotated

    
    def rotate_panda(self,pd_waves, rotate_angle):
        
        #Transpose to make easier to dice and splice
        
        a=pd_waves[0:rotate_angle]
        b=pd_waves[rotate_angle:len(pd_waves)]
        
        frames=[b,a]
        result = pd.concat(frames)
        result = result.reset_index()
        result = result.drop(['index'], axis=1)
        
        return result