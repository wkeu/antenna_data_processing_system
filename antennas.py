
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
    BORESIGHT = 180         # Specify boresight angle. Not selection of Boresight ( # should be an interger in the range 0-360)
    USL_SEARCH_RANGE = 20   # Specify range frm Main lobe to search for USL

    def __init__(self, name):
        self.name = name

    def test_function(self):
        print("Test Function is working")

    ##############################
    # Functions used by subclasses
    ##############################
    #TODO: Evaluate weather or not we use this function for anything.
    def find_az_peak(self,co, cr):  # Function to find peak of azimuth
        az_peak_amp = co.max()  # find peak valie in each column
        az_peak_pos = co.idxmax()  # find index no of peak value
        az_peak = pd.concat([az_peak_amp, az_peak_pos], axis=1)  # join az_peak_amp & az peak_pos
        az_peak = pd.concat([az_peak_amp, az_peak_pos], axis=1)  # join az_peak_amp & az peak_pos
        az_peak.columns = ['amplitude', 'angle']
        return az_peak

    ###############################################################################
    #
    #   normalise co & cr together
    #
    ###############################################################################
    # TODO: Evaluate wheather or not we need to have a normalise2 function
    def normalise(self,co, cr):
        az_peak_amp = co.max()
        normalise_co = co - az_peak_amp
        normalise_cr = cr - az_peak_amp
        normalised_az = pd.concat([normalise_co, normalise_cr], axis=1)
        return normalised_az

    # TODO: Merge Normalize and Normailse two into one function.
    def normalise2(self, co, cr):
        # Function needed for plotting. Returns two results rather than one.
        az_peak_amp = co.max()
        normalise_co = co - az_peak_amp
        normalise_cr = cr - az_peak_amp

        return normalise_co, normalise_cr

    def find_nearest(self,array, value):
        # Function to find the index of the nearest value in an array
        idx = (np.abs(array - value)).argmin()
        return idx

    def stretch_axis(self,x, y, factor):
        # "Stretch" the axis to have xfactor more datapoints
        # create a new angle axis with smaller increment size
        x_strch = np.linspace(0, len(x) - len(x) / (len(x) * factor), factor * len(x))

        # interpolate ("stretch") the y_axis to match x_axis.
        y_strch = np.interp(x_strch, x, y)
        return x_strch, y_strch

    # TODO: Add support for detecting the number of peaks. (For case when we have twin-peak in amp plot). This a unique feature and thus a low priority

    def find_tilt(self,fname):
        # Function to extract the tilt from fname
        global tilt_angle
        a = fname.split()

        for b in a:
            if "T" in b:
                _, tilt_angle = b.split("T")

        return float(tilt_angle)

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
    # Azmuth
    #########
    def sector_xpol(self,co, cr):
        xpol_at_sector = co.iloc[BORESIGHT] - cr.iloc[BORESIGHT]  # co at sector - cr at sector
        xpol_at_sector = xpol_at_sector.to_frame()
        xpol_at_sector.columns = ['X Pol at sector']
        return xpol_at_sector

    def front_to_back(self,co):

        # define sector angle
        back_sight1 = BORESIGHT - 180  # define the backsight(back of antenna). eg 0 & 360 degrees
        back_sight2 = BORESIGHT + 180
        fbr_range = 30  # define +/- range to check for FBR

        fbr_search1 = back_sight1 + (fbr_range + 1)  # this is search range 1 eg 0 - 30 degrees
        fbr_search2 = back_sight2 - (fbr_range + 1)  # this is search range 2 eg 30 - 360 degrees

        fbr1, _, fbr2 = np.split(co, [fbr_search1, fbr_search2], axis=0)  # Split Co dataframe into 3 segements

        fbr_max = pd.concat([fbr1, fbr2], axis=0)  # join fbr1 & fbr2

        # Output#
        az_peak_amp = co.max()

        fbr = az_peak_amp - fbr_max.max()
        fbr_pos = fbr_max.idxmax()
        fbr = pd.concat([fbr, fbr_pos], axis=1)

        fbr.columns = ['Front to Back Ratio', '@ Angle']
        return fbr

    #########
    # Elevation
    #########

    #########
    # Both
    ##########
    # Function to find the 3db intersection points of a wave
    def find_3db_intersection_angles(self,wave_str):

        # Convert into correct format
        wave = wave_str.convert_objects(convert_numeric=True)

        # Find the peak of the wave
        peak_amp = wave.max()
        peak_angle = wave.idxmax()

        # Interpolate both axis
        factor = 100
        angle, amp = stretch_axis(np.arange(0, 360), wave.as_matrix(), factor)

        # section into left and right
        peak_idx = find_nearest(angle, peak_angle)

        # Isolate left and right hand side. Based on the location of the peak
        # TODO: Make this into a function
        if angle[peak_idx] > 180:
            # Change all values outside of range to greater that zero
            wave_left = np.copy(amp)
            wave_left[0:int(peak_idx - (len(angle) / 2))] = 0.0
            wave_left[int(peak_idx):int(peak_idx + (len(angle) / 2))] = 0.0

            # Isolate the rest of the wave using masking
            wave_right = np.copy(amp)
            wave_right[int(peak_idx - (len(angle) / 2)):int(peak_idx)] = 0.0

            if np.count_nonzero(wave_right) != np.count_nonzero(wave_left):
                print("3db intersection angle is not splitting equally")

        else:
            # Change all values outside of range to greater that zero
            wave_right = np.copy(amp)
            wave_right[0:int(peak_idx)] = 0.0
            wave_right[int(peak_idx + (len(angle) / 2)):len(angle)] = 0.0

            # Isolate the rest of the wave using masking
            wave_left = np.copy(amp)
            wave_left[int(peak_idx):int(peak_idx + len(angle) / 2)] = 0.0

            if np.count_nonzero(wave_right) != np.count_nonzero(wave_left):
                print("3db intersection angle is not splitting equally")

                # Find left and right intersection
        left_intxn = find_nearest(wave_left, peak_amp - 3)  # 3 because 3db
        right_intxn = find_nearest(wave_right, peak_amp - 3)

        return angle[left_intxn], angle[right_intxn]

    # Function to find the 3db beamwidths for a given graph
    def find_3db_bw(self,az_co, measurement_type="3db Beamwidth"):

        # Collect keys
        key_list = az_co.keys()
        # Initalise list
        bw_3db = list()

        # Cycle through each frequency column
        for i in key_list:
            # Work with each column individually
            lowwer_angle, upper_angle = find_3db_intersection_angles(az_co[i])
            bw_3db.append(cal_3db_bw(lowwer_angle, upper_angle))

        # Format into a data frame
        bw_3db_pd = pd.DataFrame({measurement_type: bw_3db, "index": key_list})
        bw_3db_pd = bw_3db_pd.set_index('index')

        return bw_3db_pd

    def cal_3db_bw(self,lowwer_angle, upper_angle):
        # Allow for overflow
        if upper_angle < lowwer_angle:
            upper_angle += 360

        bw_3db = abs(lowwer_angle - upper_angle)
        # this is our ideal value
        return bw_3db

    ###########################
    # Squint
    ###########################
    def find_squint(self,az_co):
        # Collect keys
        key_list = az_co.keys()
        # Initalise list
        sqt = list()
        midpoint = list()

        # Cycle through each frequency column
        for i in key_list:
            # Work with each column individually
            lowwer_angle, upper_angle = find_3db_intersection_angles(az_co[i])
            # Culculate squint
            x, y = cal_squint(lowwer_angle, upper_angle)
            sqt.append(x)
            midpoint.append(y)

        sqt_pd = pd.DataFrame({"Squint of 3dB Midpoint": sqt, "@ Angle": midpoint, "index": key_list})
        sqt_pd = sqt_pd.reindex(columns=["Squint of 3dB Midpoint", "@ Angle", "index"])
        sqt_pd = sqt_pd.set_index('index')
        return sqt_pd

    def cal_squint(self,lowwer_angle, upper_angle):
        # function to calculate squint. Inputs are 3db intersection points

        # Allow for overflow
        if upper_angle < lowwer_angle:
            upper_angle += 360

        midpoint = (lowwer_angle + upper_angle) / 2.0
        # this is our ideal value
        squint = abs(midpoint - BORESIGHT)

        return squint, midpoint % 360

    def peak_squint(self,az_co):
        az_peak = az_co.max()
        peak_pos = az_co.idxmax()
        peak = pd.concat([az_peak, peak_pos], axis=1)

        peak_squint = abs(peak_pos - BORESIGHT)
        peak_squint = pd.concat([peak_squint, peak_pos], axis=1)
        peak_squint.columns = (['Squint of Peak', '@ Angle'])

        return peak_squint

        def peak_tilt_dev(el_co, measurement_type, fname):
            ant_tilt = find_tilt(fname)
            el_peak = el_co.max()
            peak_pos = el_co.idxmax()
            peak = pd.concat([el_peak, peak_pos], axis=1)

            peak_tilt_deviation = abs(peak_pos - (ant_tilt + BORESIGHT))
            peak_tilt_deviation = pd.concat([peak_tilt_deviation, peak_pos], axis=1)
            peak_tilt_deviation.columns = ([measurement_type, '@ Angle'])

            return peak_tilt_deviation

        ###############################################################################
        #
        #   Tilt Deviation of 3dB midpoint calculation
        #
        ###############################################################################

        def find_tilt_dev(el_co, measurement_type, fname):
            # Collect keys
            key_list = el_co.keys()
            # Initalise list
            dev = list()
            midpoint = list()
            ant_tilt = find_tilt(fname)
            # Cycle through each frequency column
            for i in key_list:
                # Work with each column individually
                lowwer_angle, upper_angle = find_3db_intersection_angles(el_co[i])
                # Culculate squint
                x, y = cal_dev(lowwer_angle, upper_angle, ant_tilt)
                dev.append(x)
                midpoint.append(y)

            dev_pd = pd.DataFrame({measurement_type: dev, "@ Angle": midpoint, "index": key_list})
            dev_pd = dev_pd.reindex(columns=[measurement_type, "@ Angle", "index"])
            dev_pd = dev_pd.set_index('index')
            return dev_pd

        # function to calculate squint. Inputs are 3db intersection points
        def cal_dev(r_int, l_int, ant_tilt):
            midpoint = (r_int + l_int) / 2.0
            tilt = (BORESIGHT + ant_tilt)  # this is our ideal value
            deviation = abs(midpoint - tilt)

            return deviation, midpoint

        ###############################################################################
        #
        # Calculate first USL from Main lobe
        #
        ###############################################################################

        # Function to find the peaks of a wave
        def find_peaks(wave, factor=100):

            # Convert to numpy matrix with dtype float
            wave_np = np.asarray(wave, dtype='float64')

            # Stretch the Axis
            angle, amp = stretch_axis(np.arange(0, 360), wave_np, factor)

            # Smooth the signal
            amp_smooth = savgol_filter(amp, 75, 3)

            # Find the peaks and troughs in wave
            peaks, troughs = peakdetect(amp_smooth, lookahead=300)

            # Put into dataframe
            df_peaks = pd.DataFrame(data=peaks, columns=["angle", "amp"])
            df_trough = pd.DataFrame(data=troughs, columns=["angle", "amp"])

            # Convert index into angle
            df_peaks.angle = df_peaks.angle / factor
            df_trough.angle = df_trough.angle / factor

            return df_peaks, df_trough

        # Calulate the 1st USL for a given frequency
        def cal_first_usl(wave):

            # Find the peaks and troughs
            df_peaks, _ = find_peaks(wave)

            # Find index of peak
            idx_max = df_peaks.idxmax()

            # find amp of peak and 1st usl
            amp_of_peak = df_peaks["amp"][idx_max["amp"]]
            amp_of_1stlobe = df_peaks["amp"][idx_max["amp"] - 1]
            fst_usl_angle = df_peaks["angle"][idx_max["amp"] - 1]
            first_usl = amp_of_peak - amp_of_1stlobe

            return first_usl, fst_usl_angle

        # Calulate the 1st USL for a table
        def find_first_usl(el_co, measurement_type):
            # Convert the data so that it is stored in a more appropriate format
            el_co = el_co.convert_objects(convert_numeric=True)

            # Take column index into array
            key_list = el_co.keys()
            first_usl = list()
            first_usl_angle = list()

            for i in key_list:
                # Add usl to list for given column
                usl, angle = cal_first_usl(el_co[i])
                first_usl.append(usl)
                first_usl_angle.append(angle)

            # Format to panda
            first_usl_pd = pd.DataFrame({measurement_type: first_usl, "@ Angle": first_usl_angle, "index": key_list})
            first_usl_pd = first_usl_pd.set_index('index')

            return first_usl_pd

        ###############################################################################
        #
        #   Max USL from Main lobe in Range
        #
        ###############################################################################

        # TODO:   Add support for wrap around. (ie if we go into a ngative number) the
        #        problem arises if we have a peak that is not centred at around 180
        #        degrees

        # Finds the difference in amplitude between largest side lobe and peaks over a
        # certain frequency range. By default 180 degrees away from the peak.
        def calc_usl_in_range(wave, angle_range=USL_SEARCH_RANGE, Boresight=False):

            # Find the peaks and troughs
            df_peaks, _ = find_peaks(wave)

            # find peak amp,angle and index
            _, peak_amp = df_peaks.max()
            _, peak_idx = df_peaks.idxmax()
            peak_angle = df_peaks["angle"][peak_idx]

            # For using boresight instead of peak angle
            if Boresight:
                peak_angle = BORESIGHT

            # Remove all values not in range
            df_peaks = df_peaks[(df_peaks.angle < peak_angle) & (df_peaks.angle > peak_angle - angle_range)]

            # find the peak of largest side lobe in range
            _, peak_sl_amp = df_peaks.max()

            # if a peak has been detected
            if not (df_peaks.empty):
                usl_angle_idx = df_peaks["amp"].idxmax()
                usl_peak_angle = float(df_peaks["angle"].loc[[usl_angle_idx]])

                # difference in amp
                usl = peak_amp - peak_sl_amp

            # TODO: Make this a bit more sophisticated. Its a bit hacky
            # No peak detected
            else:
                print("Warning: failed to find usl in range ....")
                print("search_range_is:" + str(angle_range))
                usl_peak_angle = peak_angle - angle_range
                usl = peak_amp - wave[int(usl_peak_angle)]

            return usl, usl_peak_angle

        # Calulate the USL for a table with a given angle range
        def find_usl_in_range(el_co, measurement_type, angle_range=20, Boresight=False):

            # TODO, Set up if boresight=True

            # Convert the data so that it is stored in a more appropriate format
            el_co = el_co.convert_objects(convert_numeric=True)

            # Take column index into array
            key_list = el_co.keys()
            usl_in_range = list()
            usl_angle_in_range = list()

            for i in key_list:
                # Add usl to list for given column
                usl, usl_angle = calc_usl_in_range(el_co[i], angle_range, Boresight)
                usl_in_range.append(usl)
                usl_angle_in_range.append(usl_angle)

            # Format into a dataframe
            usl_pd = pd.DataFrame({measurement_type: usl_in_range, "@ Angle": usl_angle_in_range, "index": key_list})
            usl_pd = usl_pd.set_index('index')

            return usl_pd

