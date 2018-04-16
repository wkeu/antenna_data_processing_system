# Antenna Data Processing System
---------------------------------
Package for the generation of antenna test reports using Python. Input patterns include Azimuth Co, Azimuth Cr and Elevation Co. Automatically generates microsoft word report which includes summary tables of measurments and pictures of the pattern files. Additionally it generates standard antenna pattern files (Planet, Atoll, MSI and Ant). 

### Metrics Calculated
* 3dB Beam Width 
* Cross Pol
* Front to Back ratio
* First Upper Sidelobe
* Squint
* Peak Devation
* Gain (Working Progress)

### Supported Antennas 
* Omnidirectional
* Sector

This allowed for the interactive visualisation of antenna specification. Additionally a dramatic improvement in throughput and quality of the test results was attained. 

## Installation instructions
---------------------------

*install anaconda 3.6.4 (Windows 64 Bit)(https://www.anaconda.com/download/)

custom packages to install to enviroment(pip install):
* mpld3==0.3
* python-docx==0.8.6

*Note: You will need to adjust Kronus.bat so that it points to the correct directory. 

### Video Tutorial 
[![Installation Instructions](http://img.youtube.com/vi/Ossz98FQkOA/maxresdefault.jpg )](https://youtu.be/rOvK_EEp3lo?list=PL9XiBq5tluqR__rTCCEkhs2Nn9olB-A-Q)

## Demo
-------
[![Demo](http://img.youtube.com/vi/Ossz98FQkOA/maxresdefault.jpg )](https://youtu.be/48oUes7xsiM?list=PL9XiBq5tluqR__rTCCEkhs2Nn9olB-A-Q)

Video demonstrating how to operate program. 

## Adding new class of Antenna  
------------------------------
[![New Class of Antenna](http://img.youtube.com/vi/Ossz98FQkOA/maxresdefault.jpg )](https://youtu.be/rOvK_EEp3lo?list=PL9XiBq5tluqR__rTCCEkhs2Nn9olB-A-Q)

### Steps:
* gui: Add antenna type to antenna options in the GUI. 
* generate_data: Change determine_ant_type() function to account for this new anntenna. 
* antennas: Add a new class of antenna to the system. This will contain all the functions for the calculations on a particular measurement. It is reccomended to look at object orientated programming with Python tutorails before doing this. It is also advisable to look at the other anntennas (Sector and Omni) which have been implemented as they will provide a good template. 


## Adding Gain Antenna
------------------------------
[![Gain Antenna](http://img.youtube.com/vi/Ossz98FQkOA/maxresdefault.jpg )](https://youtu.be/rWX__yiAm18?list=PL9XiBq5tluqR__rTCCEkhs2Nn9olB-A-Q)

### Steps:
* gui: Add new antenna gain model to GAIN_OPTIONS list.
* antenna_raw_data\golden_ref_gain\gain_standards_golden_refrence: Add new known gain data to a new sheet on the excel spreadsheet. 

## System Discription 
--------------------
[![System Overview](http://img.youtube.com/vi/Ossz98FQkOA/maxresdefault.jpg )](https://youtu.be/Ossz98FQkOA?list=PL9XiBq5tluqR__rTCCEkhs2Nn9olB-A-Q)

* gui: Frontend. Allow for user to launch and configure program. Launch from here.
* generate data: Essentially main, where all scripts are launched. Heart of the program.  
* antennas: Contains all classes of antennas and how each calculation is perfored for each antenna. Eg. 3dbw for a sector. 
* antenna plots: Contains all functions for plotting (Polar, Cartisian, Interactive)
* file merge: Contains all functions for reading in the data. Used for everything bar gain.
* file merge2: Contains all functions for reading in data for gain caluclations. 
* gain: Used to calculate the gain.
* generate pattern files: Functions for generation of pattern files
* generate word report: Functions for the generation of a word report.
* peak detect: Used to detect the peaks of patterns. Important for USL in range calcualtions.
* Khronos.bat: Bat file for lauching program without the need for use of Spyder. 
