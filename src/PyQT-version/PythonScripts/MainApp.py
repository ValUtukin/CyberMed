import sys
import comport as com
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QStackedWidget
from PyQt5.QtWidgets import QMessageBox, QFileDialog
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

        self.upper_rotation_file_path = None
        self.lower_rotation_file_path = None
        self.upper_finger_file_path = None
        self.lower_finger_file_path = None

        self.upper_motors_comboBox.addItems(['Motor 1', 'Motor 2', 'Motor 3', 'Motor 4', 'Motor 5', 'Motor 6'])
        self.lower_motors_comboBox.addItems(['Motor 1', 'Motor 2', 'Motor 3', 'Motor 4', 'Motor 5', 'Motor 6'])
        self.upper_motors_finger_comboBox.addItems(['Motor 1', 'Motor 2', 'Motor 3', 'Motor 4', 'Motor 5', 'Motor 6'])
        self.lower_motors_finger_comboBox.addItems(['Motor 1', 'Motor 2', 'Motor 3', 'Motor 4', 'Motor 5', 'Motor 6'])
        self.upper_motors_rotation_dict = {
            '1': '01',
            '2': '01',
            '3': '01',
            '4': '01',
            '5': '01',
            '6': '01',
            '_1': '10',
            '_2': '10',
            '_3': '10',
            '_4': '10',
            '_5': '10',
            '_6': '10'
        }
        self.upper_motors_rotation_dict_default = self.upper_motors_rotation_dict.copy()

        self.lower_motors_rotation_dict = {
            '1': '01',
            '2': '01',
            '3': '01',
            '4': '01',
            '5': '01',
            '6': '01',
            '_1': '10',
            '_2': '10',
            '_3': '10',
            '_4': '10',
            '_5': '10',
            '_6': '10'
        }
        self.lower_motors_rotation_dict_default = self.lower_motors_rotation_dict.copy()

        self.upper_motors_finger_dict = {
            '1': '000',
            '2': '001',
            '3': '010',
            '4': '011',
            '5': '100',
            '6': '101'
        }
        self.upper_motors_finger_dict_default = self.upper_motors_finger_dict.copy()

        self.lower_motors_finger_dict = {
            '1': '000',
            '2': '001',
            '3': '010',
            '4': '011',
            '5': '100',
            '6': '101'
        }
        self.lower_motors_finger_dict_default = self.lower_motors_finger_dict.copy()

        self.upper_motor_pwm_scale.valueChanged.connect(self.update_upper_pwm_label)
        self.lower_motor_pwm_scale.valueChanged.connect(self.update_lower_pwm_label)

        #  Rotation-settings connections
        self.upper_check_motor_btn.clicked.connect(self.check_upper_motor)
        self.lower_check_motor_btn.clicked.connect(self.check_lower_motor)

        self.upper_apply_rotation_btn.clicked.connect(self.upper_apply_motor_rotation)
        self.lower_apply_rotation_btn.clicked.connect(self.lower_apply_motor_rotation)

        self.upper_discard_all_rotation_btn.clicked.connect(self.upper_discard_all_rotation_settings)
        self.lower_discard_all_rotation_btn.clicked.connect(self.lower_discard_all_rotation_settings)

        #  Motor-to-Finger connections
        self.upper_check_motor_finger_btn.clicked.connect(self.upper_check_motor_finger)
        self.lower_check_motor_finger_btn.clicked.connect(self.lower_check_motor_finger)

        self.upper_apply_finger_btn.clicked.connect(self.upper_apply_motor_finger)
        self.lower_apply_finger_btn.clicked.connect(self.lower_apply_motor_finger)

        self.upper_discard_all_finger_btn.clicked.connect(self.upper_discard_all_finger_settings)
        self.lower_discard_all_finger_btn.clicked.connect(self.lower_discard_all_finger_settings)

        #  Open-File connections
        self.upper_open_rotation_file_for_save_btn.clicked.connect(self.upper_open_rotation_file)
        self.lower_open_rotation_file_for_save_btn.clicked.connect(self.lower_open_rotation_file)
        self.upper_open_finger_file_for_save_btn.clicked.connect(self.upper_open_finger_file)
        self.lower_open_finger_file_for_save_btn.clicked.connect(self.lower_open_finger_file)

        #  Override-File connections
        self.upper_override_rotation_file_btn.clicked.connect(self.upper_override_rotation_file)
        self.lower_override_rotation_file_btn.clicked.connect(self.lower_override_rotation_file)
        self.upper_override_finger_file_btn.clicked.connect(self.upper_override_finger_file)
        self.lower_override_finger_file_btn.clicked.connect(self.lower_override_finger_file)

        #  Discard-File connections
        self.upper_discard_all_rotation_btn.clicked.connect(self.upper_discard_all_rotation)
        self.lower_discard_all_rotation_btn.clicked.connect(self.lower_discard_all_rotation)
        self.upper_discard_all_finger_btn.clicked.connect(self.upper_discard_all_finger)
        self.lower_discard_all_finger_btn.clicked.connect(self.lower_discard_all_finger)

        #  Load-File connections
        self.upper_load_rotation_btn.clicked.connect(self.upper_load_rotation)
        self.lower_load_rotation_btn.clicked.connect(self.lower_load_rotation)
        self.upper_load_finger_btn.clicked.connect(self.upper_load_finger)
        self.lower_load_finger_btn.clicked.connect(self.lower_load_finger)

        #  COMPORT connections
        self.upper_comport_comboBox.activated.connect(self.upper_update_comport_combo_box)
        self.lower_comport_comboBox.activated.connect(self.lower_update_comport_combo_box)
        self.rescan_comport_btn.clicked.connect(self.rescan_comport)
        self.reset_comport_btn.clicked.connect(self.reset_comport)

        # Menu-Bar connections
        self.actionManual_Control.triggered.connect(self.manual_control)
        self.actionPre_saved_moves.triggered.connect(self.pre_saved_moves)
        self.actionElbow_and_Shoulder.triggered.connect(self.elbow_and_shoulder)
        self.actionMain_Window.triggered.connect(self.main_window)
        self.actionMain_Window.setEnabled(False)  # Disable Main Window action when App starts
        # self.motor_settings_groupBox.setEnabled(False)  # Disable Motor Setting box

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

    def upper_update_comport_combo_box(self):
        current_index = self.upper_comport_comboBox.currentIndex()
        lower_combo_box_current_index = self.lower_comport_comboBox.currentIndex()
        self.upper_current_comport_name = get_comport_name(self.upper_comport_comboBox.currentText())

        self.lower_comport_comboBox.clear()
        self.lower_comport_comboBox.addItems(self.available_ports)
        self.lower_comport_comboBox.setCurrentIndex(lower_combo_box_current_index)
        self.lower_comport_comboBox.model().item(current_index).setFlags(QtCore.Qt.NoItemFlags)
        print(f"update_upper: Upper - {self.upper_current_comport_name}, Lower - {self.lower_current_comport_name}")
        self.connect_upper_comport()

    def lower_update_comport_combo_box(self):
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
                self.update_upper_status_label(True)
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
                self.update_lower_status_label(True)
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

        self.update_upper_status_label(False)
        self.update_lower_status_label(False)

    # TODO: Looks like this method simular to rescan_comport. Maybe should remove this one...?
    def reset_comport(self):
        self.upper_comport_comboBox.clear()
        self.lower_comport_comboBox.clear()

        self.upper_comport_comboBox.addItems(self.available_ports)
        self.lower_comport_comboBox.addItems(self.available_ports)

        self.upper_current_comport_name = None
        self.lower_current_comport_name = None

    def update_upper_status_label(self, connected):
        if connected:
            self.upper_comport_status_label.setStyleSheet("border: 3px solid #00AB5D; background-color: #00AB5D")
        else:
            self.upper_comport_status_label.setStyleSheet("border: 3px solid red; background-color: red")

    def update_lower_status_label(self, connected):
        if connected:
            self.lower_comport_status_label.setStyleSheet("border: 3px solid #00AB5D; background-color: #00AB5D")
        else:
            self.lower_comport_status_label.setStyleSheet("border: 3px solid red; background-color: red")

    def update_upper_pwm_label(self, value):
        self.upper_motor_pwm_label.setText(str(value))

    def update_lower_pwm_label(self, value):
        self.lower_motor_pwm_label.setText(str(value))

    def check_upper_motor(self):
        motor_number = self.upper_motors_comboBox.currentIndex() + 1  # Indexes start from 0. Motors start from 1
        pwm = self.upper_motor_pwm_scale.value()
        time = float(self.upper_time_input.toPlainText())
        reverse_flag = self.upper_reverse_motor_checkBox.isChecked()

        if reverse_flag:
            motor_byte_mode = self.upper_motors_rotation_dict[f'_{motor_number}']
        else:
            motor_byte_mode = self.upper_motors_rotation_dict[f'{motor_number}']

        motor_byte_base = '000'
        motor_byte = motor_byte_base + motor_byte_mode + self.upper_motors_finger_dict[f'{motor_number}']

        print(f'We about to check Upper Motor#{motor_number}, motor_byte: {motor_byte}')
        # self.model.send_command('Upper', '00011110', motor_byte, pwm, time, 0)
        # self.model.power_command('Upper', '00000001', '00000001')

    def check_lower_motor(self):
        motor_number = self.lower_motors_comboBox.currentIndex() + 1  # Indexes start from 0. Motors start from 1
        pwm = self.lower_motor_pwm_scale.value()
        time = float(self.lower_time_input.toPlainText())
        reverse_flag = self.lower_reverse_motor_checkBox.isChecked()

        if reverse_flag:
            motor_byte_mode = self.motors_settings_dict[f'_{motor_number}']
        else:
            motor_byte_mode = self.motors_settings_dict[f'{motor_number}']

        motor_byte_base = '000'
        motor_byte = motor_byte_base + motor_byte_mode + self.upper_motors_finger_dict[f'{motor_number}']

        print(f'We about to check Lower Motor#{motor_number}, motor_byte: {motor_byte}')
        # self.model.send_command('Lower', '00011110', motor_byte, pwm, time, 0)
        # self.model.power_command('Lower', '00000001', '00000001')

    def upper_apply_motor_rotation(self):
        motor_number = self.upper_motors_comboBox.currentIndex() + 1
        reverse_flag = self.upper_reverse_motor_checkBox.isChecked()
        warning_message = f'''Nothing to change: reverse flag - {reverse_flag}
Upper motor #{motor_number} has default settings'''
        if reverse_flag:
            self.manual_control.upper_change_motor_rotation(motor_number)
        else:
            QMessageBox.warning(self, 'Warning', warning_message)

    def lower_apply_motor_rotation(self):
        motor_number = self.lower_motors_comboBox.currentIndex() + 1
        reverse_flag = self.lower_reverse_motor_checkBox.isChecked()
        warning_message = f'''Nothing to change: reverse flag - {reverse_flag}
Lower motor #{motor_number} has default settings'''
        if reverse_flag:
            self.manual_control.lower_change_motor_rotation(motor_number)
        else:
            QMessageBox.warning(self, 'Warning', warning_message)

    def upper_discard_all_rotation_settings(self):
        pass

    def lower_discard_all_rotation_settings(self):
        pass

    def upper_discard_all_finger_settings(self):
        pass

    def lower_discard_all_finger_settings(self):
        pass

    def upper_check_motor_finger(self):
        motor_number = self.upper_motors_finger_comboBox.currentIndex() + 1
        motor_number_byte = self.upper_motor_number_input.toPlainText()

        print(f"Motor #{motor_number}, byte number: {motor_number_byte}")
        motor_byte_base = '000'
        motor_byte = motor_byte_base + self.upper_motors_finger_dict[f'{motor_number}'] + motor_number_byte

        print(f'We about to check Lower Motor#{motor_number}, motor_byte: {motor_byte}')
        # self.model.send_command('Upper', '00011110', motor_byte, 50, 0.5, 0)
        # self.model.power_command('Upper', '00000001', '00000001')

    def lower_check_motor_finger(self):
        motor_number = self.lower_motors_finger_comboBox.currentIndex() + 1
        motor_number_byte = self.lower_motor_number_input.toPlainText()

        print(f"Motor #{motor_number}, byte number: {motor_number_byte}")
        motor_byte_base = '000'
        motor_byte = motor_byte_base + self.upper_motors_finger_dict[f'{motor_number}'] + motor_number_byte

        print(f'We about to check Lower Motor#{motor_number}, motor_byte: {motor_byte}')
        # self.model.send_command('Lower', '00011110', motor_byte, 50, 0.5, 0)
        # self.model.power_command('Lower', '00000001', '00000001')

    def upper_apply_motor_finger(self):
        motor_number = self.upper_motors_finger_comboBox.currentIndex() + 1
        motor_byte_number = self.upper_motor_number_input.toPlainText()

        print(f'Motor #{motor_number}, finger num: {motor_byte_number}')

    def lower_apply_motor_finger(self):
        motor_number = self.lower_motors_finger_comboBox.currentIndex() + 1
        motor_byte_number = self.lower_motor_number_input.toPlainText()

        print(f'Motor #{motor_number}, finger num: {motor_byte_number}')

    def upper_open_rotation_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File (Upper rotation)", "/", "Text Files (*.txt)")
        if file_path:
            self.upper_rotation_file_path_label.setText(file_path)
            self.upper_rotation_file_path = file_path

    def lower_open_rotation_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File (Lower rotation)", "/", "Text Files (*.txt)")
        if file_path:
            self.lower_rotation_file_path_label.setText(file_path)
            self.lower_rotation_file_path = file_path

    def upper_open_finger_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File (Upper finger)", "/", "Text Files (*.txt)")
        if file_path:
            self.upper_finger_file_path_label.setText(file_path)
            self.upper_finger_file_path = file_path

    def lower_open_finger_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File (Lower finger)", "/", "Text Files (*.txt)")
        if file_path:
            self.lower_finger_file_path_label.setText(file_path)
            self.lower_finger_file_path = file_path

    # Write all settings to the selected file path
    def upper_override_rotation_file(self):
        with open(self.upper_rotation_file_path, 'w') as f:
            for item in self.upper_motors_rotation_dict.items():
                target_str = f'M{item[0]}: {item[1]}'
                f.write(target_str + '\n')

    def lower_override_rotation_file(self):
        with open(self.lower_rotation_file_path, 'w') as f:
            for item in self.lower_motors_rotation_dict.items():
                target_str = f'M{item[0]}: {item[1]}'
                f.write(target_str + '\n')

    def upper_override_finger_file(self):
        with open(self.upper_finger_file_path, 'w') as f:
            for item in self.upper_motors_finger_dict.items():
                target_str = f'M{item[0]}: {item[1]}'
                f.write(target_str + '\n')

    def lower_override_finger_file(self):
        with open(self.lower_finger_file_path, 'w') as f:
            for item in self.lower_motors_finger_dict.items():
                target_str = f'M{item[0]}: {item[1]}'
                f.write(target_str + '\n')

    def upper_discard_all_rotation(self):
        pass

    def lower_discard_all_rotation(self):
        pass

    def upper_discard_all_finger(self):
        pass

    def lower_discard_all_finger(self):
        pass

    def upper_load_rotation(self):
        if self.upper_settings_file_path is not None:
            upper_settings_dict = dict()
            with open(self.upper_settings_file_path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    motor_number_position = line.find("M") + 1
                    motor_rotation_position = line.find(":") + 2
                    motor_rotation_str = line[motor_rotation_position:motor_rotation_position + 2]
                    if line[motor_number_position] == '_':
                        motor_number_str = line[motor_number_position:motor_number_position + 2]
                    else:
                        motor_number_str = line[motor_number_position]
                    upper_settings_dict[motor_number_str] = motor_rotation_str
            print(upper_settings_dict)
        else:
            print(f"File path is None")

    def lower_load_rotation(self):
        if self.lower_settings_file_path is not None:
            lower_settings_dict = dict()
            with open(self.lower_settings_file_path, 'r') as f:
                lines = f.readlines()
                print(f'Number of lines: {len(lines)}')
                for line in lines:
                    motor_number_position = line.find("M") + 1
                    motor_rotation_position = line.find(":") + 2
                    motor_rotation_str = line[motor_rotation_position:motor_rotation_position + 2]
                    if line[motor_number_position] == '_':
                        motor_number_str = line[motor_number_position:motor_number_position + 2]
                    else:
                        motor_number_str = line[motor_number_position]
                    lower_settings_dict[motor_number_str] = motor_rotation_str
            print(lower_settings_dict)
        else:
            print(f"File path is None")

    def upper_load_finger(self):
        pass

    def lower_load_finger(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApplication()
    window.show()
    sys.exit(app.exec_())
