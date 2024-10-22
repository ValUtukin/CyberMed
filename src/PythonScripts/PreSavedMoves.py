import sys
import PreSavedMovesUi
from CommandMaster import CommandMaster
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox


def str_to_bytearray(hex_string):
    stripped_str = hex_string[2:-1]  # Remove 'U('/'L(' and ')' from command. See data files
    # Split the string (1e 0c 35 etc.) into a list of hex values [1e, 0c, 35, etc.]
    hex_values = stripped_str.split()
    # Convert each hex value back to its original byte representation using fromhex()
    bytes_list = [bytes.fromhex(hex_value) for hex_value in hex_values]
    # Concatenate the byte values into a single bytearray
    original_bytearray = bytearray().join(bytes_list)
    return original_bytearray


def str_to_byte(hex_string):
    return bytes.fromhex(hex_string)


class PreSavedMoves(QtWidgets.QMainWindow, PreSavedMovesUi.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.command_master = None
        self.move_script_file_path = None
        self.default_move_script_text = "Move script is now empty"
        self.place_default_text()

        self.open_script_file_btn.clicked.connect(self.open_move_script)
        self.load_script_file_btn.clicked.connect(self.load_move_script)
        self.send_full_sequence_btn.clicked.connect(self.send_full_sequence)
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
        print("PreSavedMoves/upper_set_rotation - get a rotation dict:")
        for key, value in rotation_dict.items():
            self.upper_rotation_dict[key] = value
        print(self.upper_rotation_dict)

    def lower_set_rotation(self, rotation_dict):
        print("PreSavedMoves/lower_set_rotation - get a rotation dict:")
        for key, value in rotation_dict.items():
            self.lower_rotation_dict[key] = value
        print(self.lower_rotation_dict)

    def upper_set_finger(self, finger_dict):
        print("PreSavedMoves/upper_set_finger - get a finger dict:")
        for key, value in finger_dict.items():
            self.upper_finger_dict[key] = value
        print(self.upper_finger_dict)

    def lower_set_finger(self, finger_dict):
        print("PreSavedMoves/lower_set_finger - get a finger dict:")
        for key, value in finger_dict.items():
            self.lower_finger_dict[key] = value
        print(self.lower_finger_dict)

    def set_command_master(self, master: CommandMaster):
        self.command_master = master

    def place_default_text(self):
        self.move_script_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        self.move_script_label.setWordWrap(True)
        self.move_script_label.setText(self.default_move_script_text)

    def open_move_script(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "../../../Data/", "Text Files (*.txt)")
        if file_path:
            self.script_file_path_label.setText(file_path)
            self.move_script_file_path = file_path

    def load_move_script(self):
        if self.move_script_file_path is None:
            QMessageBox.warning(self, 'Warning', 'Undefined file location')
        else:
            with open(self.move_script_file_path, 'r') as file:
                file_data = file.read()
                self.move_script_label.setText(file_data)
                file.close()
            # QMessageBox.information(self, 'Success', 'Data successfully saved!')

    # TODO: Data can be loaded from the file. Need to do data transition!
    def send_full_sequence(self):
        text_bytes = self.move_script_label.text()
        part_flag = True  # True - upper part, False - lower part
        for i in range(0, len(text_bytes), 17):
            command_str = text_bytes[i:i + 17]
            command_byte = str_to_bytearray(command_str)
            print(f'Command {command_byte}, type {type(command_byte)}, len {len(command_byte)}')
            if part_flag:
                self.command_master.send_command_bytes('Upper', command_byte)
                part_flag = False
            else:
                self.command_master.send_command_bytes('Lower', command_byte)
                part_flag = True
        part_flag = True  # Set flag back to True. Just in case
        self.command_master.power_command('Upper', config='00000001', power_byte='00000001')
        self.command_master.power_command('Lower', config='00000001', power_byte='00000001')

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
            print('Tense - Thumb')
            upper_motor_rotation_byte = self.upper_rotation_dict.get('1')
            upper_motor_number_byte = self.upper_finger_dict.get('1')
            upper_motor_byte = motor_byte_base + upper_motor_rotation_byte + upper_motor_number_byte

            lower_motor_rotation_byte = self.lower_rotation_dict.get('1')
            lower_motor_number_byte = self.lower_finger_dict.get('1')
            lower_motor_byte = motor_byte_base + lower_motor_rotation_byte + lower_motor_number_byte
        elif current_finger_index == 1:
            print('Tense - Index')
            upper_motor_rotation_byte = self.upper_rotation_dict.get('2')
            upper_motor_number_byte = self.upper_finger_dict.get('2')
            upper_motor_byte = motor_byte_base + upper_motor_rotation_byte + upper_motor_number_byte

            lower_motor_rotation_byte = self.lower_rotation_dict.get('2')
            lower_motor_number_byte = self.lower_finger_dict.get('2')
            lower_motor_byte = motor_byte_base + lower_motor_rotation_byte + lower_motor_number_byte
        elif current_finger_index == 2:
            print('Tense - Middle')
            upper_motor_rotation_byte = self.upper_rotation_dict.get('3')
            upper_motor_number_byte = self.upper_finger_dict.get('3')
            upper_motor_byte = motor_byte_base + upper_motor_rotation_byte + upper_motor_number_byte

            lower_motor_rotation_byte = self.lower_rotation_dict.get('3')
            lower_motor_number_byte = self.lower_finger_dict.get('3')
            lower_motor_byte = motor_byte_base + lower_motor_rotation_byte + lower_motor_number_byte
        elif current_finger_index == 3:
            print('Tense - Ring')
            upper_motor_rotation_byte = self.upper_rotation_dict.get('4')
            upper_motor_number_byte = self.upper_finger_dict.get('4')
            upper_motor_byte = motor_byte_base + upper_motor_rotation_byte + upper_motor_number_byte

            lower_motor_rotation_byte = self.lower_rotation_dict.get('4')
            lower_motor_number_byte = self.lower_finger_dict.get('4')
            lower_motor_byte = motor_byte_base + lower_motor_rotation_byte + lower_motor_number_byte
        elif current_finger_index == 4:
            print('Tense - Pinky')
            upper_motor_rotation_byte = self.upper_rotation_dict.get('5')
            upper_motor_number_byte = self.upper_finger_dict.get('5')
            upper_motor_byte = motor_byte_base + upper_motor_rotation_byte + upper_motor_number_byte

            lower_motor_rotation_byte = self.lower_rotation_dict.get('5')
            lower_motor_number_byte = self.lower_finger_dict.get('5')
            lower_motor_byte = motor_byte_base + lower_motor_rotation_byte + lower_motor_number_byte
        else:
            print(f'Unknown finger index: {current_finger_index}')

        pwm = self.tense_finger_pwm_scale.value()
        time = float(self.tense_finger_time_input.toPlainText())
        if upper_motor_byte != '' and lower_motor_byte != '':
            self.command_master.send_command(part='Upper', config='00001110', motor_byte=upper_motor_byte, pwm=pwm,
                                             work_time=time)
            self.command_master.send_command(part='Lower', config='00001110', motor_byte=lower_motor_byte, pwm=pwm,
                                             work_time=time)
            self.command_master.power_command('Upper', config='00000001', power_byte='00000001')
            self.command_master.power_command('Lower', config='00000001', power_byte='00000001')
        else:
            print('PreSavedMoves/tense_finger_command - motor bytes are empty')

    def release_finger_command(self):
        current_finger_index = self.tense_finger_comboBox.currentIndex()
        motor_byte_base = '000'
        upper_motor_byte = ''
        lower_motor_byte = ''
        if current_finger_index == 0:
            print('Release - Thumb')
            upper_motor_rotation_byte = self.upper_rotation_dict.get('_1')
            upper_motor_number_byte = self.upper_finger_dict.get('1')
            upper_motor_byte = motor_byte_base + upper_motor_rotation_byte + upper_motor_number_byte

            lower_motor_rotation_byte = self.lower_rotation_dict.get('_1')
            lower_motor_number_byte = self.lower_finger_dict.get('1')
            lower_motor_byte = motor_byte_base + lower_motor_rotation_byte + lower_motor_number_byte
        elif current_finger_index == 1:
            print('Release - Index')
            upper_motor_rotation_byte = self.upper_rotation_dict.get('_2')
            upper_motor_number_byte = self.upper_finger_dict.get('2')
            upper_motor_byte = motor_byte_base + upper_motor_rotation_byte + upper_motor_number_byte

            lower_motor_rotation_byte = self.lower_rotation_dict.get('_2')
            lower_motor_number_byte = self.lower_finger_dict.get('2')
            lower_motor_byte = motor_byte_base + lower_motor_rotation_byte + lower_motor_number_byte
        elif current_finger_index == 2:
            print('Release - Middle')
            upper_motor_rotation_byte = self.upper_rotation_dict.get('_3')
            upper_motor_number_byte = self.upper_finger_dict.get('3')
            upper_motor_byte = motor_byte_base + upper_motor_rotation_byte + upper_motor_number_byte

            lower_motor_rotation_byte = self.lower_rotation_dict.get('_3')
            lower_motor_number_byte = self.lower_finger_dict.get('3')
            lower_motor_byte = motor_byte_base + lower_motor_rotation_byte + lower_motor_number_byte
        elif current_finger_index == 3:
            print('Release - Ring')
            upper_motor_rotation_byte = self.upper_rotation_dict.get('_4')
            upper_motor_number_byte = self.upper_finger_dict.get('4')
            upper_motor_byte = motor_byte_base + upper_motor_rotation_byte + upper_motor_number_byte

            lower_motor_rotation_byte = self.lower_rotation_dict.get('_4')
            lower_motor_number_byte = self.lower_finger_dict.get('4')
            lower_motor_byte = motor_byte_base + lower_motor_rotation_byte + lower_motor_number_byte
        elif current_finger_index == 4:
            print('Release - Pinky')
            upper_motor_rotation_byte = self.upper_rotation_dict.get('_5')
            upper_motor_number_byte = self.upper_finger_dict.get('5')
            upper_motor_byte = motor_byte_base + upper_motor_rotation_byte + upper_motor_number_byte

            lower_motor_rotation_byte = self.lower_rotation_dict.get('_5')
            lower_motor_number_byte = self.lower_finger_dict.get('5')
            lower_motor_byte = motor_byte_base + lower_motor_rotation_byte + lower_motor_number_byte
        else:
            print(f'Unknown finger index: {current_finger_index}')

        pwm = 50
        time = 0.2
        if upper_motor_byte != '' and lower_motor_byte != '':
            self.command_master.send_command(part='Upper', config='00001110', motor_byte=upper_motor_byte, pwm=pwm,
                                             work_time=time)
            self.command_master.send_command(part='Lower', config='00001110', motor_byte=lower_motor_byte, pwm=pwm,
                                             work_time=time)
            self.command_master.power_command('Upper', config='00000001', power_byte='00000001')
            self.command_master.power_command('Lower', config='00000001', power_byte='00000001')
        else:
            print('PreSavedMoves/tense_finger_command - motor bytes are empty')

    def update_tense_finger_pwm_label(self, value):
        self.tense_finger_pwm_label.setText(str(value))


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = PreSavedMoves()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
