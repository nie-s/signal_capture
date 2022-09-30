import numpy as np
import math


class HRV_Calculator():
    def __init__(self):
        self.measures = {}
        self.result = {}

    def rolmean(self, dataset, hrw, fs):
        mov_avg = dataset['hart'].rolling(int(hrw * fs)).mean()  # calculate moving average
        avg_hr = (np.mean(dataset['hart']))
        mov_avg = [avg_hr if math.isnan(x) else x for x in mov_avg]
        mov_avg = [x * 1.2 for x in mov_avg]  # and *20%
        dataset['hart_rollingmean'] = mov_avg  # append the moving average to the dataframe

    def detect_peaks(self, dataset):
        # mark regions of interest
        window = []
        peaklist = []
        listpos = 0  # use a counter to move over the different data columns
        for datapoint in dataset.hart:
            rollingmean = dataset.hart_rollingmean[listpos]  # get local mean
            if (datapoint < rollingmean) and (len(window) < 1):  # if theres no detectable -> do nothing
                listpos += 1
            elif (datapoint > rollingmean) and (len(window) < 1):  # if the signal comes above local mean -> mark ROI
                window.append(datapoint)
                listpos += 1
            elif (len(window) >= 1):  # if the signal drops below local mean -> determine highest point
                maximum = max(window)
                beatposition = listpos - len(window) + (
                    window.index(max(window)))  # note the position of the high point on the X-axis
                peaklist.append(beatposition)  # add the detected peak high point to list
                window = []  # clear the marked ROI
                listpos += 1
        self.measures['peaklist'] = peaklist
        self.measures['ybeat'] = [dataset.hart[x] for x in peaklist]
        self.measures['hart_rollingmean'] = dataset['hart_rollingmean']
        self.measures['hart'] = dataset['hart']

    def calc_RR(self, dataset, fs):
        RR_list = []  # R-R interval of signal
        peaklist = self.measures['peaklist']
        count = 0
        while (count < (len(peaklist) - 1)):
            RR_interval = (peaklist[count + 1] - peaklist[count])  # calculate distance between beats in no of samples
            ms_dist = ((RR_interval / fs) * 1000.0)  # convert sample distances to ms distances
            RR_list.append(ms_dist)  # append to list
            count += 1
        self.measures['RR_list'] = RR_list

    def calc_bpm(self):
        RR_list = self.measures['RR_list']
        self.measures['bpm'] = 60000 / np.mean(RR_list)  # 60000 ms (1 minute) / average R-R interval of signal

    def get_result(self):
        RR_diff = []
        RR_sqdiff = []

        RR_list = self.measures['RR_list']
        count_diff = 0  # use a counter to iterate over the RR_list
        while (count_diff < (len(RR_list) - 1)):  # leep going as long as there are R-R intervals
            RR_diff.append(abs(RR_list[count_diff] - RR_list[
                count_diff + 1]))  # xalculates absolute difference between successive R-R interval
            RR_sqdiff.append(
                math.pow(RR_list[count_diff] - RR_list[count_diff + 1], 2))  # calculates squared difference
            count_diff += 1

        ibi = np.mean(RR_list)  # the mean of RR_list is the mean Inter Beat Interval
        sdnn = np.std(RR_list)  # stdev of all R-R intervals
        sdsd = np.std(RR_diff)  # take stdev of the differences between all subsequent R-R intervals
        rmssd = np.sqrt(np.mean(RR_sqdiff))  # Take root of the mean of the list of squared differences
        nn20 = [x for x in RR_diff if (x > 20)]  # first create a list of all values over 20, 50
        nn50 = [x for x in RR_diff if (x > 50)]
        pnn20 = float(len(nn20)) / float(len(RR_diff))
        pnn50 = float(len(nn50)) / float(len(RR_diff))  # float so no rounding

        result = {
            "IBI": ibi,
            "SDNN": sdnn,
            "SDSD": sdsd,
            "RMSSD": rmssd,
            "pNN20": pnn20,
            "pNN50": pnn50,
        }
        return result

    def cal_hrv(self, dataset, hrw, fs):
        if dataset.size < 300:
            return {
                "IBI": 0,
                "SDNN": 0,
                "SDSD": 0,
                "RMSSD": 0,
                "pNN20": 0,
                "pNN50": 0,
            }

        dataset.columns = ["hart"]
        # hrw is the one-sided window size (used 0.75) and fs is the sample rate (data is recorded at 100Hz)
        self.rolmean(dataset, hrw, fs)
        self.detect_peaks(dataset)
        self.calc_RR(dataset, fs)
        self.calc_bpm()

        return self.get_result()
