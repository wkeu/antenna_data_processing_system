"""
Function to generate patterns. This is not yet finished but nearly all the 
functionality is there it just needs to be hooked up. 


Functions to convert horizontal data and vertical data into planet,msi,atoll 
and .ant formats.

"""

###############################################################################
    #
    # planet
    #
###############################################################################

def export_to_planet(horz_data,vert_data,header,fname="test",path):
    
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

###############################################################################
    #
    # msi
    #
###############################################################################

def export_to_msi(horz_data,vert_data,header,fname="test",path):
    
    #Function to convert file
    def convert_data_to_str(data):
        string=""
        a=0.0
        
        for i in data:
            string += str(a) + "\t" + str(round(i,1)) + "\n" 
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
    
    f = open(path+fname+".msi",'w')
    f.write(final_planet)
    f.close()

###############################################################################
    #
    # Atolll
    #
###############################################################################
def export_to_atoll(horz_data,vert_data,header,fname="test",path):

    #Convert data to planent string format
    def convert_data_to_str(data):
        string=""
        a=0
        
        for i in data:
            string += str(a) + " " + str(round(i,1)) +" "
            a+=1 
            
        return string
       

    #Header
    header_final=("Name;Gain (dBi);Manufacturer;Comments;Pattern;Pattern Electrical Tilt (°);BeamWidth;FMin;FMax;Frequency;V_WIDTH;Tilt;H_WIDTH;FAMILY;DIMENSIONS HxWxD(INCHES);Weight (LBS)\n"
    +header["NAME"]+";"+header["GAIN"].split("dBi")[0]+";Alpha Wireless;;2 0 0 360 " )
    
    #Footer
    footer_final="0;0;57;;;"+header["FREQUENCY"]+";7;41;;57;;;"
    
    middle = "1 0 360 "
    
    #Horizontal
    horz_final=convert_data_to_str(abs(horz_data))
    
    #Vertical
    vert_final=convert_data_to_str(abs(vert_data))
    
    final_atoll= header_final + horz_final + middle + vert_final + footer_final
    
    f = open(path+fname+".Atoll.Txt",'w')
    f.write(final_atoll)
    f.close()

###############################################################################
    #
    # ant
    #
###############################################################################

def export_to_ant(horz_data,vert_data,header,fname="test",path):

    #Convert data to planent string format
    def convert_data_to_str(data):
        string=""
        
        for i in data:
            string += str(round(i,1)) + "\n" 
        
        return string
    
    #Horizontal
    horz_final=convert_data_to_str(abs(horz_data))
    
    #Vertical
    vert_final=convert_data_to_str(abs(vert_data))
    
    #Construct Final String 
    final_ant = horz_final + vert_final 
    final_ant = final_ant.rstrip('\n')
    
    f = open(path+fname+'.ant','w')
    f.write(final_ant)
    f.close()



# TODO: Finish this function 
def generate_pattern_files(all_ports,model,save_dir):

    model = "AWXXXX"
    header=dict()
    header["NAME"]=model
    header["FREQUENCY"]=" "
    header["H_WIDTH"]=" "
    header["V_WIDTH"]=" "
    header["GAIN"]=" "

    save_dir= "C:\\Users\\Matt Slevin\\Desktop\\processed data\\patterns\\planet"

    horz_data=all_ports["P1"]["AZ T0 CO"]["amplitude"]
    vert_data=all_ports["P1"]["EL T0 CO"]["amplitude"]

