"""
Basic Gui, allows for the 
"""

from tkinter import *
from tkinter import filedialog
import webbrowser
from generate_data import Generate_data
import os 

class Startscreen:

    #TODO: Set up directory to be independent of any user
    source_dir=os.getcwd() + "\\antenna_raw_data\\sector_data\\IR468_V2"
    save_path= os.getcwd() 

    # Function for initializing object
    def __init__(self, master):

        # TODO: Refactor each area into sections. Tidies up code

        #########################################
        # Initialize
        #########################################
        frame = Frame(master)
        frame.grid()
        frame.winfo_toplevel().title("AW Khronos")
        #frame.configure(bg="#3c3f41") #Add background color for debugging

        #########################################
        # Specify Directories
        #########################################
        # Source
        self.label_1 = Label(frame, text="Source Dir:")
        self.label_1.grid(row=0, column=0,sticky=W+E, padx=(10,10),pady=(20,0))

        self.source_dir_label = Label(frame, text=self.source_dir, bg="white", anchor=W)
        self.source_dir_label.grid(row=0, column=1, sticky=W + E, padx=(0, 10), pady=(20, 0))

        self.SourceButton = Button(frame, text="...", command=self.update_source_dir)
        self.SourceButton.grid(row=0, column=2,padx=(0,10),pady=(20,0))

        # Destination
        self.label_3 = Label(frame, text="Destination Dir:" )
        self.label_3.grid(row=1, column=0, sticky=W,padx=(10,10))

        self.dest_dir_label = Label(frame, text=self.save_path, bg="white", anchor=W)
        self.dest_dir_label.grid(row=1, column=1, sticky=W + E, padx=(0, 10))

        self.SourceButton = Button(frame, text="...", command=self.update_dest_dir)
        self.SourceButton.grid(row=1, column=2,padx=(0,10))

        #########################################
        # Type of antenna list
        #########################################

        self.label_5 = Label(frame, text="Antenna Type:")
        self.label_5.grid(row=2, column=0,sticky=E+W,padx=(10,10),pady=(10,10))

        OPTIONS = [
            "Sector",
            "Omnidirectional",
            
        ]  # etc

        self.antenna_type = StringVar(frame)
        self.antenna_type.set(OPTIONS[0])  # default value

        w = OptionMenu(frame, self.antenna_type, *OPTIONS)
        w.grid(row=2,column=1,sticky=W+E,padx=(0,10))

        #########################################
        # Options
        #########################################

        self.Images = BooleanVar()
        C1 = Checkbutton(frame, text="Images", variable=self.Images, \
                         onvalue=True, offvalue=False, height=1, \
                         width=20, anchor=W)
        C1.select()  # Leave turned on
        C1.grid(row=3,column=1,sticky=W+E,padx=(0,10))

        self.Report = BooleanVar()
        C2 = Checkbutton(frame, text="Report", variable=self.Report, \
                         onvalue=True, offvalue=False, height=1, \
                         width=20, anchor=W)
        C2.select()  # Leave turned on
        C2.grid(row=4,column=1,sticky=W+E,padx=(0,10))

        self.Pattern_Files = BooleanVar()
        C3 = Checkbutton(frame, text="Pattern Files", variable=self.Pattern_Files, \
                         onvalue=True, offvalue=False, height=1, \
                         width=20, anchor=W )
        C3.select() #Leave turned on
        C3.grid(row=5,column=1,sticky=W+E,padx=(0,10))

        self.Gain = BooleanVar()
        C3 = Checkbutton(frame, text="Gain", variable=self.Gain, \
                         onvalue=True, offvalue=False, height=1, \
                         width=20, anchor=W )
        C3.select() #Leave turned on
        C3.grid(row=6,column=1,sticky=W+E,padx=(0,10))
        #########################################
        # TODO: Settings Menu (Boresight, USL_SEARCH_RANGE, etc.)
        #########################################
        
        self.label_gain_ref = Label(frame, text="Ref Ant Model:")
        self.label_gain_ref.grid(row=7, column=0,sticky=E+W,padx=(10,10),pady=(10,10))
        
        GAIN_OPTIONS = [
            "FR6509",
            "AW3023",
            "Satimo LB"
        ]  # etc

        self.gain_ref_model = StringVar(frame)
        self.gain_ref_model.set(GAIN_OPTIONS[0])  # default value

        x = OptionMenu(frame, self.gain_ref_model, *GAIN_OPTIONS)
        x.grid(row=7,column=1,sticky=W+E,padx=(0,10))

        #########################################
        # Generate
        #########################################
        self.ComputeButton = Button(frame, text="Generate", bg="#00FF00", command=self.run_program)
        self.ComputeButton.config(relief=SUNKEN)
        self.ComputeButton.grid(row=8,column=1,sticky=E,padx=(0,10),pady=(20,10))

        self.HelpButton = Button(frame, text="Help", command=self.help_button)
        self.HelpButton.grid(row=9,column=1,sticky=E,padx=(0,10),pady=(0,10))

    ##########################################
    # Class Functions
    ##########################################

    # TODO: Refactor these two functions into one. They are very similar
    def update_source_dir(self):
        filedir = filedialog.askdirectory()
        print(filedir)
        self.source_dir=filedir
        self.source_dir_label.config(text=filedir)

    def update_dest_dir(self):
        filedir = filedialog.askdirectory()
        print(filedir)
        self.save_path=filedir
        self.dest_dir_label.config(text=filedir)

    def run_program(self):
        print("running generate data")
        #Create a Generate data
        prog = Generate_data( source_dir = self.source_dir ,
                       save_path = self.save_path,
                       antenna_type = self.antenna_type.get(),
                       Images = self.Images.get(),
                       Report = self.Report.get(),
                       Pattern_Files = self.Pattern_Files.get(),
                       Gain = self.Gain.get(),
                       gain_ref_model = self.gain_ref_model.get()
                       )
        
        self.test()

        #Run generate data
        prog.run()

    #For Debug, print info
    def test(self):
        print("\n\n\n")
        print("Source Dir: \n"+self.source_dir)
        print("Destination Dir:\n" + self.save_path)
        print("Antenna Type: " + self.antenna_type.get())
        print("Images: "+str(self.Images.get()))
        print("Report: "+str(self.Report.get()))
        print("Pattern Files: "+str(self.Pattern_Files.get()))
        print("Gain Ref Model: " + self.gain_ref_model.get())

    def help_button(self):
        url = 'https://github.com/wkeu/antenna_data_processing_system#antenna-data-processing-system'
        webbrowser.open_new(url)

# Main window
root = Tk()
b = Startscreen(root)
# Display on the screen
root.mainloop()