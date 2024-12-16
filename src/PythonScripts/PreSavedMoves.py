import time
import PreSavedMovesUi
from logging import getLogger
from CommandMaster import CommandMaster
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox


def str_to_bytearray(hex_string):
    stripped_str = hex_string[2:-1]  # Remove 'U('/'L(' and ')' from command. See data files
    # Split the string (1e 0c 35 etc.) into a list of hex values [1e, 0c, 35, etc.]
    hex_values = stripped_str.split()
    # Convert each hex value back to its original byte representation using fromhex()
    bytes_list = [bytes.fromhex(hex_value) for hex_value in hex_values]
    # Concatenate the byte values into a single bytearray
    original_bytearray = bytearray().join(bytes_list)
    return original_bytearray


def get_particular_byte(hex_string: int, target_byte: int) -> int | None:
    if 0 <= target_byte <= 4:
        stripped_str = hex_string[2:-1]  # Remove 'U('/'L(' and ')' from command. See data files
        # Split the string (1e 0c 35 etc.) into a list of hex values [1e, 0c, 35, etc.]
        hex_values = stripped_str.split()
        return int(hex_values[target_byte], 16)
    else:
        print(f"PreSavedMoves/get_particular_byte: No such byte in sequence: {target_byte}")
        return None


def decimal_int_to_binary_str(decimal_int):
    total = ""
    while decimal_int > 0:
        if decimal_int % 2 == 0:
            total += '0'
            decimal_int /= 2
        else:
            total += '1'
            decimal_int //= 2
    target_line = total[::-1]

    # return string representation of given int into byte e.g. 00110101
    return target_line.zfill(8)


def str_to_byte(hex_string):
    return bytes.fromhex(hex_string)


