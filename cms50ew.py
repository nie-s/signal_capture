import time

import serial
import bluetooth
import glob
import datetime
import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd

from hrv_Calculator import HRV_Calculator


class CMS50EW():
    """Class to instantiate a CMS50EW pulse oximeter."""

    def __init__(self):
        self.pulse_xdata, self.pulse_ydata, self.spo2_xdata, self.spo2_ydata, self.ppg_ydata, self.ppg_ydata, self.finger_data, self.hrv_data = \
            [[], [], [], [], [], [], ['Y'], []]
        self.x_label = 'Time [s]'  # Define x-axis label for plots
        self.x_values = []
        self.plot_title = 'Saved session'
        self.n_data_points = 0
        self.timer = 0
        self.starttime = 0
        self.stored_data = []
        self.pydatetime = None
        self.hrv_Calculator = HRV_Calculator()
        # Most of the following commands we don't use. They are just there as
        # some sort of documentation
        self.cmd_hello1 = b'\x7d\x81\xa7\x80\x80\x80\x80\x80\x80'
        self.cmd_hello2 = b'\x7d\x81\xa2\x80\x80\x80\x80\x80\x80'
        self.cmd_hello3 = b'\x7d\x81\xa0\x80\x80\x80\x80\x80\x80'
        self.cmd_session_hello = b'\x7d\x81\xad\x80\x80\x80\x80\x80\x80'
        self.cmd_get_session_count = b'\x7d\x81\xa3\x80\x80\x80\x80\x80\x80'
        self.cmd_get_session_time = b'\x7d\x81\xa5\x80\x80\x80\x80\x80\x80'
        self.cmd_get_session_duration = b'\x7d\x81\xa4\x80\x80\x80\x80\x80\x80'
        self.cmd_get_user_info = b'\x7d\x81\xab\x80\x80\x80\x80\x80\x80'
        self.cmd_get_session_data = b'\x7d\x81\xa6\x80\x80\x80\x80\x80\x80'
        self.cmd_get_deviceid = b'\x7d\x81\xaa\x80\x80\x80\x80\x80\x80'
        self.cmd_get_info = b'\x7d\x81\xb0\x80\x80\x80\x80\x80\x80'
        self.cmd_get_model = b'\x7d\x81\xa8\x80\x80\x80\x80\x80\x80'
        self.cmd_get_vendor = b'\x7d\x81\xa9\x80\x80\x80\x80\x80\x80'
        self.cmd_session_erase = b'\x7d\x81\xae\x80\x80\x80\x80\x80\x80'
        self.cmd_custom = b'\x7d\x81\xf5\x80\x80\x80\x80\x80\x80'
        self.cmd_session_stuff = b'\x7d\x81\xaf\x80\x80\x80\x80\x80\x80'
        self.cmd_get_live_data = b'\x7d\x81\xa1\x80\x80\x80\x80\x80\x80'

    def setup_device(self, target, baudrate):
        self.target = target

        try:
            self.ser = serial.Serial(self.target,
                                     baudrate=baudrate,
                                     parity=serial.PARITY_NONE,
                                     stopbits=serial.STOPBITS_ONE,
                                     bytesize=serial.EIGHTBITS,
                                     timeout=0.1,
                                     xonxoff=1)
            return True
        except:
            return False

    def initiate_device(self):
        """Sends bytes to device which seem to serve its initialization."""
        self.send_cmd(self.cmd_hello1)
        response = self.recv()
        if not response:
            return False
        self.send_cmd(self.cmd_hello2)
        self.send_cmd(self.cmd_hello3)
        self.recv()
        return True

    def recv(self, bytes=1):
        """Receives entire response from device and saves it in list."""
        response_list = []
        while True:
            response = self.ser.read()

            if response:
                response_list.append(response)
            else:
                break
        return response_list

    def send_cmd(self, cmd, debug=False):
        """
        Sends specified command to device and prints debug output if debug flag
        is set.
        """

        self.ser.write(cmd)

        if debug:
            print("Write:    ", cmd)
            response = []
            while True:
                r = response.append(self.ser.read())
                if self.ser.in_waiting == 0:
                    break
            response_string = ' '.join([str(ord(r)) for r in response])
            print("Response: ", response)

    def process_data(self):
        """Reads data from device and returns key values."""
        counter = 1
        value_list = []
        while counter < 9:
            value = self.ser.read()
            # The following if clause basically functions to discard the first
            # bunch of data  which is of no use to us; the list of values we
            # need starts with a 1.

            if ord(value) == 1:
                value_list = []
                counter = 1
            else:
                counter += 1
            value_list.append(value)

        # Extract the key values from value_list
        finger = value_list[3]
        if finger == b'\xc0':
            finger = 'Y'
        else:
            finger = 'N'
        strength = int(ord(value_list[4][0:4]) & 0xf)
        pulse_rate = int(ord(value_list[5]) & 0x7f)
        spo2 = int(ord(value_list[6]) & 0x7f)
        ppg = int(ord(value_list[3]) & 0x7f)
        pulse_pd = pd.DataFrame(self.ppg_ydata)
        hrv = self.hrv_Calculator.cal_hrv(pulse_pd, 1, 60)

        now = datetime.datetime.now()
        nowtimestamp = time.time()
        nowtime = str(now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])

        return [nowtime, nowtimestamp, finger, pulse_rate, spo2, ppg, strength,
                hrv["IBI"], hrv["SDNN"], hrv["SDSD"], hrv["RMSSD"], hrv["pNN20"], hrv["pNN50"]]

    def convert_datetime(self):
        """Replaces time deltas with absolute time."""
        for data in self.stored_data:
            newtime = self.pydatetime + datetime.timedelta(0, data[0])
            self.x_values.append(data[0])  # Copy original values for Matplotlib
            data[0] = newtime.time().strftime('%d %B %Y, %H:%M:%S')
        self.x_label = 'Time'
        enddatetime = self.pydatetime + datetime.timedelta(0, self.x_values[-1])
        self.plot_title = str('Recorded session from ' +
                              self.pydatetime.strftime('%d %B %Y, %H:%M:%S') + ' to '
                              + enddatetime.strftime('%d %B %Y, %H:%M:%S'))

    def write_csv(self, timestamp):
        """Writes session data as CSV file."""
        filename = "data/spo2_" + timestamp + ".csv"

        with open(filename, 'w', newline='') as f:
            datawriter = csv.writer(f, delimiter=',')
            datawriter.writerow(
                ['Time', 'Timestamp', 'Pulse rate [bpm]', 'spo2', 'ppg', 'strength', 'IBI', 'SDNN', 'SDSD', 'RMSSD',
                 'pNN20', 'pNN50'])
            datawriter.writerows(self.stored_data)

        # self.plot_mpl(timestamp)
        # for i in range(0, len(self.pulse_ydata)):
        #     time_in_ms = self.starttime + self.pulse_xdata[i]
        #     timeStr = time.strftime('%Y-%m-%d-%H:%M:%S.{}'.format(str(time_in_ms % 1 * 10000)[:5]), time.localtime(
        #         self.starttime + self.pulse_xdata[i]))
        #     datawriter.writerow([timeStr, self.pulse_ydata[i], self.ppg_ydata[i]])

    def close_device(self):
        """Closes device socket"""
        self.ser.close()

    def plot_mpl(self, timestamp):
        """Plots stored session data as Matplotlib plot."""

        hrv = self.hrv_data[-1]
        sdnn = hrv["SDNN"] / 141 * 50
        rmssd = hrv["RMSSD"] / 39 * 10
        pnn20 = hrv["pNN20"] / 34 * 10000
        pnn50 = hrv["pNN50"] / 16 * 10000

        # hrv["IBI"], hrv["SDNN"], hrv["SDSD"], hrv["RMSSD"], hrv["pNN20"], hrv["pNN50"]])
        results = [{"SDANN": 100, "RMSSD": 100, "PNN20": 100, "PNN50": 100},
                   {"SDANN": sdnn, "RMSSD": rmssd, "PNN20": pnn20, "PNN50": pnn50}, ]

        data_length = len(results[0])

        # 将极坐标根据数据长度进行等分
        angles = np.linspace(0, 2 * np.pi, data_length, endpoint=False)
        labels = [key for key in results[0].keys()]
        score = [[v for v in result.values()] for result in results]
        # 使雷达图数据封闭
        score_a = np.concatenate((score[0], [score[0][0]]))
        score_b = np.concatenate((score[1], [score[1][0]]))
        angles = np.concatenate((angles, [angles[0]]))
        labels = np.concatenate((labels, [labels[0]]))
        # 设置图形的大小
        fig = plt.figure(figsize=(10, 38), dpi=100)
        # 新建一个子图
        ax = plt.subplot(4, 1, 1, polar=True)
        # 绘制雷达图
        ax.plot(angles, score_a, 'o-', linewidth=2, label='Reference', color='lightskyblue')
        ax.fill(angles, score_a, alpha=0.25)

        ax.plot(angles, score_b, 'o-', linewidth=2, label='Comparison', color='salmon')
        ax.fill(angles, score_b, alpha=0.4, color='mistyrose')

        # 设置雷达图中每一项的标签显示
        ax.set_thetagrids(angles * 180 / np.pi, labels)
        # 设置雷达图的0度起始位置
        ax.set_theta_zero_location('N')
        # 设置雷达图的坐标刻度范围
        ax.set_rlim(0, 150)

        # 设置雷达图的坐标值显示角度，相对于起始角度的偏移量
        ax.set_rlabel_position(270)
        ax.set_title("HRV Parameter Radar Chart\n (Chart values in %, Reference NNI parameters = 100%", fontsize=17)
        # plt.legend(["Reference", "Comparison"], loc='best')
        plt.legend(loc='best')

        pulse_plot = plt.subplot(4, 1, 2)

        if self.x_label == 'Time':
            xvalues = []
            for value in self.x_values:
                newdatetime = self.pydatetime + datetime.timedelta(0, value)
                xvalues.append(time.strftime('%m-%d,%H:%M', newdatetime))
        else:
            xvalues = [data[0] for data in self.stored_data]

        ln1 = pulse_plot.plot(xvalues, [data[2] for data in self.stored_data], c='lightcoral', label="pulse")
        pulse_plot.set_title("Spo2 & HR", fontsize=17)
        # pulse_plot.set_xlabel(self.x_label, fontsize=24)
        pulse_plot.set_ylabel('Pulse rate [bpm]', fontsize=14)
        pulse_plot.set_ylim([40, 220])

        spo2_plot = pulse_plot.twinx()
        ln2 = spo2_plot.plot(xvalues, [data[3] for data in self.stored_data], color='skyblue', label="spo2")
        spo2_plot.set_ylabel('SpO2 [%]', fontsize=14)
        spo2_plot.set_ylim([80, 100])

        # plt.xticks(xvalues[0::100])
        plt.xticks([])
        pulse_plot.tick_params(axis='both', labelsize=14)
        spo2_plot.tick_params(axis='both', labelsize=14)

        lns = ln1 + ln2
        labs = ["pulse", "spo2"]
        pulse_plot.legend(lns, labs, loc=0)

        '''
        plot 3
        '''

        # xvalues, [data[2] for data in self.stored_data]
        plt.subplot(4, 1, 3)

        yvalues = [data[2] for data in self.stored_data]

        plt.plot(xvalues, yvalues, ls="dashed", c="gray", lw=0.5)
        plt.scatter(xvalues, yvalues, c=yvalues, cmap=plt.cm.RdYlGn_r, edgecolor='none', s=40)  # 根据每个点的y值来设置其颜色
        # 设置图表标题并给坐标轴加上标签

        level1 = max(yvalues) + 3
        level3 = min(yvalues) - 3
        level2 = (level1 + level3) / 2

        plt.axhline(y=level1, c="r", lw=1)
        plt.axhline(y=level2, c="orange", lw=1)
        plt.axhline(y=level3, c="green", lw=1)

        plt.title("Heart Rate Heat Plot", fontsize=17)
        plt.ylabel("Heart Rate", fontsize=14)
        plt.xticks([])

        # 设置刻度标记的大小
        plt.tick_params(axis='both', which='major', labelsize=14)

        plt.subplot(4, 1, 4)

        peaklist = self.hrv_Calculator.measures['peaklist']
        ybeat = self.hrv_Calculator.measures['ybeat']
        plt.title("Heartbeat Plot")
        plt.plot(self.hrv_Calculator.measures['hart'], alpha=0.5, color='skyblue', label="raw signal")
        plt.plot(self.hrv_Calculator.measures['hart_rollingmean'], color='yellowgreen', label="moving average")
        plt.scatter(peaklist, ybeat, color='lightcoral',
                    label="average: %.1f BPM" % self.hrv_Calculator.measures['bpm'])
        plt.legend(loc=4, framealpha=0.6)

        filename = "pic/spo2_" + timestamp + ".pdf"
        plt.savefig(filename)
        plt.show()
