import cv2
import imutils
import pyqtgraph as pg


class WebCam():
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
        self.outVideo.write(frame)

        frame = imutils.resize(frame, width=300)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        self.frame, _ = pg.makeARGB(frame, None, None, None, False)
        self.pw.img.setImage(self.frame)
        self.pw.vb.viewport().update()
