import csv
import os

import cv2
import imutils
import pyqtgraph as pg

EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised", "neutral"]


class Emotion():

    def __init__(self):
        self.frame = []
        self.pw = None
        self.emotion_data = []

        self.starting = 0
        self.starting_timestamp = 0

    def setup_webcam(self, w, index):
        self.pw = w.pw
        camera = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        print(int(camera.get(cv2.CAP_PROP_FPS)))

        camera.set(cv2.CAP_PROP_FPS, 30)
        # camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        # camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        if not os.path.isdir(w.folder):
            os.makedirs(w.folder)

        # self.fps = int(camera.get(cv2.CV_CAP_PROP_FPS) / 1)
        self.fps = 30
        self.outVideo = cv2.VideoWriter(w.folder + '/out.avi', cv2.VideoWriter_fourcc(*'mp4v'), self.fps,
                                        (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
                                         int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))))
        # self.outVideo = cv2.VideoWriter(w.folder + '/out.avi', cv2.VideoWriter_fourcc(*'MJPG'), self.fps, (1280, 720))

        return camera, self.outVideo

    def update(self, frame_read):
        frame = imutils.resize(frame_read, width=640, height=480)

        frameClone = frame.copy()
        # print(frameClone)
        '''
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
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
        '''

        self.outVideo.write(frame_read)

        frameClone, _ = pg.makeARGB(frameClone, None, None, None, False)
        self.pw.img.setImage(frameClone)
        self.pw.vb.viewport().update()

        return []

    def write_csv(self, folder, timestamp):
        filename = folder + "/emotion.csv"
        with open(filename, 'w', newline='') as f:
            datawriter = csv.writer(f, delimiter=',')
            datawriter.writerow(
                ['Time', 'Timestamp', "angry", "disgust", "scared", "happy", "sad", "surprised", "neutral"])
            datawriter.writerows(self.emotion_data)
