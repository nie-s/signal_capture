import csv
import datetime
import os
import time

import cv2
import imutils
import pyqtgraph as pg

from device import emtion_reg

EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised", "neutral"]


class Emotion():

    def __init__(self):
        self.frame = []
        self.pw = None
        self.emotion_data = []

    def setup_webcam(self, w, index):
        self.pw = w.pw
        camera = cv2.VideoCapture(index)

        if not os.path.isdir(w.folder):
            os.makedirs(w.folder)

        self.fps = int (camera.get(cv2.CAP_PROP_FPS) / 2.7)
        self.outVideo = cv2.VideoWriter(w.folder + '/out.avi', cv2.VideoWriter_fourcc(*'mp4v'), self.fps, (448, 336))

        return camera, self.outVideo

    def update(self, frame_read):
        now = datetime.datetime.now()
        nowtimestamp = time.time()
        nowtime = str(now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])

        frame = imutils.resize(frame_read, width=448, height=336)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        frameClone = frame.copy()
        preds, label, fX, fY, fW, fH = emtion_reg.get_emotion(gray)

        if preds is None:
            return

        for (i, (emotion, prob)) in enumerate(zip(EMOTIONS, preds)):
            # construct the label text
            text = "{}: {:.2f}%".format(emotion, prob * 100)

            cv2.putText(frameClone, label, (fX, fY - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
            cv2.rectangle(frameClone, (fX, fY), (fX + fW, fY + fH),
                          (0, 0, 255), 2)



        preds = preds.tolist()
        data = [nowtime, nowtimestamp] + preds
        self.emotion_data.append(data)
        self.outVideo.write(frameClone)

        frameClone, _ = pg.makeARGB(frameClone, None, None, None, False)
        self.pw.img.setImage(frameClone)
        self.pw.vb.viewport().update()

        return preds

    def write_csv(self, folder, timestamp):
        filename = folder + "/emotion.csv"
        with open(filename, 'w', newline='') as f:
            datawriter = csv.writer(f, delimiter=',')
            datawriter.writerow(
                ['Time', 'Timestamp', "angry", "disgust", "scared", "happy", "sad", "surprised", "neutral"])
            datawriter.writerows(self.emotion_data)
