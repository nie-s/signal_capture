import cv2
from PyQt5 import QtCore


class VideoThread(QtCore.QThread):
    def __init__(self, video, w, ):
        super().__init__()
        self.video = video
        self.w = w

    def run(self):
        self.camera, self.out = self.video.setup_webrrcam(self.w.pw)

        while self.w.live_running:
            try:

                _, frame = self.camera.read()
                self.update_plot(frame)
            except (TypeError):
                if self.w.live_running:
                    print('Something happened.\nRestarting live feed ...')

    def update_plot(self, load_frame):
        while self.w.live_running:
            self.w.video.update(load_frame)
