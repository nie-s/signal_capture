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
        while self.w.live_running:
            frame = self.camera.read()[1]
            data = self.w.emotion.update(frame)
            # print(data)
            self.w.pw.barSet.remove(0, 7)
            self.w.pw.barSet.append(data)
