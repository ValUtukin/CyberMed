import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QStackedWidget
from PyQt5.uic import loadUi
from ManualControl import ManualControl
from PreSavedMoves import PreSavedMoves
from Model import *


class MyApplication(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load the UI from the UI file
        loadUi("../UIs/MainWindow.ui", self)

        text = "Welcome to CyberMed SoftWare"
        self.welcome_label.setText(f"<font color='#00AB5D', size=24>{text}</font>")

        self.model = Model()
        self.available_ports = com.show_available_ports()
        self.upper_comport_comboBox.addItems(self.available_ports)
        self.lower_comport_comboBox.addItems(self.available_ports)
        self.upper_current_comport = None
        self.lower_current_comport = None

        self.upper_comport_comboBox.activated.connect(self.update_upper_combo_box)
        self.lower_comport_comboBox.activated.connect(self.update_lower_combo_box)
        self.rescan_comport_btn.clicked.connect(self.rescan_comport)
        self.reset_comport_btn.clicked.connect(self.reset_comport)

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

    # TODO: Add method to set selected comports inside Model and notice ManualControl and PreSavedMoves
    def update_upper_combo_box(self):
        current_index = self.upper_comport_comboBox.currentIndex()
        lower_comboBox_current_index = self.lower_comport_comboBox.currentIndex()
        self.upper_current_comport = self.upper_comport_comboBox.currentText()[:4]

        self.lower_comport_comboBox.clear()
        self.lower_comport_comboBox.addItems(self.available_ports)
        self.lower_comport_comboBox.setCurrentIndex(lower_comboBox_current_index)
        self.lower_comport_comboBox.model().item(current_index).setFlags(QtCore.Qt.NoItemFlags)
        print(f"update_upper: Upper - {self.upper_current_comport}, Lower - {self.lower_current_comport}")

    def update_lower_combo_box(self):
        current_index = self.lower_comport_comboBox.currentIndex()
        upper_comboBox_current_index = self.upper_comport_comboBox.currentIndex()
        self.lower_current_comport = self.lower_comport_comboBox.currentText()[:4]

        self.upper_comport_comboBox.clear()
        self.upper_comport_comboBox.addItems(self.available_ports)
        self.upper_comport_comboBox.setCurrentIndex(upper_comboBox_current_index)
        self.upper_comport_comboBox.model().item(current_index).setFlags(QtCore.Qt.NoItemFlags)
        print(f"update_lower: Upper - {self.upper_current_comport}, Lower - {self.lower_current_comport}")

    def rescan_comport(self):
        self.upper_comport_comboBox.clear()
        self.lower_comport_comboBox.clear()
        self.available_ports = com.show_available_ports()
        self.upper_comport_comboBox.addItems(self.available_ports)
        self.lower_comport_comboBox.addItems(self.available_ports)

    def reset_comport(self):
        self.upper_comport_comboBox.clear()
        self.lower_comport_comboBox.clear()
        self.upper_comport_comboBox.addItems(self.available_ports)
        self.lower_comport_comboBox.addItems(self.available_ports)
        self.upper_current_comport = None
        self.lower_current_comport = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApplication()
    window.show()
    sys.exit(app.exec_())