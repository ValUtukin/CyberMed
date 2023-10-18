import sys
import PreSavedMovesUi
from Model import *
import comport as com
from PyQt5 import QtWidgets, QtCore


class PreSavedMoves(QtWidgets.QMainWindow, PreSavedMovesUi.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        text = "Fist"
        self.fist_label.setText(f"<font color='#00AB5D', size=24>{text}</font>")

        self.fist_compress_btn.clicked.connect(self.fist_compress)
        self.fist_release_btn.clicked.connect(self.fist_release)

        print('PreSavedMoves/__init__()')

    def fist_compress(self):
        print('PreSavedMoves/Fist compress')

    def fist_release(self):
        print('PreSavedMoves/Fist Release')