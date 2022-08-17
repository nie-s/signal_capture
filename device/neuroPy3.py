import csv
import datetime
import time

import serial


class NeuroPy():
    def __init__(self):
        self.attention_ydata = []
        self.meditation_ydata = []
        self.rawValue_ydata = []
        self.delta_ydata = []
        self.theta_ydata = []
        self.lowAlpha_ydata = []
        self.highAlpha_ydata = []
        self.lowBeta_ydata = []
        self.highBeta_ydata = []
        self.lowGamma_ydata = []
        self.midGamma_ydata = []
        self.poorSignal_ydata = []
        self.blinkStrength_ydata = []
        self.egg_xdata = []

        self.timer = 0
        self.starttime = 0
        self.stored_data = []

        self.sel = None
        self.port = None
        self.baudRate = None

    def setup_device(self, port, baudRate):
        self.port = port
        try:
            self.sel = serial.Serial(port, baudRate)
            return True
        except:
            return False

    def process_data(self):
        begin = 0
        attention, meditation, blinkStrength, rawValue, delta, theta, lowAlpha, \
        highAlpha, lowBeta, highBeta, lowGamma, midGamma = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        p1 = self.sel.read(1).hex()  # read first 2 packets
        p2 = self.sel.read(1).hex()
        while p1 != 'aa' or p2 != 'aa':
            p1 = p2
            p2 = self.sel.read(1).hex()
        else:
            # a valid packet is available
            payload = []
            checksum = 0
            payloadLength = int(self.sel.read(1).hex(), 16)
            for i in range(payloadLength):
                tempPacket = self.sel.read(1).hex()
                payload.append(tempPacket)
                checksum += int(tempPacket, 16)
            checksum = ~checksum & 0x000000ff
            if checksum == int(self.sel.read(1).hex(), 16):
                i = 0
                while i < payloadLength:
                    code = payload[i]
                    if (code == '02'):  # poorSignal
                        i = i + 1
                        poorSignal = int(payload[i], 16)
                    elif (code == '04'):  # attention
                        begin = 1
                        i = i + 1
                        attention = int(payload[i], 16)
                        self.attention_ydata.append(attention)
                    elif (code == '05'):  # meditation
                        begin = 1
                        i = i + 1
                        meditation = int(payload[i], 16)
                        self.meditation_ydata.append(meditation)
                    elif (code == '16'):  # blink strength
                        i = i + 1
                        blinkStrength = int(payload[i], 16)
                        self.blinkStrength_ydata.append(blinkStrength)

                    elif (code == '80'):  # raw value
                        i = i + 1  # for length/it is not used since length =1 byte long and always=2
                        i = i + 1
                        if begin == 1:
                            val0 = int(payload[i], 16)
                            i = i + 1
                            if val0 * 256 + int(payload[i], 16) > 32768:
                                rawValue = (val0 * 256 + int(payload[i], 16) - 65536)
                            else:
                                rawValue = (val0 * 256 + int(payload[i], 16))
                            self.rawValue_ydata.append(rawValue)

                        else:
                            i = i + 1
                    elif (code == '83'):  # ASIC_EEG_POWER
                        begin = 1
                        i = i + 1  # for length/it is not used since length =1 byte long and always=2
                        # delta:
                        i = i + 1
                        val0 = int(payload[i], 16)
                        i = i + 1
                        val1 = int(payload[i], 16)
                        i = i + 1
                        delta = val0 * 65536 + val1 * 256 + int(payload[i], 16)
                        self.delta_ydata.append(delta)
                        # theta:
                        i = i + 1
                        val0 = int(payload[i], 16)
                        i = i + 1
                        val1 = int(payload[i], 16)
                        i = i + 1
                        theta = val0 * 65536 + val1 * 256 + int(payload[i], 16)
                        self.theta_ydata.append(theta)

                        # lowAlpha:
                        i = i + 1
                        val0 = int(payload[i], 16)
                        i = i + 1
                        val1 = int(payload[i], 16)
                        i = i + 1
                        lowAlpha = val0 * 65536 + val1 * 256 + int(payload[i], 16)
                        self.lowAlpha_ydata.append(lowAlpha)

                        # highAlpha:
                        i = i + 1
                        val0 = int(payload[i], 16)
                        i = i + 1
                        val1 = int(payload[i], 16)
                        i = i + 1
                        highAlpha = val0 * 65536 + val1 * 256 + int(payload[i], 16)
                        self.highAlpha_ydata.append(highAlpha)

                        # lowBeta:
                        i = i + 1
                        val0 = int(payload[i], 16)
                        i = i + 1
                        val1 = int(payload[i], 16)
                        i = i + 1
                        lowBeta = val0 * 65536 + val1 * 256 + int(payload[i], 16)
                        self.lowBeta_ydata.append(lowBeta)

                        # highBeta:
                        i = i + 1
                        val0 = int(payload[i], 16)
                        i = i + 1
                        val1 = int(payload[i], 16)
                        i = i + 1
                        highBeta = val0 * 65536 + val1 * 256 + int(payload[i], 16)
                        self.highBeta_ydata.append(highBeta)

                        # lowGamma:
                        i = i + 1
                        val0 = int(payload[i], 16)
                        i = i + 1
                        val1 = int(payload[i], 16)
                        i = i + 1
                        lowGamma = val0 * 65536 + val1 * 256 + int(payload[i], 16)
                        self.lowGamma_ydata.append(lowGamma)

                        # midGamma:
                        i = i + 1
                        val0 = int(payload[i], 16)
                        i = i + 1
                        val1 = int(payload[i], 16)
                        i = i + 1
                        midGamma = val0 * 65536 + val1 * 256 + int(payload[i], 16)
                        self.midGamma_ydata.append(midGamma)

                    else:
                        pass
                    i = i + 1

        now = datetime.datetime.now()
        nowtimestamp = time.time()
        nowtime = str(now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])

        self.egg_xdata.append(nowtimestamp - self.starttime)

        data = [nowtime, nowtimestamp, attention, meditation, blinkStrength, rawValue, delta, theta, lowAlpha,
                highAlpha, lowBeta, highBeta, lowGamma, midGamma]
        self.stored_data.append(data)

        return data

    def write_csv(self, timestamp):
        """Writes session data as CSV file."""
        filename = "data/egg_" + timestamp + ".csv"

        with open(filename, 'w', newline='') as f:
            datawriter = csv.writer(f, delimiter=',')
            datawriter.writerow(
                ['Time', 'Timestamp', ' Pulse rate [bpm]', 'spo2', 'ppg', 'strength', 'IBI', 'SDNN', 'SDSD', 'RMSSD',
                 'pNN20', 'pNN50'])
            datawriter.writerows(self.stored_data)
