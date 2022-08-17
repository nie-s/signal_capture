import cv2
import pyqtgraph as pg

from device import emtion_reg

EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised", "neutral"]


class Emotion():

    def __init__(self):
        self.frame = []
        self.pw = None

    def setup_webcam(self, pw):
        self.pw = pw
        camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = camera.get(cv2.CAP_PROP_FPS)

        # self.outVideo = cv2.VideoWriter('out.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fp, (width, height))
        # self.outVideo = cv2.VideoWriter('out.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps,
        #                                 (int(camera.get(3)), int(camera.get(4))))
        self.outVideo = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc('P', 'I', 'M', 'I'), fps, (width, height))

        return camera, self.outVideo

    def update(self, frame):
        # frame = imutils.resize(frame, width=500)
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

        self.outVideo.write(frameClone)
        frameClone, _ = pg.makeARGB(frameClone, None, None, None, False)
        self.pw.img.setImage(frameClone)
        self.pw.vb.viewport().update()
