import csv
import datetime
import time

from PyQt5 import QtCore


class EmotionThread(QtCore.QThread):
    def __init__(self, emotion, w, index):
        super().__init__()
        self.emotion = emotion
        self.w = w
        self.index = index

    def run(self):
        self.camera, self.out = self.emotion.setup_webcam(self.w, self.index)

        while self.w.live_running:
            try:
                self.update_plot()
            except Exception as e:
                print(e)
                if self.w.live_running:
                    self.camera, self.out = self.emotion.setup_webcam(self.w, self.index)
                    print('Something happened in emotion_thread')

    def update_plot(self):
        started = False
        print(datetime.datetime.now())
        while self.w.live_running:
            frame = self.camera.read()[1]

            if not started:
                now = datetime.datetime.now()
                nowtime = str(now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
                nowtimestamp = time.time()
                self.emotion.starting = now
                self.emotion.starting_timestamp = nowtimestamp

                print("视频录制")
                with open(self.w.folder + '/actions.csv', 'a') as f:
                    datawriter = csv.writer(f, delimiter=',')
                    datawriter.writerow([nowtime, nowtimestamp, '视频录制'])
                started = True

            data = self.w.emotion.update(frame)
            # print(data)
            # self.w.pw.barSet.remove(0, 7)
            # self.w.pw.barSet.append(data)
