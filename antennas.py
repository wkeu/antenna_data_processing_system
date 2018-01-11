
########################################################################################################################
#
# Libraries Used
#
########################################################################################################################

import numpy as np
import pandas as pd
from scipy.signal import savgol_filter
from peakdetect import peakdetect

########################################################################################################################
#
# Parent Class
#
########################################################################################################################

class Masterantenna:
    "Common base class for all antennas"

    #Global Variables
    BORESIGHT = 180         # Specify boresight angle. Not selection of Boresight
                            # should be an interger in the range 0-360
    USL_SEARCH_RANGE = 20   # Specify range frm Main lobe to search for USL

    def __init__(self, name):
        self.name = name

    def test_function(self):
        print("Test Function is working")

    ##############################
    # Functions used by subclasses
    ##############################

    def normalise(self):
        #TODO
        print("To be Implemented")

    def normalise2(self):
        # TODO
        print("To be Implemented")

    def find_az_peak(self):
        #Not sure if this function is ever used.
        # TODO
        print("To be Implemented")

    def find_nearest(array, value):
        idx = (np.abs(array - value)).argmin()
        return idx

    # "Stretch" the axis to have xfactor more datapoints
    def stretch_axis(x, y, factor):
        # create a new angle axis with smaller increment size
        x_strch = np.linspace(0, len(x) - len(x) / (len(x) * factor), factor * len(x))

        # interpolate ("stretch") the y_axis to match x_axis.
        y_strch = np.interp(x_strch, x, y)
        return x_strch, y_strch

    #############################
    # Results table function + Plots
    #############################

    def results_co(self):
        # TODO
        print("To be Implemented")

    def results_cr(self):
        # TODO
        print("To be Implemented")

    def results_final(self):
        # TODO
        print("To be Implemented")

    def generate_plots(self):
        #Generate all plots for all measurements
        #TODO
        print("To be Implemented")

########################################################################################################################
#
# Child Class
#
########################################################################################################################

#Sector Antenna Class
class Sector(Masterantenna):
    def __init__(self, name):
        self.name = name

    def test_function(self):
        print("Test Function is working")

    #########
    # Azimuth
    #########

    #########
    # Elevation
    #########

    #########
    # Both
    #########

#Omnidirectional Antenna Class
class Omnidirectional(Masterantenna):
    def __init__(self, name):
        self.name = name

    def test_function(self):
        print("Test Function is working")

    #########
    # Azmuth
    #########

    #########
    # Elevation
    #########

#Twin Peak Antenna Class
class Twin(Masterantenna):
    def __init__(self, name):
        self.name = name

    def test_function(self):
        print("Test Function is working")

########################################################################################################################
#
# Template Class: Copy and paste this code to add a new type of antenna
#
########################################################################################################################

class Template(Masterantenna):