#################################################################################################################
#
# For a later date
#
#################################################################################################################


# Omnidirectional Antenna Class
class Omnidirectional(Masterantenna):
    def __init__(self, name):
        self.name = name

    def test_function(self):
        print("Test Function is working")

    def find_ripple(az_co, measurement_type="Ripple"):
        # Function to find the 3db beamwidths for a given graph
        # Collect keys
        key_list = az_co.keys()

        # Initalise list
        ripple = list()

        # Cycle through each frequency column
        for i in key_list:
            # Work with each column individually
            ripple.append(cal_ripple(az_co[i]))

        # Format into a data frame
        ripple_pd = pd.DataFrame({measurement_type: ripple, "index": key_list})
        ripple_pd = ripple_pd.set_index('index')

        return ripple_pd

    def cal_ripple(wave_str):
        peaks, troughs = find_peaks(wave_str)

        wave_max = peaks["amp"].max()
        wave_min = troughs["amp"].min()

        ripple = abs(wave_max - wave_min)

        return ripple


#Twin Peak Antenna Class
class Twin(Masterantenna):
    def __init__(self, name):
        self.name = name

    def test_function(self):
        print("Test Function is working")

class Template(Masterantenna):
    #Template Class: Copy and paste this code to add a new type of antenna
    def __init__(self, name):
        self.name = name

    def test_function(self):
        print("Test Function is working")

