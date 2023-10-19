import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QStackedWidget
from PyQt5.uic import loadUi
from ManualControl import ManualControl
from PreSavedMoves import PreSavedMoves


class MyApplication(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load the UI from the UI file
        loadUi("../UIs/MainWindow.ui", self)

        text = "Welcome to CyberMed SoftWare"
        self.welcome_label.setText(f"<font color='#00AB5D', size=24>{text}</font>")

        # Connect your menu actions to functions here
        self.actionManual_Control.triggered.connect(self.manual_control)
        self.actionPre_saved_moves.triggered.connect(self.pre_saved_moves)

        self.manual_control = ManualControl()
        self.pre_saved_moves = PreSavedMoves()

        self.stackedWidget.addWidget(self.manual_control)
        self.stackedWidget.addWidget(self.pre_saved_moves)

    def manual_control(self):
        self.stackedWidget.setCurrentWidget(self.manual_control)

    def pre_saved_moves(self):
        self.stackedWidget.setCurrentWidget(self.pre_saved_moves)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApplication()
    window.show()
    sys.exit(app.exec_())