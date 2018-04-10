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

*install anaconda 3.6.4 (Windows 64 Bit)(https://anaconda.org/anaconda/python/3.6.4/download/win-64/python-3.6.4-h0c2934d_3.tar.bz2)

custom packages to install to enviroment(pip install):
* mpld3==0.3
* python-docx==0.8.6

*Note: You will need to adjust Kronus.bat so that it points to the correct directory. 

### Video Tutorial 
[![Installation Instructions](https://img.youtube.com/vi/T-D1KVIuvjA/0.jpg)](http://www.youtube.com/watch?v=T-D1KVIuvjA)

## Demo
-------


## Adding new class of Antenna  
------------------------------

## System Discription 
--------------------
* gui: Frontend. Allow for user to launch and configure program. Launch from here.
* generate data: Essentially main, from 
* antennas: Contains all classes of antennas and how each calculation is perfored for each antenna. Eg. 3dbw for a sector. 
* antenna plots: Contains all functions for plotting (Polar, Cartisian, Interactive)
* file merge: Contains all functions for reading in the 
* generate pattern files:
* generate word report:
* peak detect:
* Khronos.bat:
