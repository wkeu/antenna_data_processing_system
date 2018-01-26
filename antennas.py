
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
    USL_SEARCH_RANGE = 45   # Specify range frm Main lobe to search for USL
    FBR_RANGE = 30  # define +/- range to check for FBR

    def __init__(self, name):
        self.name = name

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

    def get_tilt(self,fname):
        # Function to extract the tilt from fname
        global tilt_angle
        a = fname.split()

        for b in a:
            if "T" in b:
                _, tilt_angle = b.split("T")

        return float(tilt_angle)
    
        # Function to find the peaks of a wave

    def get_peaks(self,wave, factor=100):

        # Convert to numpy matrix with dtype float
        wave_np = np.asarray(wave, dtype='float64')

        # Stretch the Axis
        angle, amp = self.stretch_axis(np.arange(0, len(wave_np)), wave_np, factor)

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
    
    def calc_usl_in_range(self,wave, Boresight=False):

        #TODO:Refactor angle range
        angle_range=self.USL_SEARCH_RANGE
        # Find the peaks and troughs
        df_peaks, _ = self.get_peaks(wave)

        # find peak amp,angle and index
        _, peak_amp = df_peaks.max()
        _, peak_idx = df_peaks.idxmax()
        peak_angle = df_peaks["angle"][peak_idx]

        # For using boresight instead of peak angle
        if Boresight:
            peak_angle = self.BORESIGHT

        # Remove all values not in range
        df_peaks = df_peaks[(df_peaks.angle < peak_angle) & (df_peaks.angle > peak_angle - angle_range)]

        # find the peak of largest side lobe in range
        _, peak_sl_amp = df_peaks.max()

        # if a peak has been detected
        #TODO: This dosnt work properly for the angle. Problem is that it is pulling out the peak angle
        if not (df_peaks.empty):
            usl_angle_idx = df_peaks["amp"].idxmax()
            usl_peak_angle = float(df_peaks["angle"].loc[[usl_angle_idx]])

            # Peak_s1 and peak are the same
            if(peak_amp==peak_sl_amp):
                #Get the next largest peak
                _,peak_sl_amp=df_peaks["amp"].nlargest(n=2, keep='first')
                usl=peak_amp - peak_sl_amp
                
            else:    
                usl = peak_amp - peak_sl_amp

        # TODO: Make this a bit more sophisticated. Its a bit hacky
        # No peak detected
        else:
            print("Warning: failed to find usl in range ....")
            print("search_range_is:" + str(angle_range))
            usl_peak_angle = peak_angle - angle_range
            usl = peak_amp - wave[int(usl_peak_angle)]

        return usl, usl_peak_angle


    # Calulate the 1st USL in a given frequency range
    def cal_first_usl(self,wave):

        # Find the peaks and troughs
        df_peaks, _ = self.get_peaks(wave)

        # Find index of peak
        idx_max = df_peaks.idxmax()

        # find amp of peak and 1st usl
        amp_of_peak = df_peaks["amp"][idx_max["amp"]]
        amp_of_1stlobe = df_peaks["amp"][idx_max["amp"] - 1]
        fst_usl_angle = df_peaks["angle"][idx_max["amp"] - 1]
        first_usl = amp_of_peak - amp_of_1stlobe

        return first_usl, fst_usl_angle
    
    def cal_squint(self,lowwer_angle, upper_angle):
        # function to calculate squint. Inputs are 3db intersection points
    
        # Allow for overflow
        if upper_angle < lowwer_angle:
            upper_angle += 360
    
        midpoint = (lowwer_angle + upper_angle) / 2.0
        # this is our ideal value
        squint = abs(midpoint - self.BORESIGHT)
    
        return squint, midpoint % 360

    def cal_3db_bw(self,lowwer_angle, upper_angle):
        # Allow for overflow
        if upper_angle < lowwer_angle:
            upper_angle += 360

        bw_3db = abs(lowwer_angle - upper_angle)
        # this is our ideal value
        return bw_3db
    
    # Function to find the 3db intersection points of a wave
    def find_3db_intersection_angles(self,wave_str):

        # Convert into correct format
        wave = wave_str.convert_objects(convert_numeric=True)

        # Find the peak of the wave
        peak_amp = wave.max()
        peak_angle = wave.idxmax()

        # Interpolate both axis
        factor = 100
        angle, amp = self.stretch_axis(np.arange(0, 360), wave.as_matrix(), factor)

        # section into left and right
        peak_idx = self.find_nearest(angle, peak_angle)

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
        left_intxn = self.find_nearest(wave_left, peak_amp - 3)  # 3 because 3db
        right_intxn = self.find_nearest(wave_right, peak_amp - 3)

        return angle[left_intxn], angle[right_intxn]
    
    # function to calculate squint. Inputs are 3db intersection points
    def cal_tilt_dev(self,r_int, l_int, ant_tilt):
        midpoint = (r_int + l_int) / 2.0
        tilt = (self.BORESIGHT + ant_tilt)  # this is our ideal value
        deviation = abs(midpoint - tilt)

        return deviation, midpoint


    def cal_peak_dev(self, wave, ant_tilt):

        #Convert to file format
        wave = wave.convert_objects(convert_numeric=True)
                
        # Find the peak of the wave
        pk_angle = wave.idxmax()
        
        tilt = (self.BORESIGHT + ant_tilt)  # this is our ideal value
        deviation = abs(pk_angle - tilt)

        return deviation, pk_angle
    
########################################################################################################################
#
# Child Class
#
########################################################################################################################

#Sector Antenna Class
class Sector(Masterantenna):
    def __init__(self, name):
        self.name = name

    ###########################################################################
    #   Results table
    ###########################################################################
    #Results table for azimuth 
    def results_table_az(self,az_co,az_cr):
        #Convert to numeric pd          
        az_co = az_co.convert_objects(convert_numeric=True)
        az_cr = az_cr.convert_objects(convert_numeric=True)

        #Calculate
        xpol_at_sector = self.find_xpol(az_co,az_cr)    
        fbr = self.find_front_to_back(az_co)                            
        az_bw_3db = self.find_3db_bw(az_co,"Az Co 3db BW")
        squint= self.find_squint(az_co)
        
        #Put into a dataframe
        results = pd.DataFrame()
        results = pd.concat([az_bw_3db,squint,xpol_at_sector,fbr],axis = 1)
        
        return results
    
    #Results table for elevation 
    def results_table_el(self,el_co,fname="EL TX"):
        #Convert to numeric pd    
        el_co = el_co.convert_objects(convert_numeric=True)
        
        #Calculate
        el_bw_3db = self.find_3db_bw(el_co,"3db BW "+fname)
        first_usl= self.find_first_usl(el_co,"first_usl "+fname)
        usl_range = self.find_usl_in_range(el_co,measurement_type="usl_range "+fname)
        usl_range_bs = self.find_usl_in_range(el_co, measurement_type="usl_range bs"+fname, Boresight=True)
        peak_dev = self.find_peak_dev(el_co,'Peak dev'+fname,fname)
        tilt_dev = self.find_tilt_dev(el_co,'Tilt dev'+fname,fname)    
        
        #Put into a dataframe
        results = pd.DataFrame()
        results = pd.concat([el_bw_3db,first_usl,usl_range,usl_range_bs,peak_dev,tilt_dev],axis = 1)
        
        return results

    ###########################################################################
    # Azmuth
    ###########################################################################
    def find_xpol(self,co, cr):
        xpol_at_sector = co.iloc[self.BORESIGHT] - cr.iloc[self.BORESIGHT]  # co at sector - cr at sector
        xpol_at_sector = xpol_at_sector.to_frame()
        xpol_at_sector.columns = ['X Pol at sector']
        return xpol_at_sector

    def find_front_to_back(self,co):

        # define sector angle
        back_sight1 = self.BORESIGHT - 180  # define the backsight(back of antenna). eg 0 & 360 degrees
        back_sight2 = self.BORESIGHT + 180
        
        fbr_search1 = back_sight1 + (self.FBR_RANGE + 1)  # this is search range 1 eg 0 - 30 degrees
        fbr_search2 = back_sight2 - (self.FBR_RANGE + 1)  # this is search range 2 eg 30 - 360 degrees

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


    # Function to find the 3db beamwidths for a given graph
    def find_3db_bw(self,az_co, measurement_type="3db Beamwidth"):

        # Collect keys
        key_list = az_co.keys()
        # Initalise list
        bw_3db = list()

        # Cycle through each frequency column
        for i in key_list:
            # Work with each column individually
            lowwer_angle, upper_angle = self.find_3db_intersection_angles(az_co[i])
            bw_3db.append(self.cal_3db_bw(lowwer_angle, upper_angle))

        # Format into a data frame
        bw_3db_pd = pd.DataFrame({measurement_type: bw_3db, "index": key_list})
        bw_3db_pd = bw_3db_pd.set_index('index')

        return bw_3db_pd

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
            lowwer_angle, upper_angle = self.find_3db_intersection_angles(az_co[i])
            # Culculate squint
            x, y = self.cal_squint(lowwer_angle, upper_angle)
            sqt.append(x)
            midpoint.append(y)

        sqt_pd = pd.DataFrame({"Squint of 3dB Midpoint": sqt, "@ Angle": midpoint, "index": key_list})
        sqt_pd = sqt_pd.reindex(columns=["Squint of 3dB Midpoint", "@ Angle", "index"])
        sqt_pd = sqt_pd.set_index('index')
        return sqt_pd

    def peak_squint(self,az_co):
        peak_pos = az_co.idxmax()

        peak_squint = abs(peak_pos - self.BORESIGHT)
        peak_squint = pd.concat([peak_squint, peak_pos], axis=1)
        peak_squint.columns = (['Squint of Peak', '@ Angle'])

        return peak_squint

    ###############################################################################
    #
    #   Tilt Deviation of 3dB midpoint calculation
    #
    ###############################################################################

    def find_tilt_dev(self,el_co, measurement_type, fname):
        # Collect keys
        key_list = el_co.keys()
        # Initalise list
        dev = list()
        midpoint = list()
        ant_tilt = self.get_tilt(fname)
        # Cycle through each frequency column
        for i in key_list:
            # Work with each column individually
            lowwer_angle, upper_angle = self.find_3db_intersection_angles(el_co[i])
            # Culculate squint
            x, y = self.cal_tilt_dev(lowwer_angle, upper_angle, ant_tilt)
            dev.append(x)
            midpoint.append(y)

        dev_pd = pd.DataFrame({measurement_type: dev, "@ Angle": midpoint, "index": key_list})
        dev_pd = dev_pd.reindex(columns=[measurement_type, "@ Angle", "index"])
        dev_pd = dev_pd.set_index('index')
        return dev_pd

    def find_peak_dev(self, el_co, measurement_type, fname):
        # Collect keys
        key_list = el_co.keys()
        # Initalise list
        peak_dev = list()
        theoretical_peak = list()

        ant_tilt = self.get_tilt(fname)
        
        # Cycle through each frequency column
        for i in key_list:

            deviation, pk_angle = self.cal_peak_dev( el_co[i], ant_tilt)
            peak_dev.append(deviation)
            theoretical_peak.append(pk_angle)

        #Put into a dataframe
        peak_dev_pd = pd.DataFrame({
                measurement_type: peak_dev,
                "@ Angle pk_dev_angle": pk_angle, 
                "index": key_list})
    
        #dev_pd = dev_pd.reindex(columns=[measurement_type, "@ Angle", "index"])
        peak_dev_pd = peak_dev_pd.set_index('index')
        
        return peak_dev_pd

    ###############################################################################
    #
    # Calculate first USL from Main lobe
    #
    ###############################################################################

    # Calulate the 1st USL for a table
    def find_first_usl(self,el_co, measurement_type):
        # Convert the data so that it is stored in a more appropriate format
        el_co = el_co.convert_objects(convert_numeric=True)

        # Take column index into array
        key_list = el_co.keys()
        first_usl = list()
        first_usl_angle = list()

        for i in key_list:
            # Add usl to list for given column
            usl, angle = self.cal_first_usl(el_co[i])
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

    # Calulate the USL for a table with a given angle range
    def find_usl_in_range(self,el_co, measurement_type, Boresight=False):

        # Convert the data so that it is stored in a more appropriate format
        el_co = el_co.convert_objects(convert_numeric=True)

        # Take column index into array
        key_list = el_co.keys()
        usl_in_range = list()
        usl_angle_in_range = list()

        for i in key_list:
            # Add usl to list for given column
            usl, usl_angle = self.calc_usl_in_range(el_co[i],  Boresight)
            usl_in_range.append(usl)
            usl_angle_in_range.append(usl_angle)

        # Format into a dataframe
        usl_pd = pd.DataFrame({measurement_type: usl_in_range, "@ Angle": usl_angle_in_range, "index": key_list})
        usl_pd = usl_pd.set_index('index')

        return usl_pd



###############################################################################
#
#
#
###############################################################################
# Omnidirectional Antenna Class
class Omnidirectional(Masterantenna):
    def __init__(self, name):
        self.name = name

    def test_function(self):
        print("Test Function is working")

    ###########################################################################
    #   Results table
    ###########################################################################
    #Results table for azimuth 
    def results_table_az(self,az_co,az_cr):
        #Convert to numeric pd          
        az_co = az_co.convert_objects(convert_numeric=True)
        az_cr = az_cr.convert_objects(convert_numeric=True)

        #Calculate 
        cross_pol =  self.find_xpol(az_co,az_cr)
        ripple =     self.find_ripple(az_co)
        
        #Put into a dataframe
        results = pd.DataFrame()
        results = pd.concat([cross_pol,ripple],axis = 1)
        
        return results
    
    #Results table for elevation 
    def results_table_el(self,el_co,fname="EL TX"):
        #Convert to numeric pd    
        el_co = el_co.convert_objects(convert_numeric=True)
        
        #Calculate
        find_3db_bw = self.find_3db_bw(el_co, measurement_type="3db BW "+fname)
        first_usl= self.find_first_usl(el_co,"first_usl "+fname)
        usl_in_range= self.find_usl_in_range(el_co,"range_usl "+fname)
        usl_in_range_bs= self.find_usl_in_range(el_co,"range_usl_bs "+fname,Boresight=True)  
        tilt_dev = self.find_tilt_dev(el_co, 'Tilt dev'+fname,fname)
        peak_dev = self.find_peak_dev(el_co, 'Peak dev'+fname,fname)
        
        #Put into a dataframe
        results = pd.DataFrame()
        results = pd.concat([
                find_3db_bw,
                first_usl,
                usl_in_range,
                usl_in_range_bs,
                tilt_dev,
                peak_dev],axis = 1)
        
        return results

    #
    # Azimuth Calculation 
    #
    
    def find_ripple(self,az_co, measurement_type="Ripple"):
        # Function to find the 3db beamwidths for a given graph
        # Collect keys
        key_list = az_co.keys()

        # Initalise list
        ripple = list()

        # Cycle through each frequency column
        for i in key_list:
            # Work with each column individually
            ripple.append(self.cal_ripple(az_co[i]))

        # Format into a data frame
        ripple_pd = pd.DataFrame({measurement_type: ripple, "index": key_list})
        ripple_pd = ripple_pd.set_index('index')

        return ripple_pd

    def cal_ripple(self,wave_str):
        peaks, troughs = self.get_peaks(wave_str)

        wave_max = peaks["amp"].max()
        wave_min = troughs["amp"].min()

        ripple = abs(wave_max - wave_min)

        return ripple
    
    def find_xpol(self,az_co,az_cr):
        diff=az_co-az_cr

        cross_pol_max=diff.min()
        cross_pol_mean=diff.mean()

        cross_pol=pd.DataFrame({"X Pol (max)":cross_pol_max,"X Pol (mean)":cross_pol_mean})
        
        return cross_pol
    
    #
    # Elevation Calculation 
    #
    
    def split_wave(self,wave):
    #Function to isolate certain sections of an omni wave
        wave_np=np.asarray(wave)
        
        #Peak at full circle
        first_pk=np.concatenate((  wave_np[0:90]  ,  np.full(180,wave_np.min())  ,  wave_np[270:360]  ))
        #Centre Peak
        centre_pk=np.concatenate((  np.full(90,wave_np.min())  ,  wave_np[90:270]  ,  np.full(90,wave_np.min())  ))
        
        #First wave centred and flipped
        first_pk_flipped=np.concatenate((  np.full(90,wave_np.min())  ,  wave_np[270:360] ,  wave_np[0:90] ,  np.full(90,wave_np.min())  ))
        first_pk_flipped=np.fliplr([first_pk_flipped])[0]
        
        #Convert into a series datafram
        first_pk=pd.Series(first_pk)
        centre_pk=pd.Series(centre_pk)
        first_pk_flipped=pd.Series(first_pk_flipped)
        
        return first_pk, centre_pk, first_pk_flipped
    
    def find_3db_bw(self,az_co, measurement_type="3db Beamwidth"):

        # Collect keys
        key_list = az_co.keys()
        # Initalise list
        bw_3db_first_pk = list()
        bw_3db_centre_pk = list()
        

        # Cycle through each wave/frequency column
        for i in key_list:
            #Isolate both peaks
            first_pk,centre_pk,_ = self.split_wave(az_co[i])
        
            #First peak
            lowwer_angle, upper_angle = self.find_3db_intersection_angles(first_pk)
            bw_3db_first_pk.append(self.cal_3db_bw(lowwer_angle, upper_angle))            
            
            #Centre Peak
            lowwer_angle, upper_angle = self.find_3db_intersection_angles(centre_pk)
            bw_3db_centre_pk.append(self.cal_3db_bw(lowwer_angle, upper_angle))  

        # Format into a data frame
        bw_3db_pd = pd.DataFrame({
                measurement_type+" first pk": bw_3db_first_pk,
                measurement_type+" centre pk": bw_3db_centre_pk, 
                "index": key_list})
        bw_3db_pd = bw_3db_pd.set_index('index')

        return bw_3db_pd
    
    def find_first_usl(self,el_co, measurement_type):
        # Calulate the 1st USL 
        
        # Convert the data so that it is stored in a more appropriate format
        el_co = el_co.convert_objects(convert_numeric=True)

        # Take column index into array
        key_list = el_co.keys()

        first_usl_first_pk = list()
        first_usl_first_pk_angle = list()        
        first_usl_centre_peak = list()
        first_usl_centre_pk_angle = list()        

        for i in key_list:
            #Isolate both peaks waves
            _,centre_pk,first_pk_rvd = self.split_wave(el_co[i])
            
            #First Peak
            usl, angle = self.cal_first_usl(first_pk_rvd)
            angle=abs(first_pk_rvd.idxmax()-angle) #To Correct for flipping and centering
            first_usl_first_pk.append(usl)
            first_usl_first_pk_angle.append(angle)
            
            #Centre
            usl, angle = self.cal_first_usl(centre_pk)
            first_usl_centre_peak.append(usl)
            first_usl_centre_pk_angle.append(angle)

        # Format to panda
        first_usl_pd = pd.DataFrame({
                measurement_type+" first pk": first_usl_first_pk, 
                "@ Angle f_pk": first_usl_first_pk_angle, 
                measurement_type+" centre pk": first_usl_centre_peak, 
                "@ Angle c_pk": first_usl_centre_pk_angle,
                "index": key_list})
        first_usl_pd = first_usl_pd.set_index('index')

        return first_usl_pd
    
    # Calulate the USL for a table with a given angle range
    def find_usl_in_range(self,el_co, measurement_type, Boresight=False):

        # Convert the data so that it is stored in a more appropriate format
        el_co = el_co.convert_objects(convert_numeric=True)

        # Take column index into array
        key_list = el_co.keys()

        #List for values        
        range_usl_first_pk = list()
        range_usl_first_pk_angle = list()        
        range_usl_centre_peak = list()
        range_usl_centre_pk_angle = list()      

        for i in key_list:
            
            #Isolate both peaks waves
            _,centre_pk,first_pk_rvd = self.split_wave(el_co[i])
            
            #First Peak
            usl, angle = self.calc_usl_in_range(first_pk_rvd, Boresight)
            angle=abs(first_pk_rvd.idxmax()-angle) #To Correct for flipping and centering
            range_usl_first_pk.append(usl)
            range_usl_first_pk_angle.append(angle)
            
            #Centre
            usl, angle = self.calc_usl_in_range(centre_pk, Boresight)
            range_usl_centre_peak.append(usl)
            range_usl_centre_pk_angle.append(angle)

        # Format to panda
        range_usl_pd = pd.DataFrame({
                measurement_type+" first pk": range_usl_first_pk, 
                "@ Angle f_pk": range_usl_first_pk_angle, 
                measurement_type+" centre pk": range_usl_centre_peak, 
                "@ Angle c_pk": range_usl_centre_pk_angle,
                "index": key_list})
        range_usl_pd = range_usl_pd.set_index('index')

        return range_usl_pd
     
    def find_tilt_dev(self,el_co, measurement_type, fname):
    
        # Collect keys
        key_list = el_co.keys()
        
        # Initalise list
        dev_first_pk = list()
        midpoint_first_pk = list()
        dev_centre_pk = list()
        midpoint_centre_pk = list()
        
        #Get the tilt
        ant_tilt = self.get_tilt(fname)
        
        # Cycle through each frequency column
        for i in key_list:
            
            #Isolate both peaks waves
            first_pk,centre_pk,first_pk_rvd = self.split_wave(el_co[i])
            
            # First Peak
            lowwer_angle, upper_angle = self.find_3db_intersection_angles(first_pk_rvd)
            x, y = self.cal_tilt_dev(lowwer_angle, upper_angle, ant_tilt)
            dev_first_pk.append(x)
            midpoint_first_pk.append(y)
    
            # Centre Peak
            lowwer_angle, upper_angle = self.find_3db_intersection_angles(centre_pk)
            x, y = self.cal_tilt_dev(lowwer_angle, upper_angle, ant_tilt)
            dev_centre_pk.append(x)
            midpoint_centre_pk.append(y)
            
        # Format to panda data frame
        dev_pd = pd.DataFrame({
                measurement_type+" first pk": dev_first_pk, 
                "@ Angle f_pk": midpoint_first_pk, 
                measurement_type+" centre pk": dev_centre_pk, 
                "@ Angle c_pk": midpoint_centre_pk, 
                "index": key_list})
        
        #dev_pd = dev_pd.reindex(columns=[measurement_type, "@ Angle", "index"])
        dev_pd = dev_pd.set_index('index')
        return dev_pd
    
    def find_peak_dev(self,el_co, measurement_type, fname):
    
        # Collect keys
        key_list = el_co.keys()
        
        # Initalise list
        first_peak_dev = list()
        actual_first_peak = list()
        centre_peak_dev = list()
        actual_centre_peak = list()

        #Get the tilt
        ant_tilt = self.get_tilt(fname)
        
        # Cycle through each frequency column
        for i in key_list:
            
            #Isolate both peaks waves
            first_pk,centre_pk,first_pk_rvd = self.split_wave(el_co[i])
            
            # First Peak
            deviation, pk_angle = self.cal_peak_dev( first_pk_rvd, ant_tilt)
            first_peak_dev.append(deviation)
            actual_first_peak.append(pk_angle)
            
            # Centre Peak
            deviation, pk_angle = self.cal_peak_dev( centre_pk, ant_tilt)
            centre_peak_dev.append(deviation)
            actual_centre_peak.append(pk_angle)
                        
        # Format to panda data frame
        dev_pd = pd.DataFrame({
                measurement_type+" first pk": first_peak_dev, 
                "@ Angle f_pk": actual_first_peak, 
                measurement_type+" centre pk": centre_peak_dev, 
                "@ Angle c_pk": actual_centre_peak, 
                "index": key_list})
        
        #dev_pd = dev_pd.reindex(columns=[measurement_type, "@ Angle", "index"])
        dev_pd = dev_pd.set_index('index')
        return dev_pd


#################################################################################################################
#
# For a later date
#
#################################################################################################################

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

#TODO: Create a tri sector omni hybrid 
