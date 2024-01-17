import sys
import ElbowAndShoulderUi
from Model import *
import comport as com
from PyQt5 import QtWidgets, QtCore


class ElbowAndShoulder(QtWidgets.QMainWindow, ElbowAndShoulderUi.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.elbow_compress_btn.clicked.connect(self.elbow_compress)
        self.elbow_release_btn.clicked.connect(self.elbow_release)
        self.elbow_stop_btn.clicked.connect(self.elbow_stop)

        self.shoulder_motor1_compress_btn.clicked.connect(self.shoulder_motor1_compress)
        self.shoulder_motor1_release_btn.clicked.connect(self.shoulder_motor1_release)
        self.shoulder_motor1_stop_btn.clicked.connect(self.shoulder_motor1_stop)

        self.shoulder_motor2_compress_btn.clicked.connect(self.shoulder_motor2_compress)
        self.shoulder_motor2_release_btn.clicked.connect(self.shoulder_motor2_release)
        self.shoulder_motor2_stop_btn.clicked.connect(self.shoulder_motor2_stop)

        self.shoulder_motor3_compress_btn.clicked.connect(self.shoulder_motor3_compress)
        self.shoulder_motor3_release_btn.clicked.connect(self.shoulder_motor3_release)
        self.shoulder_motor3_stop_btn.clicked.connect(self.shoulder_motor3_stop)

    def elbow_compress(self):
        pass

    def elbow_release(self):
        pass

    def elbow_stop(self):
        pass

    def shoulder_motor1_compress(self):
        pass

    def shoulder_motor1_release(self):
        pass

    def shoulder_motor1_stop(self):
        pass

    def shoulder_motor2_compress(self):
        pass

    def shoulder_motor2_release(self):
        pass

    def shoulder_motor2_stop(self):
        pass

    def shoulder_motor3_compress(self):
        pass

    def shoulder_motor3_release(self):
        pass

    def shoulder_motor3_stop(self):
        pass


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ElbowAndShoulder()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
