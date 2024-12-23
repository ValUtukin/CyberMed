import sys
import comport as com
from logging import getLogger, basicConfig, DEBUG
from comport import ComportInstance
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.uic import loadUi
from ManualControl import ManualControl
from PreSavedMoves import PreSavedMoves
from ElbowAndShoulder import ElbowAndShoulder
from DataCollector import DataCollector
from FileWriter import FileWriter
from CommandMaster import CommandMaster


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

        # Set Application Icon (window top-left). !Modify icon path to your directory!
        self.icon_file_path = r"C:/PyCharmProjects/PyQt_withHub/CyberMed/Images/cyber_hand.png"
        self.setWindowIcon(QtGui.QIcon(self.icon_file_path))

        text = "Welcome to CyberMed SoftWare"
        self.welcome_label.setText(f"<font color='#00AB5D', size=24>{text}</font>")

        # Setup Logger
        self.main_logger = getLogger()
        self.logging_format = "[%(levelname)s] - [%(asctime)s] - [%(name)s] - %(message)s"
        self.log_file_path = r"D://PythonProjects/log/MainApp.log"
        basicConfig(filename=self.log_file_path, filemode='w', level=DEBUG, format=self.logging_format)
        self.main_logger.info("START NEW SESSION")

        self.command_master = CommandMaster()
        self.available_ports = com.show_available_ports()
        self.upper_comport_comboBox.addItems(self.available_ports)
        self.lower_comport_comboBox.addItems(self.available_ports)
        self.upper_current_comport_name = None
        self.lower_current_comport_name = None
        self.upper_current_comport = None
        self.lower_current_comport = None

        # File path for custom command logging
        self.command_log_file_path = r"D:/PythonProjects/CyberMed/CyberMed/Data/command_log.txt"
        # Clearing command log file every time MainApp is started
        with open(self.command_log_file_path, 'w') as f:
            f.write("")

        # Default settings file paths. Use for autoload function (motor_settings_autoload). !Modify to your directory!
        self.upper_rotation_file_path = r"D:/PythonProjects/CyberMed/CyberMed/Data/upper_rotation.txt"
        self.lower_rotation_file_path = r"D:/PythonProjects/CyberMed/CyberMed/Data/lower_rotation.txt"
        self.upper_finger_file_path = r"D:/PythonProjects/CyberMed/CyberMed/Data/upper_finger.txt"
        self.lower_finger_file_path = r"D:/PythonProjects/CyberMed/CyberMed/Data/lower_finger.txt"
        self.upper_adc_channels_file_path = r"D:/PythonProjects/CyberMed/CyberMed/Data/upper_adc_channels.txt"
        self.lower_adc_channels_file_path = r"D:/PythonProjects/CyberMed/CyberMed/Data/lower_adc_channels.txt"

        self.upper_motors_comboBox.addItems(['Motor 1', 'Motor 2', 'Motor 3', 'Motor 4', 'Motor 5', 'Motor 6'])
        self.lower_motors_comboBox.addItems(['Motor 1', 'Motor 2', 'Motor 3', 'Motor 4', 'Motor 5', 'Motor 6'])
        self.upper_motors_finger_comboBox.addItems(['Motor 1', 'Motor 2', 'Motor 3', 'Motor 4', 'Motor 5', 'Motor 6'])
        self.lower_motors_finger_comboBox.addItems(['Motor 1', 'Motor 2', 'Motor 3', 'Motor 4', 'Motor 5', 'Motor 6'])
        self.upper_motors_adc_test_comboBox.addItems(['Motor 1', 'Motor 2', 'Motor 3', 'Motor 4', 'Motor 5', 'Motor 6'])
        self.lower_motors_adc_test_comboBox.addItems(['Motor 1', 'Motor 2', 'Motor 3', 'Motor 4', 'Motor 5', 'Motor 6'])
        self.upper_motors_adc_channel_comboBox.addItems(['Channel 0', 'Channel 1', 'Channel 2', 'Channel 3',
                                                         'Channel 4', 'Channel 5'])
        self.lower_motors_adc_channel_comboBox.addItems(['Channel 0', 'Channel 1', 'Channel 2', 'Channel 3',
                                                         'Channel 4', 'Channel 5'])
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

        self.upper_adc_channels_dict = {
            '1': '0',
            '2': '1',
            '3': '2',
            '4': '3',
            '5': '4',
            '6': '5'
        }
        self.upper_adc_channels_dict_default = self.upper_adc_channels_dict.copy()

        self.lower_adc_channels_dict = {
            '1': '0',
            '2': '1',
            '3': '2',
            '4': '3',
            '5': '4',
            '6': '5'
        }
        self.lower_adc_channels_dict_default = self.lower_adc_channels_dict.copy()

        self.upper_motor_pwm_scale.valueChanged.connect(self.update_upper_pwm_label)
        self.lower_motor_pwm_scale.valueChanged.connect(self.update_lower_pwm_label)

        #  Rotation-settings connections
        self.upper_check_motor_btn.clicked.connect(self.upper_check_motor_rotation)
        self.lower_check_motor_btn.clicked.connect(self.lower_check_motor_rotation)

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

        # ADC-testing connections
        self.upper_check_adc_btn.clicked.connect(self.upper_check_adc)
        self.lower_check_adc_btn.clicked.connect(self.lower_check_adc)
        self.upper_motor_adc_test_pwm_scale.valueChanged.connect(self.update_upper_adc_pwm_label)
        self.lower_motor_adc_test_pwm_scale.valueChanged.connect(self.update_lower_adc_pwm_label)
        self.upper_apply_adc_data_btn.clicked.connect(self.upper_apply_adc_data)
        self.lower_apply_adc_data_btn.clicked.connect(self.lower_apply_adc_data)
        self.upper_discard_adc_data_btn.clicked.connect(self.upper_discard_adc_data)
        self.lower_discard_adc_data_btn.clicked.connect(self.lower_discard_adc_data)
        self.adc_label_place_default_text('Upper')
        self.adc_label_place_default_text('Lower')
        self.upper_adc_test_thread = QtCore.QThread()
        self.lower_adc_test_thread = QtCore.QThread()

        #  Open-File connections
        self.upper_open_rotation_file_for_save_btn.clicked.connect(self.upper_open_rotation_file)
        self.lower_open_rotation_file_for_save_btn.clicked.connect(self.lower_open_rotation_file)
        self.upper_open_finger_file_for_save_btn.clicked.connect(self.upper_open_finger_file)
        self.lower_open_finger_file_for_save_btn.clicked.connect(self.lower_open_finger_file)
        self.upper_open_adc_file_for_save_btn.clicked.connect(self.upper_open_adc_file)
        self.lower_open_adc_file_for_save_btn.clicked.connect(self.lower_open_adc_file)

        #  Override-File connections
        self.upper_override_rotation_file_btn.clicked.connect(self.upper_override_rotation_file)
        self.lower_override_rotation_file_btn.clicked.connect(self.lower_override_rotation_file)
        self.upper_override_finger_file_btn.clicked.connect(self.upper_override_finger_file)
        self.lower_override_finger_file_btn.clicked.connect(self.lower_override_finger_file)
        self.upper_override_adc_file_btn.clicked.connect(self.upper_override_adc_file)
        self.lower_override_adc_file_btn.clicked.connect(self.lower_override_adc_file)

        #  Load-File connections
        self.upper_load_rotation_btn.clicked.connect(self.upper_load_rotation)
        self.lower_load_rotation_btn.clicked.connect(self.lower_load_rotation)
        self.upper_load_finger_btn.clicked.connect(self.upper_load_finger)
        self.lower_load_finger_btn.clicked.connect(self.lower_load_finger)
        self.upper_load_adc_btn.clicked.connect(self.upper_load_adc)
        self.lower_load_adc_btn.clicked.connect(self.lower_load_adc)

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
        self.file_writer = FileWriter()

        # Collectors to test ADC
        self.upper_adc_collector = DataCollector(set_num=1, name="MainApp Upper-test")
        self.lower_adc_collector = DataCollector(set_num=1, name="MainApp Lower-test")
        # Setup ADC-testing thread
        self.upper_setup_adc_test_thread()
        self.lower_setup_adc_test_thread()

        # Collectors for actual work
        self.upper_collector = DataCollector(set_num=1, name="Upper-single")
        self.lower_collector = DataCollector(set_num=1, name="Lower-single")
        self.upper_collector_both = DataCollector(set_num=1, name="Upper-both")
        self.lower_collector_both = DataCollector(set_num=1, name="Lower-both")

        self.manual_control.set_upper_data_collector(self.upper_collector)
        self.manual_control.set_lower_data_collector(self.lower_collector)
        self.manual_control.set_upper_collector_both(self.upper_collector_both)
        self.manual_control.set_lower_collector_both(self.lower_collector_both)
        self.manual_control.set_file_writer(self.file_writer)

        # Give copy of CommandMaster instance to other classes, so they can interact with comports through it
        master_copy = self.command_master
        self.manual_control.set_command_master(master_copy)
        self.pre_saved_moves.set_command_master(master_copy)

        self.stackedWidget.addWidget(self.manual_control)
        self.stackedWidget.addWidget(self.pre_saved_moves)
        self.stackedWidget.addWidget(self.elbow_and_shoulder)

        # Load motor settings from default directory
        self.motor_settings_autoload()
        # Show the obtained settings
        self.settings_from_file_init()

    def motor_settings_autoload(self):
        print("MainApp/motor_settings_autoload - load settings")
        upper_rotation_dict = dict()
        lower_rotation_dict = dict()
        upper_finger_dict = dict()
        lower_finger_dict = dict()
        upper_adc_channels_dict = dict()
        lower_adc_channels_dict = dict()

        # Load upper rotation file
        with open(self.upper_rotation_file_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                motor_number_position = line.find("M") + 1
                motor_rotation_position = line.find(":") + 2
                motor_rotation_str = line[motor_rotation_position:motor_rotation_position + 2]
                if line[motor_number_position] == '_':
                    motor_number_str = line[motor_number_position:motor_number_position + 2]
                else:
                    motor_number_str = line[motor_number_position]
                upper_rotation_dict[motor_number_str] = motor_rotation_str

        # Load lower rotation file
        with open(self.lower_rotation_file_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                motor_number_position = line.find("M") + 1
                motor_rotation_position = line.find(":") + 2
                motor_rotation_str = line[motor_rotation_position:motor_rotation_position + 2]
                if line[motor_number_position] == '_':
                    motor_number_str = line[motor_number_position:motor_number_position + 2]
                else:
                    motor_number_str = line[motor_number_position]
                lower_rotation_dict[motor_number_str] = motor_rotation_str

        # Load upper finger file
        with open(self.upper_finger_file_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                motor_number_position = line.find("M") + 1
                motor_finger_position = line.find(":") + 2
                motor_finger_str = line[motor_finger_position:motor_finger_position + 3]
                motor_number_str = line[motor_number_position]
                upper_finger_dict[motor_number_str] = motor_finger_str

        # Load upper finger file
        with open(self.lower_finger_file_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                motor_number_position = line.find("M") + 1
                motor_finger_position = line.find(":") + 2
                motor_finger_str = line[motor_finger_position:motor_finger_position + 3]
                motor_number_str = line[motor_number_position]
                lower_finger_dict[motor_number_str] = motor_finger_str

        # Load upper ADC channels file
        with open(self.upper_adc_channels_file_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                motor_number_position = line.find("M") + 1
                motor_adc_position = line.find(":") + 2
                motor_adc_str = line[motor_adc_position:motor_adc_position + 3]
                motor_number_str = line[motor_number_position]
                upper_adc_channels_dict[motor_number_str] = motor_adc_str

        # Load lower ADC channels file
        with open(self.lower_adc_channels_file_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                motor_number_position = line.find("M") + 1
                motor_adc_position = line.find(":") + 2
                motor_adc_str = line[motor_adc_position:motor_adc_position + 3]
                motor_number_str = line[motor_number_position]
                lower_adc_channels_dict[motor_number_str] = motor_adc_str

        self.manual_control.upper_set_rotation(upper_rotation_dict)
        self.pre_saved_moves.upper_set_rotation(upper_rotation_dict)
        self.upper_motors_rotation_dict = upper_rotation_dict

        self.manual_control.lower_set_rotation(lower_rotation_dict)
        self.pre_saved_moves.lower_set_rotation(lower_rotation_dict)
        self.lower_motors_rotation_dict = lower_rotation_dict

        self.manual_control.upper_set_finger(upper_finger_dict)
        self.pre_saved_moves.upper_set_finger(upper_finger_dict)
        self.upper_motors_finger_dict = upper_finger_dict

        self.manual_control.lower_set_finger(lower_finger_dict)
        self.pre_saved_moves.lower_set_finger(lower_finger_dict)
        self.lower_motors_finger_dict = lower_finger_dict

        self.upper_adc_channels_dict = upper_adc_channels_dict
        self.manual_control.upper_set_adc_channels(upper_adc_channels_dict)

        self.lower_adc_channels_dict = lower_adc_channels_dict
        self.manual_control.lower_set_adc_channels(lower_adc_channels_dict)

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
        self.__connect_upper_comport()

    def lower_update_comport_combo_box(self):
        current_index = self.lower_comport_comboBox.currentIndex()
        upper_combo_box_current_index = self.upper_comport_comboBox.currentIndex()
        self.lower_current_comport_name = get_comport_name(self.lower_comport_comboBox.currentText())

        self.upper_comport_comboBox.clear()
        self.upper_comport_comboBox.addItems(self.available_ports)
        self.upper_comport_comboBox.setCurrentIndex(upper_combo_box_current_index)
        self.upper_comport_comboBox.model().item(current_index).setFlags(QtCore.Qt.NoItemFlags)
        print(f"update_lower: Upper - {self.upper_current_comport_name}, Lower - {self.lower_current_comport_name}")
        self.__connect_lower_comport()

    def __connect_upper_comport(self):
        if self.upper_current_comport_name is None:
            self.main_logger.warning("Cannot connect: upper comport name is None")
        else:
            try:
                self.upper_current_comport = ComportInstance(self.upper_current_comport_name, 'Upper')
                self.upper_current_comport.set_command_log_file_path(self.command_log_file_path)
                if self.upper_current_comport.is_open:
                    self.command_master.set_upper_comport(self.upper_current_comport)
                    self.upper_collector.set_default_comport(self.upper_current_comport)
                    self.upper_collector_both.set_upper_comport_both(self.upper_current_comport)
                    self.upper_adc_collector.set_default_comport(self.upper_current_comport)
                    self.update_upper_status_label(True)
                else:
                    print('Upper comport is not open')
            except Exception as e:
                self.main_logger.warning(e)
                self.upper_current_comport_name = None

    def __connect_lower_comport(self):
        if self.lower_current_comport_name is None:
            self.main_logger.warning("Cannot connect: lower comport name is None")
        else:
            try:
                self.lower_current_comport = ComportInstance(self.lower_current_comport_name, 'Lower')
                self.lower_current_comport.set_command_log_file_path(self.command_log_file_path)
                if self.lower_current_comport.is_open:
                    self.command_master.set_lower_comport(self.lower_current_comport)
                    self.lower_collector.set_default_comport(self.lower_current_comport)
                    self.lower_collector_both.set_lower_comport_both(self.lower_current_comport)
                    self.lower_adc_collector.set_default_comport(self.lower_current_comport)
                    self.update_lower_status_label(True)
                else:
                    print('Lower comport is not open')
            except Exception as e:
                self.main_logger.warning(e)
                self.lower_current_comport_name = None

    def rescan_comport(self):
        if self.upper_current_comport:
            self.upper_current_comport.close_comport()
        if self.lower_current_comport:
            self.lower_current_comport.close_comport()

        self.upper_current_comport_name = None
        self.lower_current_comport_name = None

        self.upper_comport_comboBox.clear()
        self.lower_comport_comboBox.clear()

        self.available_ports = com.show_available_ports()
        self.upper_comport_comboBox.addItems(self.available_ports)
        self.lower_comport_comboBox.addItems(self.available_ports)

        self.update_upper_status_label(False)
        self.update_lower_status_label(False)
        self.main_logger.info("Rescan comports. Both ports are None now")

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

    def upper_check_motor_rotation(self):
        motor_number = self.upper_motors_comboBox.currentIndex() + 1  # Indexes start from 0. Motors start from 1
        pwm = self.upper_motor_pwm_scale.value()
        time_to_work = self.upper_time_input.toPlainText()
        reverse_flag = self.upper_reverse_motor_checkBox.isChecked()

        if reverse_flag:
            motor_byte_mode = self.upper_motors_rotation_dict[f'_{motor_number}']
        else:
            motor_byte_mode = self.upper_motors_rotation_dict[f'{motor_number}']

        motor_byte_base = '000'
        motor_byte = motor_byte_base + motor_byte_mode + self.upper_motors_finger_dict[f'{motor_number}']

        self.main_logger.debug(f'We about to check Upper Motor#{motor_number} rotation, motor_byte: {motor_byte}')
        self.command_master.send_command(part='Upper', config='00011110', motor_byte=motor_byte, pwm=pwm,
                                         work_time=time_to_work, delay='0.0', write_to_script_file=False)
        self.command_master.power_command(part='Upper', config='00000001', power_byte='00000001')

    def lower_check_motor_rotation(self):
        motor_number = self.lower_motors_comboBox.currentIndex() + 1  # Indexes start from 0. Motors start from 1
        pwm = self.lower_motor_pwm_scale.value()
        time_to_work = self.lower_time_input.toPlainText()
        reverse_flag = self.lower_reverse_motor_checkBox.isChecked()

        if reverse_flag:
            motor_byte_mode = self.lower_motors_rotation_dict[f'_{motor_number}']
        else:
            motor_byte_mode = self.lower_motors_rotation_dict[f'{motor_number}']

        motor_byte_base = '000'
        motor_byte = motor_byte_base + motor_byte_mode + self.lower_motors_finger_dict[f'{motor_number}']

        self.main_logger.debug(f'We about to check Lower Motor#{motor_number} rotation, motor_byte: {motor_byte}')
        self.command_master.send_command(part='Lower', config='00011110', motor_byte=motor_byte, pwm=pwm,
                                         work_time=time_to_work, delay='0.0', write_to_script_file=False)
        self.command_master.power_command(part='Lower', config='00000001', power_byte='00000001')

    def upper_apply_motor_rotation(self):
        motor_number = self.upper_motors_comboBox.currentIndex() + 1
        reverse_flag = self.upper_reverse_motor_checkBox.isChecked()
        warning_message = f'''Nothing to change: reverse flag - {reverse_flag}
Upper motor #{motor_number} has default settings'''
        if reverse_flag:
            motor_key_str = str(motor_number)
            temp = self.upper_motors_rotation_dict.get(motor_key_str)
            self.upper_motors_rotation_dict[motor_key_str] = self.upper_motors_rotation_dict[f'_{motor_key_str}']
            self.upper_motors_rotation_dict[f'_{motor_key_str}'] = temp
            print(self.upper_motors_rotation_dict)
        else:
            QMessageBox.warning(self, 'Warning', warning_message)

    def lower_apply_motor_rotation(self):
        motor_number = self.lower_motors_comboBox.currentIndex() + 1
        reverse_flag = self.lower_reverse_motor_checkBox.isChecked()
        warning_message = f'''Nothing to change: reverse flag - {reverse_flag}
Lower motor #{motor_number} has default settings'''
        if reverse_flag:
            motor_key_str = str(motor_number)
            temp = self.lower_motors_rotation_dict.get(motor_key_str)
            self.lower_motors_rotation_dict[motor_key_str] = self.lower_motors_rotation_dict[f'_{motor_key_str}']
            self.lower_motors_rotation_dict[f'_{motor_key_str}'] = temp
            print(self.lower_motors_rotation_dict)
        else:
            QMessageBox.warning(self, 'Warning', warning_message)

    def upper_discard_all_rotation_settings(self):
        self.upper_motors_rotation_dict = self.upper_motors_rotation_dict_default
        self.main_logger.debug("Roll back upper rotation dict to its default")

    def lower_discard_all_rotation_settings(self):
        self.lower_motors_rotation_dict = self.lower_motors_rotation_dict_default
        self.main_logger.debug("Roll back lower rotation dict to its default")

    def upper_discard_all_finger_settings(self):
        self.upper_motors_finger_dict = self.upper_motors_finger_dict_default
        self.main_logger.debug("Roll back upper finger dict to its default")

    def lower_discard_all_finger_settings(self):
        self.lower_motors_finger_dict = self.lower_motors_finger_dict_default
        self.main_logger.debug("Roll back lower finger dict to its default")

    def upper_check_motor_finger(self):
        motor_number = self.upper_motors_finger_comboBox.currentIndex() + 1
        motor_number_byte = self.upper_motor_number_input.toPlainText()

        motor_byte_base = '000'
        motor_byte = motor_byte_base + self.upper_motors_rotation_dict[f'{motor_number}'] + motor_number_byte

        self.main_logger.debug(f"We about to check Upper Motor-to-Finger #{motor_number}, motor_byte: {motor_byte}")
        self.command_master.send_command(part='Upper', config='00011110', motor_byte=motor_byte, pwm=15,
                                         work_time='1.0', delay='0.0', write_to_script_file=False)
        self.command_master.power_command(part='Upper', config='00000001', power_byte='00000001')

    def lower_check_motor_finger(self):
        motor_number = self.lower_motors_finger_comboBox.currentIndex() + 1
        motor_number_byte = self.lower_motor_number_input.toPlainText()

        motor_byte_base = '000'
        motor_byte = motor_byte_base + self.lower_motors_rotation_dict[f'{motor_number}'] + motor_number_byte

        self.main_logger.debug(f"We about to check Lower Motor-to-Finger #{motor_number}, motor_byte: {motor_byte}")
        self.command_master.send_command(part='Lower', config='00011110', motor_byte=motor_byte, pwm=15,
                                         work_time='1.0', delay='0.0', write_to_script_file=False)
        self.model.power_command(part='Lower', config='00000001', power_byte='00000001')

    def upper_apply_motor_finger(self):
        motor_number = str(self.upper_motors_finger_comboBox.currentIndex() + 1)
        motor_byte_number = self.upper_motor_number_input.toPlainText()
        print(f'Motor #{motor_number}, finger num: {motor_byte_number}')

        for key, value in self.upper_motors_finger_dict.items():
            if value == motor_byte_number:
                if key == motor_number:
                    print(f'Nothing to change: Motor #{motor_number} is already {motor_byte_number}')
                else:
                    temp = self.upper_motors_finger_dict[motor_number]
                    self.upper_motors_finger_dict[motor_number] = motor_byte_number
                    self.upper_motors_finger_dict[key] = temp
        print(self.upper_motors_finger_dict)

    def lower_apply_motor_finger(self):
        motor_number = str(self.lower_motors_finger_comboBox.currentIndex() + 1)
        motor_byte_number = self.lower_motor_number_input.toPlainText()
        print(f'Motor #{motor_number}, finger num: {motor_byte_number}')

        for key, value in self.lower_motors_finger_dict.items():
            if value == motor_byte_number:
                if key == motor_number:
                    print(f'Nothing to change: Motor #{motor_number} is already {motor_byte_number}')
                else:
                    temp = self.lower_motors_finger_dict[motor_number]
                    self.lower_motors_finger_dict[motor_number] = motor_byte_number
                    self.lower_motors_finger_dict[key] = temp
        print(self.lower_motors_finger_dict)

    # TODO: Need to finish ADC-check block. Display label doesn't work properly
    def upper_check_adc(self):
        motor_number = self.upper_motors_adc_test_comboBox.currentIndex() + 1
        adc_channel = self.upper_motors_adc_channel_comboBox.currentIndex()
        pwm = self.upper_motor_adc_test_pwm_scale.value()
        time_to_work = 2.0
        delay_before_work = 0.5
        motor_byte_base = '000'
        motor_rotation_mode = self.upper_motors_rotation_dict[f'{motor_number}']
        motor_finger_number = self.upper_motors_finger_dict[f'{motor_number}']
        motor_byte = motor_byte_base + motor_rotation_mode + motor_finger_number

        adc_decimal = 2 ** adc_channel
        self.upper_adc_collector.set_test_adc_byte_count(time_to_work=time_to_work)
        self.upper_adc_collector.set_test_adc_delay(delay_before_work=delay_before_work)
        self.command_master.upper_send_adc(adc_decimal=adc_decimal)
        self.command_master.send_command(part="Upper", config='00011110', motor_byte=motor_byte, pwm=pwm,
                                         work_time=time_to_work, delay=delay_before_work, write_to_script_file=False)

        self.upper_adc_test_thread.start()
        self.command_master.power_command(part='Upper', config='00000001', power_byte='00000001')

        self.command_master.clear_upper_command_list()

    # TODO: Finish this method according to upper_check_adc
    def lower_check_adc(self):
        motor_number = self.lower_motors_adc_test_comboBox.currentIndex() + 1
        adc_channel = self.lower_motors_adc_channel_comboBox.currentIndex()
        pwm = self.lower_motor_adc_test_pwm_scale.value()
        time_to_work = 1.0
        delay_before_work = 0.0
        motor_byte_base = '000'
        motor_rotation_mode = self.lower_motors_rotation_dict[f'{motor_number}']
        motor_finger_number = self.lower_motors_finger_dict[f'{motor_number}']  # string number 000, 001, 010 etc.
        motor_byte = motor_byte_base + motor_rotation_mode + motor_finger_number

        adc_decimal = 2 ** adc_channel
        self.lower_adc_collector.set_test_adc_byte_count(time_to_work=time_to_work)
        self.lower_adc_collector.set_test_adc_delay(delay_before_work=delay_before_work)
        self.command_master.lower_send_adc(adc_decimal=adc_decimal)
        self.command_master.send_command(part="Lower", config='00011110', motor_byte=motor_byte, pwm=pwm,
                                         work_time=time_to_work, delay=delay_before_work, write_to_script_file=False)

        self.lower_adc_test_thread.start()
        self.command_master.power_command(part='Lower', config='00000001', power_byte='00000001')

        self.command_master.clear_lower_command_list()

    def upper_setup_adc_test_thread(self):
        self.upper_adc_collector.moveToThread(self.upper_adc_test_thread)
        self.upper_adc_test_thread.started.connect(self.upper_adc_collector.simple_adc_test)
        self.upper_adc_collector.adc_check_complete.connect(self.upper_show_adc_test_data)
        self.upper_adc_collector.finished.connect(self.finish_upper_adc_test_thread)

    def lower_setup_adc_test_thread(self):
        self.lower_adc_collector.moveToThread(self.lower_adc_test_thread)
        self.lower_adc_test_thread.started.connect(self.lower_adc_collector.simple_adc_test)
        self.lower_adc_collector.adc_check_complete.connect(self.lower_show_adc_test_data)
        self.lower_adc_collector.finished.connect(self.finish_lower_adc_test_thread)

    def upper_show_adc_test_data(self):
        test_data = self.upper_adc_collector.get_test_data()
        text_to_show = ""
        for i in range(len(test_data)):
            text_to_show += str(test_data[i])
            text_to_show += " "
        self.upper_adc_test_data_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        self.upper_adc_test_data_label.setWordWrap(True)
        self.upper_adc_test_data_label.setText(text_to_show)

    def lower_show_adc_test_data(self):
        test_data = self.lower_adc_collector.get_test_data()
        text_to_show = ""
        for i in range(len(test_data)):
            text_to_show += str(test_data[i])
            text_to_show += " "
        self.lower_adc_test_data_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        self.lower_adc_test_data_label.setWordWrap(True)
        self.lower_adc_test_data_label.setText(text_to_show)

    def adc_label_place_default_text(self, part):
        default_text = "No data from"
        if part == 'Upper':
            ending = " UPPER Collector"
            self.upper_adc_test_data_label.setText(default_text + ending)
        elif part == 'Lower':
            ending = " LOWER Collector"
            self.lower_adc_test_data_label.setText(default_text + ending)
        else:
            print(f'place_default_text - No such part: {part}')

    def finish_upper_adc_test_thread(self):
        print('finishing the thread')
        self.upper_adc_test_thread.quit()
        self.command_master.release_upper_comport_after_thread()

    def finish_lower_adc_test_thread(self):
        print('finishing the thread')
        self.lower_adc_test_thread.quit()
        self.command_master.release_lower_comport_after_thread()

    def upper_apply_adc_data(self):
        motor_number = str(self.upper_motors_adc_test_comboBox.currentIndex() + 1)
        adc_channel = str(self.upper_motors_adc_channel_comboBox.currentIndex())
        print(f'Upper ADC -> Motor #{motor_number}, adc channel: {adc_channel}')

        for key, value in self.upper_adc_channels_dict.items():
            if value == adc_channel:
                if key == motor_number:
                    print(f'Nothing to change: Motor #{motor_number} is already {adc_channel}')
                else:
                    temp = self.upper_adc_channels_dict[motor_number]
                    self.upper_adc_channels_dict[motor_number] = adc_channel
                    self.upper_adc_channels_dict[key] = temp
        print(self.upper_adc_channels_dict)

    def lower_apply_adc_data(self):
        motor_number = str(self.lower_motors_adc_test_comboBox.currentIndex() + 1)
        adc_channel = str(self.lower_motors_adc_channel_comboBox.currentIndex())
        print(f'Lower ADC -> Motor #{motor_number}, adc channel: {adc_channel}')

        for key, value in self.lower_adc_channels_dict.items():
            if value == adc_channel:
                if key == motor_number:
                    print(f'Nothing to change: Motor #{motor_number} is already {adc_channel}')
                else:
                    temp = self.lower_adc_channels_dict[motor_number]
                    self.lower_adc_channels_dict[motor_number] = adc_channel
                    self.lower_adc_channels_dict[key] = temp
        print(self.lower_adc_channels_dict)

    def upper_discard_adc_data(self):
        self.upper_adc_test_data_label.clear()
        self.adc_label_place_default_text('Upper')
        self.upper_adc_collector.clear_test_data()

    def lower_discard_adc_data(self):
        self.lower_adc_test_data_label.clear()
        self.adc_label_place_default_text('Lower')
        self.lower_adc_collector.clear_test_data()

    def update_upper_adc_pwm_label(self, value):
        self.upper_motor_adc_test_pwm_label.setText(str(value))

    def update_lower_adc_pwm_label(self, value):
        self.lower_motor_adc_test_pwm_label.setText(str(value))

    # Methods to OPEN settings file. Prepare it for further work
    def upper_open_rotation_file(self):
        window_name = "Open File (Upper rotation)"
        search_dir = "../../Data/"
        file_path, _ = QFileDialog.getOpenFileName(self, window_name, search_dir, "Text Files (*.txt)")
        if file_path:
            self.upper_rotation_file_path_label.setText(file_path)
            self.upper_rotation_file_path = file_path

    def lower_open_rotation_file(self):
        window_name = "Open File (Lower rotation)"
        search_dir = "../../Data/"
        file_path, _ = QFileDialog.getOpenFileName(self, window_name, search_dir, "Text Files (*.txt)")
        if file_path:
            self.lower_rotation_file_path_label.setText(file_path)
            self.lower_rotation_file_path = file_path

    def upper_open_finger_file(self):
        window_name = "Open File (Upper finger)"
        search_dir = "../../Data/"
        file_path, _ = QFileDialog.getOpenFileName(self, window_name, search_dir, "Text Files (*.txt)")
        if file_path:
            self.upper_finger_file_path_label.setText(file_path)
            self.upper_finger_file_path = file_path

    def lower_open_finger_file(self):
        window_name = "Open File (Lower finger)"
        search_dir = "../../Data/"
        file_path, _ = QFileDialog.getOpenFileName(self, window_name, search_dir, "Text Files (*.txt)")
        if file_path:
            self.lower_finger_file_path_label.setText(file_path)
            self.lower_finger_file_path = file_path

    def upper_open_adc_file(self):
        window_name = "Open File (Upper ADC)"
        search_dir = "../../Data/"
        file_path, _ = QFileDialog.getOpenFileName(self, window_name, search_dir, "Text Files (*.txt)")
        if file_path:
            self.upper_adc_channels_file_path_label.setText(file_path)
            self.upper_adc_channels_file_path = file_path

    def lower_open_adc_file(self):
        window_name = "Open File (Lower ADC)"
        search_dir = "../../Data/"
        file_path, _ = QFileDialog.getOpenFileName(self, window_name, search_dir, "Text Files (*.txt)")
        if file_path:
            self.lower_adc_channels_file_path_label.setText(file_path)
            self.lower_adc_channels_file_path = file_path

    # Methods to WRITE settings to the selected file path
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

    def upper_override_adc_file(self):
        with open(self.upper_adc_channels_file_path, 'w') as f:
            for item in self.upper_adc_channels_dict.items():
                target_str = f'M{item[0]}: {item[1]}'
                f.write(target_str + '\n')

    def lower_override_adc_file(self):
        with open(self.lower_adc_channels_file_path, 'w') as f:
            for item in self.lower_adc_channels_dict.items():
                target_str = f'M{item[0]}: {item[1]}'
                f.write(target_str + '\n')

    # Methods to LOAD settings from files
    def upper_load_rotation(self):
        if self.upper_rotation_file_path is None:
            QMessageBox.warning(self, 'Warning', "Upper rotation file path is empty")
            return None
        upper_rotation_dict = dict()
        with open(self.upper_rotation_file_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                motor_number_position = line.find("M") + 1
                motor_rotation_position = line.find(":") + 2
                motor_rotation_str = line[motor_rotation_position:motor_rotation_position + 2]
                if line[motor_number_position] == '_':
                    motor_number_str = line[motor_number_position:motor_number_position + 2]
                else:
                    motor_number_str = line[motor_number_position]
                upper_rotation_dict[motor_number_str] = motor_rotation_str
        self.manual_control.upper_set_rotation(upper_rotation_dict)
        self.upper_motors_rotation_dict = upper_rotation_dict

    def lower_load_rotation(self):
        if self.lower_rotation_file_path is None:
            QMessageBox.warning(self, 'Warning', "Lower rotation file path is empty")
            return None
        lower_rotation_dict = dict()
        with open(self.lower_rotation_file_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                motor_number_position = line.find("M") + 1
                motor_rotation_position = line.find(":") + 2
                motor_rotation_str = line[motor_rotation_position:motor_rotation_position + 2]
                if line[motor_number_position] == '_':
                    motor_number_str = line[motor_number_position:motor_number_position + 2]
                else:
                    motor_number_str = line[motor_number_position]
                lower_rotation_dict[motor_number_str] = motor_rotation_str
        self.manual_control.lower_set_rotation(lower_rotation_dict)
        self.lower_motors_rotation_dict = lower_rotation_dict

    def upper_load_finger(self):
        if self.upper_finger_file_path is None:
            QMessageBox.warning(self, 'Warning', "Upper finger file path is empty")
            return None
        upper_finger_dict = dict()
        with open(self.upper_finger_file_path, 'r') as f:
            lines = f.readlines()
            print(f'Number of lines: {len(lines)}')
            for line in lines:
                motor_number_position = line.find("M") + 1
                motor_finger_position = line.find(":") + 2
                motor_finger_str = line[motor_finger_position:motor_finger_position + 3]
                motor_number_str = line[motor_number_position]
                upper_finger_dict[motor_number_str] = motor_finger_str
        self.manual_control.upper_set_finger(upper_finger_dict)
        self.upper_motors_finger_dict = upper_finger_dict

    def lower_load_finger(self):
        if self.lower_finger_file_path is None:
            QMessageBox.warning(self, 'Warning', "Lower finger file path is empty")
            return None
        lower_finger_dict = dict()
        with open(self.lower_finger_file_path, 'r') as f:
            lines = f.readlines()
            print(f'Number of lines: {len(lines)}')
            for line in lines:
                motor_number_position = line.find("M") + 1
                motor_finger_position = line.find(":") + 2
                motor_finger_str = line[motor_finger_position:motor_finger_position + 3]
                motor_number_str = line[motor_number_position]
                lower_finger_dict[motor_number_str] = motor_finger_str
        self.manual_control.lower_set_finger(lower_finger_dict)
        self.lower_motors_finger_dict = lower_finger_dict

    def upper_load_adc(self):
        if self.upper_adc_channels_file_path is None:
            QMessageBox.warning(self, 'Warning', "Upper ADC file path is empty")
            return None
        upper_adc_dict = dict()
        with open(self.upper_adc_channels_file_path, 'r') as f:
            lines = f.readlines()
            print(f'Number of lines: {len(lines)}')
            for line in lines:
                motor_number_position = line.find("M") + 1
                motor_adc_position = line.find(":") + 2
                motor_adc_str = line[motor_adc_position:motor_adc_position + 3]
                motor_number_str = line[motor_number_position]
                upper_adc_dict[motor_number_str] = motor_adc_str
        self.manual_control.upper_set_finger(upper_adc_dict)
        self.upper_adc_channels_dict = upper_adc_dict

    def lower_load_adc(self):
        if self.lower_adc_channels_file_path is None:
            QMessageBox.warning(self, 'Warning', "Lower ADC file path is empty")
            return None
        lower_adc_dict = dict()
        with open(self.lower_adc_channels_file_path, 'r') as f:
            lines = f.readlines()
            print(f'Number of lines: {len(lines)}')
            for line in lines:
                motor_number_position = line.find("M") + 1
                motor_adc_position = line.find(":") + 2
                motor_adc_str = line[motor_adc_position:motor_adc_position + 3]
                motor_number_str = line[motor_number_position]
                lower_adc_dict[motor_number_str] = motor_adc_str
        self.manual_control.lower_set_finger(lower_adc_dict)
        self.lower_adc_channels_dict = lower_adc_dict

    def settings_from_file_init(self):
        text_to_show = ""
        text_to_show += "Upper motor-to-finger settings:\n"
        for key, value in self.upper_motors_finger_dict.items():
            text_to_show += f"{key}) {value}\n"

        text_to_show += "\nLower motor-to-finger settings:\n"
        for key, value in self.lower_motors_finger_dict.items():
            text_to_show += f"{key}) {value}\n"

        self.settings_from_file_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        self.settings_from_file_label.setWordWrap(True)
        self.settings_from_file_label.setText(text_to_show)

    def closeEvent(self, event):
        self.main_logger.info("Application is closed")
        if self.upper_current_comport_name:
            self.upper_current_comport.write_command_log({'service_msg': "Stop Session"}, 'SERVICE')
        if self.lower_current_comport_name:
            self.lower_current_comport.write_command_log({'service_msg': "Stop Session"}, 'SERVICE')
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApplication()
    window.show()
    sys.exit(app.exec_())
