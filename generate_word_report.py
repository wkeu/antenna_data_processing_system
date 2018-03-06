# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 14:25:13 2018

@author: Matt Slevin
"""
from docx import Document
from docx.shared import Inches
import pandas as pd
import os

def panda_to_word_table(doc,df,measurment_type="El tilt devation",spec="",style="Light List Accent 1"):
    
    # Function to write excel speadsheet to word table
    #Formatting of panda dataframe
    df = df.rename(index=str, columns={"index": "Frequency"})
        
    ###############################################################################
    # Data table (1), just copy all the data of the panda. Port names, frequency ect.
    ###############################################################################
    # add a table to the end and create a reference variable
    # extra row is so we can add the header row
    t = doc.add_table(df.shape[0], df.shape[1]+2)
    t.style =style
    
    # add the header rows.
    for j in range(2,df.shape[-1]+2):
        t.cell(0,j).text = df.columns[j-2]
    
    # add the rest of the data frame
    for i in range(1,df.shape[0]):
        for j in range(df.shape[-1]):
            t.cell(i,j+2).text = str(df.values[i,j])
    
    ###############################################################################
    # Info Table I (2), Item and spec
    ###############################################################################
    t.cell(0,0).text="Item"
    t.cell(1,0).text=measurment_type
    
    #Merge cells
    a = t.cell(1, 0)
    b = t.cell(df.shape[0]-1,0)#
    a.merge(b)
    
    t.cell(0,1).text="Spec"
    t.cell(1,1).text=spec
    
    #Merge cells
    a = t.cell(1, 1)
    b = t.cell(df.shape[0]-1,1)#
    a.merge(b)
    
    ###############################################################################
    # Info Table II (3), mean, max, min, pass
    ###############################################################################
    
    df = df.set_index('Frequency')
    
    t = doc.add_table(4, 2)
    t.style = style
    
    cell = t.cell(0, 0)
    cell.text = 'Mean'
    mean=df.values.mean()
    t.cell(0, 1).text=str(round(mean,2))
    
    cell = t.cell(1, 0)
    cell.text = 'Max'
    t.cell(1, 1).text=str(df.values.max())
    
    cell = t.cell(2, 0)
    cell.text = 'Min'
    t.cell(2, 1).text=str(df.values.min())
    
    cell = t.cell(3, 0)
    cell.text = 'Pass'
    
#Function to place images into report
def insert_cart_plots(doc,images_dir_path):

    file_list=list()
    
    doc.add_heading("Plots", level=1)
    
    #Create a list of all image files
    for path, subdirs, files in os.walk(images_dir_path):
           for filename in files:
             f = os.path.join(path, filename)
             file_list.append(str(f)) 
    
    #Put Image into document
    for picture in file_list:
        #heading
        name=picture.split("\\")[-1]
        name=name.split(".")[0]
        
        doc.add_heading(name, level=2)
        doc.add_picture(picture,width=Inches(6.6))

def insert_radiation_tables(doc,master_table_path):

    #Open excel document
    xl = pd.ExcelFile(master_table_path)
    #Load in all sheet names
    sheet_names = xl.sheet_names
    
    for sheet_name in sheet_names:
        doc.add_heading(sheet_name, level=2)
        df = xl.parse(sheet_name)
        panda_to_word_table(doc,df,measurment_type=sheet_name,spec="")    

###############################################################################
#
# Main
#
###############################################################################        

def generate_report(antenna_model="AWXXXX"):
    dir_path=os.getcwd()
    master_table_path=dir_path + "\\processed_data\\master_table.xlsx"
    images_dir_path=dir_path + "\\processed_data\\images\\CART"
    save_path=dir_path + "\\processed_data\\"+antenna_model+"report.docx"
    
    # Open a new document
    doc = Document()
    doc.add_heading('Antenna Report', 0)
    
    #Add the plots
    insert_cart_plots(doc,images_dir_path)
    
    doc.add_heading("Radiation Tables", level=1)
    
    insert_radiation_tables(doc,master_table_path)
    
    # save the doc
    doc.save(save_path)
    print("Report for antenna " + antenna_model + " generated.")


