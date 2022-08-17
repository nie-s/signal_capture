from PyQt5 import QtCore


class EmotionThread(QtCore.QThread):
    def __init__(self, emotion, w, ):
        super().__init__()
        self.emotion = emotion
        self.w = w

    def run(self):
        self.camera, self.out = self.emotion.setup_webcam(self.w.pw)

        while self.w.live_running:
            try:
                self.update_plot()
            except (TypeError):
                if self.w.live_running:
                    print('Something happened.\nRestarting live feed ...')

    def update_plot(self):
        while self.w.live_running:
            _, frame = self.camera.read()
            self.w.emotion.update(frame)