class PreSavedMoves(QMainWindow, PreSavedMovesUi.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.logger = getLogger(__name__)
        self.command_master = None
        self.move_script_file_path = None
        self.default_move_script_text = "Move script is now empty"
        self.place_default_text()

        self.open_script_file_btn.clicked.connect(self.open_move_script)
        self.load_script_file_btn.clicked.connect(self.load_move_script)

        self.send_full_sequence_btn.clicked.connect(self.start_full_sequence_thread)
        self.send_full_sequence_thread = QtCore.QThread()
        self.send_sequence_manager = self.__SendSequenceManager(self.logger)
        self.send_sequence_manager.moveToThread(self.send_full_sequence_thread)
        self.send_full_sequence_thread.started.connect(self.send_sequence_manager.send_full_sequence)
        self.send_sequence_manager.finished.connect(self.finish_full_sequence_thread)

        self.send_next_command_btn.clicked.connect(self.send_next_command)

        self.current_cursor_position = 0
        self.previous_cursor_position = 0

        # Tense Fingers connections block
        self.tense_finger_pwm_scale.valueChanged.connect(self.update_tense_finger_pwm_label)
        self.tense_finger_comboBox.addItems(['Thumb', 'Index', 'Middle', 'Ring', 'Pinky'])
        self.tense_finger_btn.clicked.connect(self.tense_finger_command)
        self.release_finger_btn.clicked.connect(self.release_finger_command)
        self.upper_rotation_dict = dict()
        self.lower_rotation_dict = dict()
        self.upper_finger_dict = dict()
        self.lower_finger_dict = dict()

    def upper_set_rotation(self, rotation_dict):
        for key, value in rotation_dict.items():
            self.upper_rotation_dict[key] = value
        self.logger.info("Upper rotation dict is set")

    def lower_set_rotation(self, rotation_dict):
        for key, value in rotation_dict.items():
            self.lower_rotation_dict[key] = value
        self.logger.info("Lower rotation dict is set")

    def upper_set_finger(self, finger_dict):
        for key, value in finger_dict.items():
            self.upper_finger_dict[key] = value
        self.logger.info("Upper motor-to-finger dict is set")

    def lower_set_finger(self, finger_dict):
        for key, value in finger_dict.items():
            self.lower_finger_dict[key] = value
        self.logger.info("Lower motor-to-finger dict is set")

    def set_command_master(self, master: CommandMaster):
        self.command_master = master
        self.send_sequence_manager.set_command_master(command_master=master)

    def place_default_text(self):
        self.move_script_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        self.move_script_label.setWordWrap(True)
        self.move_script_label.setText(self.default_move_script_text)

    def open_move_script(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "../../Data/", "Text Files (*.txt)")
        if file_path:
            self.script_file_path_label.setText(file_path)
            self.move_script_file_path = file_path

    def load_move_script(self):
        if self.move_script_file_path is None:
            QMessageBox.warning(self, 'Warning', 'Undefined file location')
        else:
            with open(self.move_script_file_path, 'r') as file:
                text = file.read()
                self.move_script_label.setText(text)
            # QMessageBox.information(self, 'Success', 'Data successfully saved!')

    def start_full_sequence_thread(self):
        if not self.send_full_sequence_thread.isRunning():
            self.logger.info(f"Send-Full-Sequence-Thread Started")
            self.send_sequence_manager.set_sequence_text(sequence_text=self.move_script_label.text())
            self.send_full_sequence_thread.start()
        else:
            self.logger.warning(f"Attempt to start Send-Full-Sequence-Thread. Thread is already running")

    def finish_full_sequence_thread(self, finish_message):
        if self.send_full_sequence_thread.isRunning():
            self.logger.info(f"Send-Full-Sequence-Thread finished with message: {finish_message}")
            self.send_full_sequence_thread.quit()
        else:
            self.logger.warning(f"Attempt to quit Send-Full-Sequence-Thread. Thread not running right now")

    # TODO: It probably works bad. Need to finish it sometimes
    def send_next_command(self):
        if self.model is None:
            QMessageBox.warning(self, 'Warning', 'Model is undefined.\nCould not use COMPORTs')
        else:
            full_text_bytes = self.move_script_label.text()
            if self.current_cursor_position == len(full_text_bytes):
                QMessageBox.warning(self, 'Warning', 'All commands already sent\nSetting cursor at the start')
                self.current_cursor_position = 0
                self.previous_cursor_position = 0
            else:
                self.current_cursor_position += 34  # 30 - It's length of string with two commands in it (upper and lower)
                text_bytes = full_text_bytes[:self.current_cursor_position]
                upper_command_str = text_bytes[self.previous_cursor_position:self.previous_cursor_position + 17]
                upper_command = str_to_bytearray(upper_command_str)
                self.command_master.send_command_bytes('Upper', upper_command)

                lower_command_str = text_bytes[self.previous_cursor_position + 17:self.previous_cursor_position + 34]
                lower_command = str_to_bytearray(lower_command_str)
                self.command_master.send_command_bytes('Lower', lower_command)

                self.command_master.power_command('Upper', config='00000001', power_byte='00000001')
                self.command_master.power_command('Lower', config='00000001', power_byte='00000001')

                self.previous_cursor_position = self.current_cursor_position

    def tense_finger_command(self):
        current_finger_index = self.tense_finger_comboBox.currentIndex()
        motor_byte_base = '000'
        upper_motor_byte = ''
        lower_motor_byte = ''
        if current_finger_index == 0:
            self.logger.info("Tense thumb finger")
            upper_motor_rotation_byte = self.upper_rotation_dict.get('1')
            upper_motor_number_byte = self.upper_finger_dict.get('1')
            upper_motor_byte = motor_byte_base + upper_motor_rotation_byte + upper_motor_number_byte

            lower_motor_rotation_byte = self.lower_rotation_dict.get('1')
            lower_motor_number_byte = self.lower_finger_dict.get('1')
            lower_motor_byte = motor_byte_base + lower_motor_rotation_byte + lower_motor_number_byte
        elif current_finger_index == 1:
            self.logger.info("Tense index finger")
            upper_motor_rotation_byte = self.upper_rotation_dict.get('2')
            upper_motor_number_byte = self.upper_finger_dict.get('2')
            upper_motor_byte = motor_byte_base + upper_motor_rotation_byte + upper_motor_number_byte

            lower_motor_rotation_byte = self.lower_rotation_dict.get('2')
            lower_motor_number_byte = self.lower_finger_dict.get('2')
            lower_motor_byte = motor_byte_base + lower_motor_rotation_byte + lower_motor_number_byte
        elif current_finger_index == 2:
            self.logger.info("Tense middle finger")
            upper_motor_rotation_byte = self.upper_rotation_dict.get('3')
            upper_motor_number_byte = self.upper_finger_dict.get('3')
            upper_motor_byte = motor_byte_base + upper_motor_rotation_byte + upper_motor_number_byte

            lower_motor_rotation_byte = self.lower_rotation_dict.get('3')
            lower_motor_number_byte = self.lower_finger_dict.get('3')
            lower_motor_byte = motor_byte_base + lower_motor_rotation_byte + lower_motor_number_byte
        elif current_finger_index == 3:
            self.logger.info("Tense ring finger")
            upper_motor_rotation_byte = self.upper_rotation_dict.get('4')
            upper_motor_number_byte = self.upper_finger_dict.get('4')
            upper_motor_byte = motor_byte_base + upper_motor_rotation_byte + upper_motor_number_byte

            lower_motor_rotation_byte = self.lower_rotation_dict.get('4')
            lower_motor_number_byte = self.lower_finger_dict.get('4')
            lower_motor_byte = motor_byte_base + lower_motor_rotation_byte + lower_motor_number_byte
        elif current_finger_index == 4:
            self.logger.info("Tense pinky finger")
            upper_motor_rotation_byte = self.upper_rotation_dict.get('5')
            upper_motor_number_byte = self.upper_finger_dict.get('5')
            upper_motor_byte = motor_byte_base + upper_motor_rotation_byte + upper_motor_number_byte

            lower_motor_rotation_byte = self.lower_rotation_dict.get('5')
            lower_motor_number_byte = self.lower_finger_dict.get('5')
            lower_motor_byte = motor_byte_base + lower_motor_rotation_byte + lower_motor_number_byte
        else:
            self.logger.warning(f"Tense finger. Unknown finger index: {current_finger_index}")

        pwm = self.tense_finger_pwm_scale.value()
        tense_time = self.tense_finger_time_input.toPlainText()
        if upper_motor_byte != '' and lower_motor_byte != '':
            self.command_master.send_command(part='Upper', config='00011110', motor_byte=upper_motor_byte, pwm=pwm,
                                             work_time=tense_time, delay='0.0', write_to_script_file=False,
                                             command_type='TENSE')
            self.command_master.send_command(part='Lower', config='00001110', motor_byte=lower_motor_byte, pwm=pwm,
                                             work_time=tense_time, delay='0.0', write_to_script_file=False,
                                             command_type='TENSE')
            self.command_master.power_command('Upper', config='00000001', power_byte='00000001')
            self.command_master.power_command('Lower', config='00000001', power_byte='00000001')
        else:
            self.logger.warning(f"Unable to tense finger - motor bytes are empty: upper->{upper_motor_byte}"
                                f"lower->{lower_motor_byte}")

    def release_finger_command(self):
        current_finger_index = self.tense_finger_comboBox.currentIndex()
        motor_byte_base = '000'
        upper_motor_byte = ''
        lower_motor_byte = ''
        if current_finger_index == 0:
            self.logger.info("Release thumb finger")
            upper_motor_rotation_byte = self.upper_rotation_dict.get('_1')
            upper_motor_number_byte = self.upper_finger_dict.get('1')
            upper_motor_byte = motor_byte_base + upper_motor_rotation_byte + upper_motor_number_byte

            lower_motor_rotation_byte = self.lower_rotation_dict.get('_1')
            lower_motor_number_byte = self.lower_finger_dict.get('1')
            lower_motor_byte = motor_byte_base + lower_motor_rotation_byte + lower_motor_number_byte
        elif current_finger_index == 1:
            self.logger.info("Release index finger")
            upper_motor_rotation_byte = self.upper_rotation_dict.get('_2')
            upper_motor_number_byte = self.upper_finger_dict.get('2')
            upper_motor_byte = motor_byte_base + upper_motor_rotation_byte + upper_motor_number_byte

            lower_motor_rotation_byte = self.lower_rotation_dict.get('_2')
            lower_motor_number_byte = self.lower_finger_dict.get('2')
            lower_motor_byte = motor_byte_base + lower_motor_rotation_byte + lower_motor_number_byte
        elif current_finger_index == 2:
            self.logger.info("Release middle finger")
            upper_motor_rotation_byte = self.upper_rotation_dict.get('_3')
            upper_motor_number_byte = self.upper_finger_dict.get('3')
            upper_motor_byte = motor_byte_base + upper_motor_rotation_byte + upper_motor_number_byte

            lower_motor_rotation_byte = self.lower_rotation_dict.get('_3')
            lower_motor_number_byte = self.lower_finger_dict.get('3')
            lower_motor_byte = motor_byte_base + lower_motor_rotation_byte + lower_motor_number_byte
        elif current_finger_index == 3:
            self.logger.info("Release ring finger")
            upper_motor_rotation_byte = self.upper_rotation_dict.get('_4')
            upper_motor_number_byte = self.upper_finger_dict.get('4')
            upper_motor_byte = motor_byte_base + upper_motor_rotation_byte + upper_motor_number_byte

            lower_motor_rotation_byte = self.lower_rotation_dict.get('_4')
            lower_motor_number_byte = self.lower_finger_dict.get('4')
            lower_motor_byte = motor_byte_base + lower_motor_rotation_byte + lower_motor_number_byte
        elif current_finger_index == 4:
            self.logger.info("Release pinky finger")
            upper_motor_rotation_byte = self.upper_rotation_dict.get('_5')
            upper_motor_number_byte = self.upper_finger_dict.get('5')
            upper_motor_byte = motor_byte_base + upper_motor_rotation_byte + upper_motor_number_byte

            lower_motor_rotation_byte = self.lower_rotation_dict.get('_5')
            lower_motor_number_byte = self.lower_finger_dict.get('5')
            lower_motor_byte = motor_byte_base + lower_motor_rotation_byte + lower_motor_number_byte
        else:
            self.logger.warning(f"Release finger. Unknown finger index: {current_finger_index}")

        pwm = 13
        release_time = '0.2'
        if upper_motor_byte != '' and lower_motor_byte != '':
            self.command_master.send_command(part='Upper', config='00011110', motor_byte=upper_motor_byte, pwm=pwm,
                                             work_time=release_time, delay='0.0', write_to_script_file=False,
                                             command_type='RELEASE')
            self.command_master.send_command(part='Lower', config='00011110', motor_byte=lower_motor_byte, pwm=pwm,
                                             work_time=release_time, delay='0.0', write_to_script_file=False,
                                             command_type='RELEASE')
            self.command_master.power_command('Upper', config='00000001', power_byte='00000001')
            self.command_master.power_command('Lower', config='00000001', power_byte='00000001')
        else:
            self.logger.warning(f"Unable to release finger - motor bytes are empty: upper->{upper_motor_byte}"
                                f"lower->{lower_motor_byte}")

    def update_tense_finger_pwm_label(self, value):
        self.tense_finger_pwm_label.setText(str(value))

    # Inner class for sending command sequences. Needed for prevent main app freezing (use QThread)
    class __SendSequenceManager(QtCore.QObject):
        finished = QtCore.pyqtSignal(str)

        def __init__(self, logger):
            super().__init__()
            self.command_master = None
            self.commands_sequence = None
            self.logger = logger

        def set_command_master(self, command_master):
            self.command_master = command_master

        def set_sequence_text(self, sequence_text: str):
            self.commands_sequence = sequence_text

        def send_full_sequence(self):
            self.logger.debug("SendSequenceManager start sending full sequence")
            if self.command_master is None:
                self.finished.emit("ERROR - Command Master is None")
                return None
            if self.commands_sequence == "Move script is now empty" or self.commands_sequence is None:
                self.finished.emit("ERROR - Commands Sequence is None")
                return None
            upper_commands_list = []
            lower_commands_list = []
            upper_motor_bytes = []
            lower_motor_bytes = []
            upper_pwm = []
            lower_pwm = []
            upper_time_delay = []
            lower_time_delay = []

            # Obtaining commands from text data. Store them to upper_command_list and lower_commands_list
            for i in range(0, len(self.commands_sequence), 17):
                command_str = self.commands_sequence[i:i + 17]
                command_motor_byte = get_particular_byte(hex_string=command_str, target_byte=1)
                command_pwm = get_particular_byte(hex_string=command_str, target_byte=2)
                command_time = get_particular_byte(hex_string=command_str, target_byte=3)
                command_delay = get_particular_byte(hex_string=command_str, target_byte=4)
                if "U" in command_str:
                    command_byte = str_to_bytearray(command_str)
                    upper_commands_list.append(command_byte)

                    upper_motor_byte_str = decimal_int_to_binary_str(command_motor_byte)
                    upper_motor_bytes.append(upper_motor_byte_str)
                    upper_pwm.append(command_pwm)
                    upper_time_delay.append((command_time, command_delay))
                elif "L" in command_str:
                    command_byte = str_to_bytearray(command_str)
                    lower_commands_list.append(command_byte)

                    lower_motor_byte_str = decimal_int_to_binary_str(command_motor_byte)
                    lower_motor_bytes.append(lower_motor_byte_str)
                    lower_pwm.append(command_pwm)
                    lower_time_delay.append((command_time, command_delay))
                else:
                    self.logger.warning(f"Unknown command in script: {command_str}")

            # Actually sending command pair-by-pair (Upper and Lower)
            for i, pair in enumerate(zip(upper_commands_list, lower_commands_list)):
                upper_time = round(upper_time_delay[i][0] * 0.1, 1)
                upper_delay = round(upper_time_delay[i][1] * 0.1, 1)
                lower_time = round(lower_time_delay[i][0] * 0.1, 1)
                lower_delay = round(lower_time_delay[i][1] * 0.1, 1)
                max_time = max(upper_time, lower_time)
                max_delay = max(upper_delay, lower_delay)
                self.command_master.send_command_bytes('Upper', pair[0])
                self.command_master.send_command_bytes('Lower', pair[1])
                self.command_master.power_command('Upper', config='00000001', power_byte='00000001')
                self.command_master.power_command('Lower', config='00000001', power_byte='00000001')

                if i == (len(upper_commands_list) - 1):  # If last command was sent, then send hard-stop command
                    time.sleep(max_time + max_delay)
                    self.send_hard_stop_command('Upper', upper_motor_bytes[i])
                    self.send_hard_stop_command('Lower', lower_motor_bytes[i])
                else:
                    time.sleep(max_time + max_delay)
            self.logger.debug("SendSequenceManager finish sending full sequence")
            self.finished.emit("Thread finished successfully")

        #  Experimental command. Instantly stop the motor and hold it.
        def send_hard_stop_command(self, part: str, motor_byte: str):
            motor_byte_base = '000'
            motor_rotation_byte = '11'  # New Experimental command type
            motor_number_str = motor_byte[-3:]
            motor_byte = motor_byte_base + motor_rotation_byte + motor_number_str
            self.logger.debug(f"Hard-Stop for {part}, motor_byte={motor_byte}")
            if part == 'Upper':
                self.command_master.send_command(part='Upper', config='00011110', motor_byte=motor_byte, pwm=100,
                                                 work_time='1.0', delay='0.0')
            elif part == 'Lower':
                self.command_master.send_command(part='Lower', config='00011110', motor_byte=motor_byte, pwm=100,
                                                 work_time='1.0', delay='0.0')
            else:
                self.logger.warning(f"Unknown part (hard-stop): {part}")