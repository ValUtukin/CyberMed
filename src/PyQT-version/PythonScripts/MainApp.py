import sys
import comport as com
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QStackedWidget
from PyQt5.QtWidgets import QMessageBox
from PyQt5.uic import loadUi
from ManualControl import ManualControl
from PreSavedMoves import PreSavedMoves
from ElbowAndShoulder import ElbowAndShoulder
from DataCollector import DataCollector
from Model import *


def get_comport_name(device_full_name):
    start = device_full_name.find('COM')
    for i in range(start, len(device_full_name)):
        if device_full_name[i] == ' ':
            return device_full_name[start:i]
        else:
            continue
    else:
        return "Really strange COMPORT name"


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
        self.upper_current_comport_name = None
        self.lower_current_comport_name = None
        self.upper_current_comport = None
        self.lower_current_comport = None

        self.upper_comport_comboBox.activated.connect(self.update_upper_combo_box)
        self.lower_comport_comboBox.activated.connect(self.update_lower_combo_box)
        self.rescan_comport_btn.clicked.connect(self.rescan_comport)
        self.reset_comport_btn.clicked.connect(self.reset_comport)

        self.actionManual_Control.triggered.connect(self.manual_control)
        self.actionPre_saved_moves.triggered.connect(self.pre_saved_moves)
        self.actionElbow_and_Shoulder.triggered.connect(self.elbow_and_shoulder)
        self.actionMain_Window.triggered.connect(self.main_window)
        self.actionMain_Window.setEnabled(False)  # Disable Main Window action when App starts

        self.manual_control = ManualControl()
        self.pre_saved_moves = PreSavedMoves()
        self.elbow_and_shoulder = ElbowAndShoulder()
        self.upper_collector = DataCollector(1)
        self.lower_collector = DataCollector(1)
        self.manual_control.set_upper_data_collector(self.upper_collector)
        self.manual_control.set_lower_data_collector(self.lower_collector)

        # Give copy of Model instance to other classes, so they can interact with comports through it
        model_copy = self.model
        self.manual_control.set_model(model_copy)
        self.pre_saved_moves.set_model(model_copy)

        self.stackedWidget.addWidget(self.manual_control)
        self.stackedWidget.addWidget(self.pre_saved_moves)
        self.stackedWidget.addWidget(self.elbow_and_shoulder)

    def manual_control(self):
        self.stackedWidget.setCurrentWidget(self.manual_control)
        self.actionMain_Window.setEnabled(True)

    def pre_saved_moves(self):
        self.stackedWidget.setCurrentWidget(self.pre_saved_moves)
        self.actionMain_Window.setEnabled(True)

    def elbow_and_shoulder(self):
        self.stackedWidget.setCurrentWidget(self.elbow_and_shoulder)
        self.actionMain_Window.setEnabled(True)

    def main_window(self):
        self.stackedWidget.setCurrentWidget(self.page)
        self.actionMain_Window.setEnabled(False)

    # TODO: Add colored labels for ports connection status and connect them to connect_upper_../connect_lower_..
    def update_upper_combo_box(self):
        current_index = self.upper_comport_comboBox.currentIndex()
        lower_combo_box_current_index = self.lower_comport_comboBox.currentIndex()
        self.upper_current_comport_name = get_comport_name(self.upper_comport_comboBox.currentText())

        self.lower_comport_comboBox.clear()
        self.lower_comport_comboBox.addItems(self.available_ports)
        self.lower_comport_comboBox.setCurrentIndex(lower_combo_box_current_index)
        self.lower_comport_comboBox.model().item(current_index).setFlags(QtCore.Qt.NoItemFlags)
        print(f"update_upper: Upper - {self.upper_current_comport_name}, Lower - {self.lower_current_comport_name}")
        self.connect_upper_comport()

    def update_lower_combo_box(self):
        current_index = self.lower_comport_comboBox.currentIndex()
        upper_combo_box_current_index = self.upper_comport_comboBox.currentIndex()
        self.lower_current_comport_name = get_comport_name(self.lower_comport_comboBox.currentText())

        self.upper_comport_comboBox.clear()
        self.upper_comport_comboBox.addItems(self.available_ports)
        self.upper_comport_comboBox.setCurrentIndex(upper_combo_box_current_index)
        self.upper_comport_comboBox.model().item(current_index).setFlags(QtCore.Qt.NoItemFlags)
        print(f"update_lower: Upper - {self.upper_current_comport_name}, Lower - {self.lower_current_comport_name}")
        self.connect_lower_comport()

    # TODO: Need to test comport setting process for upper_collector and lower_collector
    def connect_upper_comport(self):
        if self.upper_current_comport_name is None:
            print('MainApp/connect_upper_comport - upper comport name is None')
        else:
            self.upper_current_comport = com.ini(self.upper_current_comport_name)
            if self.upper_current_comport.is_open:
                self.model.set_upper_comport(self.upper_current_comport)
                self.upper_collector.set_comport(self.upper_current_comport)
            else:
                print('Upper comport is not open')

    def connect_lower_comport(self):
        if self.lower_current_comport_name is None:
            print('MainApp/connect_lower_comport - lower comport name is None')
        else:
            self.lower_current_comport = com.ini(self.lower_current_comport_name)
            if self.lower_current_comport.is_open:
                self.model.set_lower_comport(self.lower_current_comport)
                self.lower_collector.set_comport(self.lower_current_comport)
            else:
                print('Lower comport is not open')

    def rescan_comport(self):
        if self.upper_current_comport:
            com.close_comport(self.upper_current_comport)
        if self.lower_current_comport:
            com.close_comport(self.lower_current_comport)

        self.upper_current_comport_name = None
        self.lower_current_comport_name = None

        self.upper_comport_comboBox.clear()
        self.lower_comport_comboBox.clear()

        self.available_ports = com.show_available_ports()
        self.upper_comport_comboBox.addItems(self.available_ports)
        self.lower_comport_comboBox.addItems(self.available_ports)

    # TODO: Looks like this method simular to rescan_comport. Maybe should remove this one...?
    def reset_comport(self):
        self.upper_comport_comboBox.clear()
        self.lower_comport_comboBox.clear()

        self.upper_comport_comboBox.addItems(self.available_ports)
        self.lower_comport_comboBox.addItems(self.available_ports)

        self.upper_current_comport_name = None
        self.lower_current_comport_name = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApplication()
    window.show()
    sys.exit(app.exec_())
