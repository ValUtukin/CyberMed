import sys
import PreSavedMovesUi
from Model import *
import comport as com
from PyQt5 import QtWidgets, QtCore


class PreSavedMoves(QtWidgets.QMainWindow, PreSavedMovesUi.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        print('PreSavedMoves/__init__()')

    def fist_compress(self):
        print('PreSavedMoves/Fist compress')

    def fist_release(self):
        print('PreSavedMoves/Fist Release')


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = PreSavedMoves()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
