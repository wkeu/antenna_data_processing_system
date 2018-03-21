from generate_data import * 

#read in the data
all_ports=read_in_data_all_ports(    sub_dir     )
save_dir= "\\processed_data\\patterns\\planet\\"
save_path=os.getcwd()+save_dir

for PN in all_ports:
    #isolate horizontal and vertical data
    horz_data_all=all_ports[PN]["AZ T0 CO"]["amplitude"]
    vert_data_all=all_ports[PN]["EL T0 CO"]["amplitude"]
    
    #Convert data to planent string format
    def convert_data_to_str(data):
        string=""
        a=0.0
        
        for i in data:
            string += str(a) + " " + str(round(i,1)) + "\n" 
            a+=1.0
            
        return string
    
    test_ant=Sector("test") #Initialize an antenna object 
    
    i=0
    
    for freq in horz_data_all:
        horz_data = horz_data_all[freq].convert_objects(convert_numeric=True)
        vert_data = vert_data_all[freq].convert_objects(convert_numeric=True)
        
        #Normalise
        horz_data_norm, _ =test_ant.normalise2(horz_data,horz_data)
        vert_data_norm, _ =test_ant.normalise2(vert_data,vert_data)
            
        #Header
        header_final=("NAME "+antenna_model+"\n"
        "MAKE Alpha Wireless Ltd\n"
        "FREQUENCY "+freq+"\n"
        "H_WIDTH " + str(int(results_per_port[i]["Az Co 3db BW"][freq])) +"\n"
        "V_WIDTH "+ str(int(results_per_port[i]["3db BW EL T0 CO"][freq]))  +"\n"
        "FRONT_TO_BACK "+ str(int(results_per_port[i]["Front to Back Ratio"][freq])) +"\n"
        "GAIN xx.xxdBi\n"
        "TILT ELECTRICAL\n"
        )
        
        #Horizontal
        horz_header = "HORIZONTAL  360\n"
        horz_final=horz_header+convert_data_to_str(abs(horz_data_norm))
        
        #Vertical
        vert_header = "VERTICAL  360\n"
        vert_final=vert_header+convert_data_to_str(abs(vert_data_norm))
        
        final_planet= header_final + horz_final + vert_final
        
        f = open(save_path+antenna_model+"_"+PN+"_"+str(freq.split(".")[0])+'.planet.txt','w')
        f.write(final_planet)
        f.close()
    
    i+=1
