import sys
import ManualControlUi
from DataCollector import DataCollector
from Model import *
import comport as com
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox


def send_power(comport):
    com.send_command(comport, config='00000001', power_byte='00000001')  # Send power ON
    print(f"ManualControl/send_power - send power to {comport.name}")


def switch_button_color(button, color='#19e676'):
    if button.styleSheet() == 'background-color:' or button.styleSheet() == '':
        button.setStyleSheet(f"background-color:{color}")
    else:
        button.setStyleSheet(f"background-color:")


def configure_relatives_buttons(group_buttons, pressed_button):
    if group_buttons[pressed_button].styleSheet() == 'background-color:' or group_buttons[pressed_button].styleSheet() == '':
        switch_button_color(group_buttons[pressed_button])
        current_button_group_copy = group_buttons.copy()
        del current_button_group_copy[pressed_button]
        for i in range(0, len(current_button_group_copy)):
            switch_button_color(current_button_group_copy[i], color='')
    else:
        return 0  # Current color is not default


class ManualControl(QtWidgets.QMainWindow, ManualControlUi.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.upper_comport = com.ini('COM2')
        # self.lower_comport = com.ini('COM7')
        self.upper_comport = None
        self.lower_comport = None
        self.model = None

        self.upper_adc_waiting_flag = False
        self.lower_adc_waiting_flag = False
        # TODO: Need to reconnect DataCollectors from here to Model. Here must be no comport logic. Only Model has.
        # self.upper_data_collector = DataCollector(1, 50, self.upper_comport)
        # self.lower_data_collector = DataCollector(1, 50, self.lower_comport)
        self.upper_data_collector = None
        self.lower_data_collector = None
        self.upper_current_plots_num = 0
        self.lower_current_plots_num = 0

        self.default_move_script_text = "Move script is now empty"
        self.move_script_file_path = None

        self.add_graph1()  # Add initial dummy graph 1
        self.add_graph2()  # Add initial dummy graph 2

        self.place_default_text()

        self.upper_send_power_btn.clicked.connect(self.upper_send_power)
        self.lower_send_power_btn.clicked.connect(self.lower_send_power)

        self.upper_send_adc.clicked.connect(self.upper_collect_adc)
        self.lower_send_adc.clicked.connect(self.lower_collect_adc)

        self.stop_receive_btn.clicked.connect(self.stop_receive)
        self.save_graph_btn.clicked.connect(self.save_plot_widget_as_jpg)

        self.open_script_file_btn.clicked.connect(self.open_script_file)
        self.save_move_script_btn.clicked.connect(self.save_script)
        self.discard_move_script_btn.clicked.connect(self.discard_script)

        self.upper_motor1_left_btn.clicked.connect(self.upper_motor1_rotate_left)
        self.upper_motor1_right_btn.clicked.connect(self.upper_motor1_rotate_right)
        self.upper_motor1_stop_btn.clicked.connect(self.upper_motor1_rotate_stop)
        self.upper_motor1_pwm_scale.valueChanged.connect(self.update_upper_label_1)
        self.upper_motor1_buttons = [self.upper_motor1_left_btn, self.upper_motor1_right_btn,
                                     self.upper_motor1_stop_btn]

        self.upper_motor2_left_btn.clicked.connect(self.upper_motor2_rotate_left)
        self.upper_motor2_right_btn.clicked.connect(self.upper_motor2_rotate_right)
        self.upper_motor2_stop_btn.clicked.connect(self.upper_motor2_rotate_stop)
        self.upper_motor2_pwm_scale.valueChanged.connect(self.update_upper_label_2)
        self.upper_motor2_buttons = [self.upper_motor2_left_btn, self.upper_motor2_right_btn,
                                     self.upper_motor2_stop_btn]

        self.upper_motor3_left_btn.clicked.connect(self.upper_motor3_rotate_left)
        self.upper_motor3_right_btn.clicked.connect(self.upper_motor3_rotate_right)
        self.upper_motor3_stop_btn.clicked.connect(self.upper_motor3_rotate_stop)
        self.upper_motor3_pwm_scale.valueChanged.connect(self.update_upper_label_3)
        self.upper_motor3_buttons = [self.upper_motor3_left_btn, self.upper_motor3_right_btn,
                                     self.upper_motor3_stop_btn]

        self.upper_motor4_left_btn.clicked.connect(self.upper_motor4_rotate_left)
        self.upper_motor4_right_btn.clicked.connect(self.upper_motor4_rotate_right)
        self.upper_motor4_stop_btn.clicked.connect(self.upper_motor4_rotate_stop)
        self.upper_motor4_pwm_scale.valueChanged.connect(self.update_upper_label_4)
        self.upper_motor4_buttons = [self.upper_motor4_left_btn, self.upper_motor4_right_btn,
                                     self.upper_motor4_stop_btn]

        self.upper_motor5_left_btn.clicked.connect(self.upper_motor5_rotate_left)
        self.upper_motor5_right_btn.clicked.connect(self.upper_motor5_rotate_right)
        self.upper_motor5_stop_btn.clicked.connect(self.upper_motor5_rotate_stop)
        self.upper_motor5_pwm_scale.valueChanged.connect(self.update_upper_label_5)
        self.upper_motor5_buttons = [self.upper_motor5_left_btn, self.upper_motor5_right_btn,
                                     self.upper_motor5_stop_btn]

        #  Lower part connection
        self.lower_motor1_left_btn.clicked.connect(self.lower_motor1_rotate_left)
        self.lower_motor1_right_btn.clicked.connect(self.lower_motor1_rotate_right)
        self.lower_motor1_stop_btn.clicked.connect(self.lower_motor1_rotate_stop)
        self.lower_motor1_pwm_scale.valueChanged.connect(self.update_lower_label_1)
        self.lower_motor1_buttons = [self.lower_motor1_left_btn, self.lower_motor1_right_btn,
                                     self.lower_motor1_stop_btn]

        self.lower_motor2_left_btn.clicked.connect(self.lower_motor2_rotate_left)
        self.lower_motor2_right_btn.clicked.connect(self.lower_motor2_rotate_right)
        self.lower_motor2_stop_btn.clicked.connect(self.lower_motor2_rotate_stop)
        self.lower_motor2_pwm_scale.valueChanged.connect(self.update_lower_label_2)
        self.lower_motor2_buttons = [self.lower_motor2_left_btn, self.lower_motor2_right_btn,
                                     self.lower_motor2_stop_btn]

        self.lower_motor3_left_btn.clicked.connect(self.lower_motor3_rotate_left)
        self.lower_motor3_right_btn.clicked.connect(self.lower_motor3_rotate_right)
        self.lower_motor3_stop_btn.clicked.connect(self.lower_motor3_rotate_stop)
        self.lower_motor3_pwm_scale.valueChanged.connect(self.update_lower_label_3)
        self.lower_motor3_buttons = [self.lower_motor3_left_btn, self.lower_motor3_right_btn,
                                     self.lower_motor3_stop_btn]

        self.lower_motor4_left_btn.clicked.connect(self.lower_motor4_rotate_left)
        self.lower_motor4_right_btn.clicked.connect(self.lower_motor4_rotate_right)
        self.lower_motor4_stop_btn.clicked.connect(self.lower_motor4_rotate_stop)
        self.lower_motor4_pwm_scale.valueChanged.connect(self.update_lower_label_4)
        self.lower_motor4_buttons = [self.lower_motor4_left_btn, self.lower_motor4_right_btn,
                                     self.lower_motor4_stop_btn]

        self.lower_motor5_left_btn.clicked.connect(self.lower_motor5_rotate_left)
        self.lower_motor5_right_btn.clicked.connect(self.lower_motor5_rotate_right)
        self.lower_motor5_stop_btn.clicked.connect(self.lower_motor5_rotate_stop)
        self.lower_motor5_pwm_scale.valueChanged.connect(self.update_lower_label_5)
        self.lower_motor5_buttons = [self.lower_motor5_left_btn, self.lower_motor5_right_btn,
                                     self.lower_motor5_stop_btn]
        self.update_counter = 0

    def set_upper_comport(self, port):
        self.upper_comport = port
        print(f'ManualControl/set_upper_comport - upper comport update: {port}')

    def set_lower_comport(self, port):
        self.lower_comport = port
        print(f'ManualControl/set_lower_comport - lower comport update: {port}')

    def set_model(self, model: Model):
        self.model = model

    # TODO: Need to test new ADC-thread functions for upper/lower part
    def set_upper_data_collector(self, collector):
        print('ManualControl/set_upper_data_collector - setting an upper collector:')
        print(collector)
        self.upper_data_collector = collector
        self.__connect_upper_collector()

    def set_lower_data_collector(self, collector):
        print('ManualControl/set_lower_data_collector - setting a lower collector:')
        print(collector)
        self.lower_data_collector = collector
        self.__connect_lower_collector()

    def __connect_upper_collector(self):
        self.upper_data_collector_thread = QtCore.QThread()
        self.upper_data_collector.moveToThread(self.upper_data_collector_thread)
        self.upper_data_collector_thread.started.connect(self.upper_data_collector.start_collecting)
        self.upper_data_collector.segment_received.connect(self.update_plot)
        self.upper_data_collector.finished.connect(self.upper_data_collector_thread.quit)

    def __connect_lower_collector(self):
        self.lower_data_collector_thread = QtCore.QThread()
        self.lower_data_collector.moveToThread(self.lower_data_collector_thread)
        self.lower_data_collector_thread.started.connect(self.lower_data_collector.start_collecting)
        self.lower_data_collector.segment_received.connect(self.update_plot)
        self.lower_data_collector.finished.connect(self.lower_data_collector_thread.quit)

    def update_plot(self):
        print(f'ManualControl/update_plot')
        sets, dict_len = self.lower_data_collector.get_data_sets()
        data_sets = list()
        x_sets = list()
        plot_names = list()
        for key in sets.keys():
            plot_names.append(int(key))
            data_sets.append(sets[key])
            x_sets.append([i for i in range(0, len(sets[key]))])
        for i in range(len(plot_names)):
            plot_item = self.graphics_layout_widget.getItem(plot_names[i], 0)
            plot_item.plot(x_sets[i], data_sets[i], pen='r')
            plot_item.showGrid(x=True, y=True, alpha=1.0)

    def set_plot(self, indexes):
        self.graphics_layout_widget.clear()
        for i in range(len(indexes)):
            print(f'{i + 1}) {indexes[i]}')
            self.graphics_layout_widget.addPlot(row=i, col=0, title=f"Motor #{indexes[i] + 1}")

    def finish_upper_collector_thread(self):
        self.upper_data_collector_thread.quit()
        com.open_comport(self.lower_comport)

    def finish_lower_collector_thread(self):
        self.lower_data_collector_thread.quit()
        com.open_comport(self.lower_comport)

    def add_graph1(self):
        x1 = [1, 2, 3, 4, 5, 6, 7, 8]
        y1 = [10, 50, 20, 70, 30, 1, 1, 1]

        plot_item1 = self.graphics_layout_widget.addPlot(row=0, col=0, title="Graph 1")
        plot_item1.plot(x1, y1, pen='r')
        plot_item1.showGrid(x=True, y=True, alpha=1.0)

    def add_graph2(self):
        x2 = [1, 2, 3, 4, 5, 6, 7, 8]
        y2 = [10, 5, 2, 7, 3, 2, 3, 4]

        plot_item2 = self.graphics_layout_widget.addPlot(row=1, col=0, title="Graph 2")
        plot_item2.plot(x2, y2, pen='g')
        plot_item2.showGrid(x=True, y=True, alpha=1.0)

    def place_default_text(self):
        self.move_script_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        self.move_script_label.setWordWrap(True)
        self.move_script_label.setText(self.default_move_script_text)

    # TODO: This method needs to be done
    def append_text(self, part, data):
        if part == 'Upper':
            print(f'Upper data:', end="")
            print(*data, end=".")
            for i in range(len(data)):
                print(f'Data: {data[i]}, type: {type(data[i])}')
        elif part == 'Lower':
            print(f'Lower data: {data}', end="")
            print(*data)
        else:
            print(f'No such part: {part}')
        # current_text = self.move_script_label.text()
        # if current_text == self.default_move_script_text:
        #     self.move_script_label.setText(data + " ")
        # else:
        #     self.move_script_label.setText(current_text + data + " ")

    def open_script_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt)")
        if file_path:
            self.script_file_path_label.setText(file_path)
            self.move_script_file_path = file_path

    def save_script(self):
        if self.move_script_file_path is None:
            QMessageBox.warning(self, 'Warning', 'Undefined file location')
        else:
            current_text = self.move_script_label.text()
            with open(self.move_script_file_path, 'a') as file:
                file.write(current_text)
                file.close()
            QMessageBox.information(self, 'Success', 'Data successfully saved!')

    def discard_script(self):
        pass

    # TODO: Do something with these two (stop_receive, save_plot_...)
    def stop_receive(self):
        print('Stop receive')
        if self.timer.isActive():  # If timer is active then stop it and run again
            self.timer.stop()

    def save_plot_widget_as_jpg(self, filename='default.jpg'):
        print('Save graph')
        # base_path = r'C:\Users\Bogh\TestFolder\\'
        # exporter = pg.exporters.ImageExporter(self.graphics_layout_widget.scene())
        # exporter.export(base_path + filename)

    def upper_send_power(self):
        self.model.power_command('Upper', config='00000001', power_byte='00000001')
        if self.upper_adc_waiting_flag:
            print("ManualControl/upper_send_power - we about to start ADC collecting")
        # send_power(self.lower_comport)

    def get_upper_adc_state(self) -> list:
        adc_arr = list()

        m1_status = self.upper_motor1_adc_box.isChecked()
        adc_arr.append(m1_status)
        m2_status = self.upper_motor2_adc_box.isChecked()
        adc_arr.append(m2_status)
        m3_status = self.upper_motor3_adc_box.isChecked()
        adc_arr.append(m3_status)
        m4_status = self.upper_motor4_adc_box.isChecked()
        adc_arr.append(m4_status)
        m5_status = self.upper_motor5_adc_box.isChecked()
        adc_arr.append(m5_status)

        return adc_arr

    def upper_collect_adc(self):
        adc_list = self.get_upper_adc_state()
        print(f'ManControl/upper_collect_adc - {adc_list}')
        m1_status = self.upper_motor1_adc_box.isChecked()
        m2_status = self.upper_motor2_adc_box.isChecked()
        m3_status = self.upper_motor3_adc_box.isChecked()
        m4_status = self.upper_motor4_adc_box.isChecked()
        m5_status = self.upper_motor5_adc_box.isChecked()
        adc_number = int(m1_status + m2_status + m3_status + m4_status + m5_status)
        adc_decimal = m1_status * 2 ** 0 + m2_status * 2 ** 1 + m3_status * 2 ** 2 + m4_status * 2 ** 3 + m5_status * 2 ** 4
        if adc_number != 0:
            self.model.upper_send_adc(adc_decimal)
            self.upper_adc_waiting_flag = True
        else:
            print('ManualControl.py/upper_collect_adc - adc_number is zero')

    def upper_motor1_rotate_left(self, args=None):
        if not args:  # Without args
            pwm = self.upper_motor1_pwm_scale.value()
            time = float(self.upper_motor1_time_input.toPlainText())
            delay = float(self.upper_motor1_delay_input.toPlainText())
            self.model.send_command('Upper', '00011110', '00001000', pwm, time, delay)
            byte_data = self.model.get_upper_commands_list()
            self.append_text('Upper', byte_data)
            configure_relatives_buttons(self.upper_motor1_buttons, 0)

            self.lower_motor1_rotate_right([15, time, delay])
            configure_relatives_buttons(self.lower_motor1_buttons, 1)
        else:  # With args
            self.model.send_command('Upper', config='00011110', motor_byte='00001000', pwm=args[0],
                                    limited_time=args[1], delay=args[2])

    def upper_motor1_rotate_right(self, args=None):
        if not args:
            pwm = self.upper_motor1_pwm_scale.value()
            time = float(self.upper_motor1_time_input.toPlainText())
            delay = float(self.upper_motor1_delay_input.toPlainText())
            self.model.send_command('Upper', '00011110', '00010000', pwm, time, delay)
            byte_data = self.model.get_upper_commands_list()
            self.append_text('Upper', byte_data)
            configure_relatives_buttons(self.upper_motor1_buttons, 1)

            self.lower_motor1_rotate_left([15, time, delay])
            configure_relatives_buttons(self.lower_motor1_buttons, 0)
        else:
            self.model.send_command('Upper', config='00011110', motor_byte='00010000', pwm=args[0],
                                    limited_time=args[1], delay=args[2])

    def upper_motor1_rotate_stop(self):
        self.model.stop_command('Upper', config='00000010', motor_byte='00000000')
        configure_relatives_buttons(self.upper_motor1_buttons, 2)
        self.model.stop_command('Lower', config='00000010', motor_byte='00000000')
        configure_relatives_buttons(self.lower_motor1_buttons, 2)

    def update_upper_label_1(self, value):
        self.upper_motor1_scale_label.setText(str(value))

    def upper_motor2_rotate_left(self, args=None):
        if not args:
            pwm = self.upper_motor2_pwm_scale.value()
            time = float(self.upper_motor2_time_input.toPlainText())
            delay = float(self.upper_motor2_delay_input.toPlainText())
            self.model.send_command('Upper', '00011110', '00001001', pwm, time, delay)
            byte_data = self.model.get_upper_commands_list()
            self.append_text('Upper', byte_data)
            configure_relatives_buttons(self.upper_motor2_buttons, 0)

            self.lower_motor2_rotate_right([15, time, delay])
            configure_relatives_buttons(self.lower_motor2_buttons, 1)
        else:
            self.model.send_command('Upper', config='00011110', motor_byte='00001001', pwm=args[0],
                                    limited_time=args[1], delay=args[2])

    def upper_motor2_rotate_right(self, args=None):
        if not args:
            pwm = self.upper_motor2_pwm_scale.value()
            time = float(self.upper_motor2_time_input.toPlainText())
            delay = float(self.upper_motor2_delay_input.toPlainText())
            self.model.send_command('Upper', '00011110', '00010001', pwm, time, delay)
            byte_data = self.model.get_upper_commands_list()
            self.append_text('Upper', byte_data)
            configure_relatives_buttons(self.upper_motor2_buttons, 1)

            self.lower_motor2_rotate_left([15, time, delay])
            configure_relatives_buttons(self.lower_motor2_buttons, 0)
        else:
            self.model.send_command('Upper', config='00011110', motor_byte='00010001', pwm=args[0],
                                    limited_time=args[1], delay=args[2])

    def upper_motor2_rotate_stop(self):
        self.model.stop_command('Upper', config='00000010', motor_byte='00000001')
        configure_relatives_buttons(self.upper_motor2_buttons, 2)
        self.model.stop_command('Lower', config='00000010', motor_byte='00000001')
        configure_relatives_buttons(self.lower_motor2_buttons, 2)

    def update_upper_label_2(self, value):
        self.upper_motor2_scale_label.setText(str(value))

    def upper_motor3_rotate_left(self, args=None):
        if not args:
            pwm = self.upper_motor3_pwm_scale.value()
            time = float(self.upper_motor3_time_input.toPlainText())
            delay = float(self.upper_motor3_delay_input.toPlainText())
            self.model.send_command('Upper', '00011110', '00001010', pwm, time, delay)
            byte_data = self.model.get_upper_commands_list()
            self.append_text('Upper', byte_data)
            configure_relatives_buttons(self.upper_motor3_buttons, 0)

            self.lower_motor3_rotate_right([15, time, delay])
            configure_relatives_buttons(self.lower_motor3_buttons, 1)
        else:
            self.model.send_command('Upper', config='00011110', motor_byte='00001010', pwm=args[0],
                                    limited_time=args[1], delay=args[2])

    def upper_motor3_rotate_right(self, args=None):
        if not args:
            pwm = self.upper_motor3_pwm_scale.value()
            time = float(self.upper_motor3_time_input.toPlainText())
            delay = float(self.upper_motor3_delay_input.toPlainText())
            self.model.send_command('Upper', '00011110', '00010010', pwm, time, delay)
            byte_data = self.model.get_upper_commands_list()
            self.append_text('Upper', byte_data)
            configure_relatives_buttons(self.upper_motor3_buttons, 1)

            self.lower_motor3_rotate_left([15, time, delay])
            configure_relatives_buttons(self.lower_motor3_buttons, 0)
        else:
            self.model.send_command('Upper', config='00011110', motor_byte='00010010', pwm=args[0],
                                    limited_time=args[1], delay=args[2])

    def upper_motor3_rotate_stop(self):
        self.model.stop_command('Upper', config='00000010', motor_byte='00000010')
        configure_relatives_buttons(self.upper_motor3_buttons, 2)
        self.model.stop_command('Lower', config='00000010', motor_byte='00000010')
        configure_relatives_buttons(self.lower_motor3_buttons, 2)

    def update_upper_label_3(self, value):
        self.upper_motor3_scale_label.setText(str(value))

    def upper_motor4_rotate_left(self, args=None):
        if not args:
            pwm = self.upper_motor4_pwm_scale.value()
            time = float(self.upper_motor4_time_input.toPlainText())
            delay = float(self.upper_motor4_delay_input.toPlainText())
            self.model.send_command('Upper', '00011110', '00001011', pwm, time, delay)
            byte_data = self.model.get_upper_commands_list()
            self.append_text('Upper', byte_data)
            configure_relatives_buttons(self.upper_motor4_buttons, 0)

            self.lower_motor4_rotate_right([15, time, delay])
            configure_relatives_buttons(self.lower_motor4_buttons, 1)
        else:
            self.model.send_command('Upper', config='00011110', motor_byte='00001011', pwm=args[0],
                                    limited_time=args[1], delay=args[2])

    def upper_motor4_rotate_right(self, args=None):
        if not args:
            pwm = self.upper_motor4_pwm_scale.value()
            time = float(self.upper_motor4_time_input.toPlainText())
            delay = float(self.upper_motor4_delay_input.toPlainText())
            self.model.send_command('Upper', '00011110', '00010011', pwm, time, delay)
            byte_data = self.model.get_upper_commands_list()
            self.append_text('Upper', byte_data)
            configure_relatives_buttons(self.upper_motor4_buttons, 1)

            self.lower_motor4_rotate_left([15, time, delay])
            configure_relatives_buttons(self.lower_motor4_buttons, 0)
        else:
            self.model.send_command('Upper', config='00011110', motor_byte='00010011', pwm=args[0],
                                    limited_time=args[1], delay=args[2])

    def upper_motor4_rotate_stop(self):
        self.model.stop_command('Upper', config='00000010', motor_byte='00000011')
        configure_relatives_buttons(self.upper_motor4_buttons, 2)
        self.model.stop_command('Lower', config='00000010', motor_byte='00000011')
        configure_relatives_buttons(self.lower_motor4_buttons, 2)

    def update_upper_label_4(self, value):
        self.upper_motor4_scale_label.setText(str(value))

    def upper_motor5_rotate_left(self, args=None):
        if not args:
            pwm = self.upper_motor5_pwm_scale.value()
            time = float(self.upper_motor5_time_input.toPlainText())
            delay = float(self.upper_motor5_delay_input.toPlainText())
            self.model.send_command('Upper', '00011110', '00001100', pwm, time, delay)
            byte_data = self.model.get_upper_commands_list()
            self.append_text('Upper', byte_data)
            configure_relatives_buttons(self.upper_motor5_buttons, 0)

            self.lower_motor5_rotate_right([15, time, delay])
            configure_relatives_buttons(self.lower_motor5_buttons, 1)
        else:
            self.model.send_command('Upper', config='00011110', motor_byte='00001100', pwm=args[0],
                                    limited_time=args[1], delay=args[2])

    def upper_motor5_rotate_right(self, args=None):
        if not args:
            pwm = self.upper_motor5_pwm_scale.value()
            time = float(self.upper_motor5_time_input.toPlainText())
            delay = float(self.upper_motor5_delay_input.toPlainText())
            self.model.send_command('Upper', '00011110', '00010100', pwm, time, delay)
            byte_data = self.model.get_upper_commands_list()
            self.append_text('Upper', byte_data)
            configure_relatives_buttons(self.upper_motor5_buttons, 1)

            self.lower_motor5_rotate_left([15, time, delay])
            configure_relatives_buttons(self.lower_motor5_buttons, 0)
        else:
            self.model.send_command('Upper', config='00011110', motor_byte='00010100', pwm=args[0],
                                    limited_time=args[1], delay=args[2])

    def upper_motor5_rotate_stop(self):
        self.model.stop_command('Upper', config='00000010', motor_byte='00000100')
        configure_relatives_buttons(self.upper_motor5_buttons, 2)
        self.model.stop_command('Lower', config='00000010', motor_byte='00000100')
        configure_relatives_buttons(self.lower_motor5_buttons, 2)

    def update_upper_label_5(self, value):
        self.upper_motor5_scale_label.setText(str(value))

    # LOWER PART Methods
    def lower_send_power(self):
        self.model.power_command('Lower', config='00000001', power_byte='00000001')
        if self.lower_adc_waiting_flag:
            print("ManualControl/lower_send_power - we about to start ADC collecting")
            self.lower_data_collector_thread.start()

    def get_lower_time_delay(self, motor_num):
        time = 0.0
        delay = 0.0
        if motor_num == 0:
            time = float(self.lower_motor1_time_input.toPlainText())
            delay = float(self.lower_motor1_delay_input.toPlainText())
            return time, delay
        elif motor_num == 1:
            time = float(self.lower_motor2_time_input.toPlainText())
            delay = float(self.lower_motor2_delay_input.toPlainText())
            return time, delay
        elif motor_num == 2:
            time = float(self.lower_motor3_time_input.toPlainText())
            delay = float(self.lower_motor3_delay_input.toPlainText())
            return time, delay
        elif motor_num == 3:
            time = float(self.lower_motor4_time_input.toPlainText())
            delay = float(self.lower_motor4_delay_input.toPlainText())
            return time, delay
        elif motor_num == 4:
            time = float(self.lower_motor5_time_input.toPlainText())
            delay = float(self.lower_motor5_delay_input.toPlainText())
            return time, delay
        else:
            return time, delay

    def get_lower_adc_state(self) -> list:
        adc_arr = list()

        m1_status = self.lower_motor1_adc_box.isChecked()
        adc_arr.append(m1_status)
        m2_status = self.lower_motor2_adc_box.isChecked()
        adc_arr.append(m2_status)
        m3_status = self.lower_motor3_adc_box.isChecked()
        adc_arr.append(m3_status)
        m4_status = self.lower_motor4_adc_box.isChecked()
        adc_arr.append(m4_status)
        m5_status = self.lower_motor5_adc_box.isChecked()
        adc_arr.append(m5_status)

        return adc_arr

    def lower_collect_adc(self):
        adc_state = self.get_lower_adc_state()
        adc_number = 0
        adc_decimal = 0
        motor_indexes = list()
        for i in range(len(adc_state)):
            if adc_state[i]:
                adc_number += 1
                adc_decimal += 2 ** i
                motor_indexes.append(i)

        if adc_number != 0:
            self.model.lower_send_adc(adc_decimal)
            self.lower_data_collector.set_holder_state(adc_state)
            print(self.lower_data_collector.get_data_sets())
            self.set_plot(motor_indexes)
            max_time = 0.0
            min_delay = 10.0  # Just magic number. Because 10 obviously greater than any possible delay
            for i in range(len(motor_indexes)):
                time_to_work, delay_before_work = self.get_lower_time_delay(motor_indexes[i])
                if time_to_work > max_time:
                    max_time = time_to_work
                if delay_before_work < min_delay:
                    min_delay = delay_before_work
            byte_count = int(max_time * 50)
            self.lower_data_collector.set_byte_count(byte_count)
            self.lower_data_collector.set_delay_for_collecting(min_delay)
            self.lower_adc_waiting_flag = True

    def lower_motor1_rotate_left(self, args=None):
        if not args:
            pwm = self.lower_motor1_pwm_scale.value()
            time = float(self.lower_motor1_time_input.toPlainText())
            delay = float(self.lower_motor1_delay_input.toPlainText())
            self.model.send_command('Lower', '00011110', '00001000', pwm, time, delay)  # Motor#2
            byte_data = self.model.get_lower_commands_list()
            self.append_text('Lower', byte_data)
            configure_relatives_buttons(self.lower_motor1_buttons, 0)

            self.upper_motor1_rotate_right([15, time, delay])
            configure_relatives_buttons(self.upper_motor1_buttons, 1)
        else:
            self.model.send_command('Lower', config='00011110', motor_byte='00001000', pwm=args[0],
                                    limited_time=args[1], delay=args[2])

    def lower_motor1_rotate_right(self, args=None):
        if not args:
            pwm = self.lower_motor1_pwm_scale.value()
            time = float(self.lower_motor1_time_input.toPlainText())
            delay = float(self.lower_motor1_delay_input.toPlainText())
            self.model.send_command('Lower', '00011110', '00010000', pwm, time, delay)  # Motor#2
            byte_data = self.model.get_lower_commands_list()
            self.append_text('Lower', byte_data)
            configure_relatives_buttons(self.lower_motor1_buttons, 1)

            self.upper_motor1_rotate_left([15, time, delay])
            configure_relatives_buttons(self.upper_motor1_buttons, 0)
        else:
            self.model.send_command('Lower', config='00011110', motor_byte='00010000', pwm=args[0],
                                    limited_time=args[1], delay=args[2])

    def lower_motor1_rotate_stop(self):
        self.model.stop_command('Lower', config='00000010', motor_byte='00000000')
        configure_relatives_buttons(self.lower_motor1_buttons, 2)
        self.model.stop_command('Upper', config='00000010', motor_byte='00000100')
        configure_relatives_buttons(self.upper_motor1_buttons, 2)

    def update_lower_label_1(self, value):
        self.lower_motor1_scale_label.setText(str(value))

    def lower_motor2_rotate_left(self, args=None):
        if not args:
            pwm = self.lower_motor2_pwm_scale.value()
            time = float(self.lower_motor2_time_input.toPlainText())
            delay = float(self.lower_motor2_delay_input.toPlainText())
            self.model.send_command('Lower', '00011110', '00001001', pwm, time, delay)  # Motor#4
            byte_data = self.model.get_lower_commands_list()
            self.append_text('Lower', byte_data)
            configure_relatives_buttons(self.lower_motor2_buttons, 0)

            self.upper_motor2_rotate_right([15, time, delay])
            configure_relatives_buttons(self.upper_motor2_buttons, 1)
        else:
            self.model.send_command('Lower', config='00011110', motor_byte='00001001', pwm=args[0],
                                    limited_time=args[1], delay=args[2])

    def lower_motor2_rotate_right(self, args=None):
        if not args:
            pwm = self.lower_motor2_pwm_scale.value()
            time = float(self.lower_motor2_time_input.toPlainText())
            delay = float(self.lower_motor2_delay_input.toPlainText())
            self.model.send_command('Lower', '00011110', '00010001', pwm, time, delay)  # Motor#4
            byte_data = self.model.get_lower_commands_list()
            self.append_text('Lower', byte_data)
            configure_relatives_buttons(self.lower_motor2_buttons, 1)

            self.upper_motor2_rotate_left([15, time, delay])
            configure_relatives_buttons(self.upper_motor2_buttons, 0)
        else:
            self.model.send_command('Lower', config='00011110', motor_byte='00010001', pwm=args[0],
                                    limited_time=args[1], delay=args[2])

    def lower_motor2_rotate_stop(self):
        self.model.stop_command('Lower', config='00000010', motor_byte='00000001')
        configure_relatives_buttons(self.lower_motor2_buttons, 2)
        self.model.stop_command('Upper', config='00000010', motor_byte='00000000')
        configure_relatives_buttons(self.upper_motor2_buttons, 2)

    def update_lower_label_2(self, value):
        self.lower_motor2_scale_label.setText(str(value))

    def lower_motor3_rotate_left(self, args=None):
        if not args:
            pwm = self.lower_motor3_pwm_scale.value()
            time = float(self.lower_motor3_time_input.toPlainText())
            delay = float(self.lower_motor3_delay_input.toPlainText())
            self.model.send_command('Lower', '00011110', '00001010', pwm, time, delay)
            byte_data = self.model.get_lower_commands_list()
            self.append_text('Lower', byte_data)
            configure_relatives_buttons(self.lower_motor3_buttons, 0)

            self.upper_motor3_rotate_right([15, time, delay])
            configure_relatives_buttons(self.upper_motor3_buttons, 1)
        else:
            self.model.send_command('Lower', config='00011110', motor_byte='00001010', pwm=args[0],
                                    limited_time=args[1], delay=args[2])

    def lower_motor3_rotate_right(self, args=None):
        if not args:
            pwm = self.lower_motor3_pwm_scale.value()
            time = float(self.lower_motor3_time_input.toPlainText())
            delay = float(self.lower_motor3_delay_input.toPlainText())
            self.model.send_command('Lower', '00011110', '00010010', pwm, time, delay)
            byte_data = self.model.get_lower_commands_list()
            self.append_text('Lower', byte_data)
            configure_relatives_buttons(self.lower_motor3_buttons, 1)

            self.upper_motor3_rotate_left([15, time, delay])
            configure_relatives_buttons(self.upper_motor3_buttons, 0)
        else:
            self.model.send_command('Lower', config='00011110', motor_byte='00010010', pwm=args[0],
                                    limited_time=args[1], delay=args[2])

    def lower_motor3_rotate_stop(self):
        self.model.stop_command('Lower', config='00000010', motor_byte='00000010')
        configure_relatives_buttons(self.lower_motor3_buttons, 2)
        self.model.stop_command('Upper', config='00000010', motor_byte='00000010')
        configure_relatives_buttons(self.upper_motor3_buttons, 2)

    def update_lower_label_3(self, value):
        self.lower_motor3_scale_label.setText(str(value))

    def lower_motor4_rotate_left(self, args=None):
        if not args:
            pwm = self.lower_motor4_pwm_scale.value()
            time = float(self.lower_motor4_time_input.toPlainText())
            delay = float(self.lower_motor4_delay_input.toPlainText())
            self.model.send_command('Lower', '00011110', '00001011', pwm, time, delay)
            byte_data = self.model.get_lower_commands_list()
            self.append_text('Lower', byte_data)
            configure_relatives_buttons(self.lower_motor4_buttons, 0)

            self.upper_motor4_rotate_right([15, time, delay])
            configure_relatives_buttons(self.upper_motor4_buttons, 1)
        else:
            self.model.send_command('Lower', config='00011110', motor_byte='00001011', pwm=args[0],
                                    limited_time=args[1], delay=args[2])

    def lower_motor4_rotate_right(self, args=None):
        if not args:
            pwm = self.lower_motor4_pwm_scale.value()
            time = float(self.lower_motor4_time_input.toPlainText())
            delay = float(self.lower_motor4_delay_input.toPlainText())
            self.model.send_command('Lower', '00011110', '00010011', pwm, time, delay)
            byte_data = self.model.get_lower_commands_list()
            self.append_text('Lower', byte_data)
            configure_relatives_buttons(self.lower_motor4_buttons, 1)

            self.upper_motor4_rotate_left([15, time, delay])
            configure_relatives_buttons(self.upper_motor4_buttons, 0)
        else:
            self.model.send_command('Lower', config='00011110', motor_byte='00010011', pwm=args[0],
                                    limited_time=args[1], delay=args[2])

    def lower_motor4_rotate_stop(self):
        self.model.stop_command('Lower', config='00000010', motor_byte='00000011')
        configure_relatives_buttons(self.lower_motor4_buttons, 2)
        self.model.stop_command('Upper', config='00000010', motor_byte='00000011')
        configure_relatives_buttons(self.upper_motor4_buttons, 2)

    def update_lower_label_4(self, value):
        self.lower_motor4_scale_label.setText(str(value))

    def lower_motor5_rotate_left(self, args=None):
        if not args:
            pwm = self.lower_motor5_pwm_scale.value()
            time = float(self.lower_motor5_time_input.toPlainText())
            delay = float(self.lower_motor5_delay_input.toPlainText())
            self.model.send_command('Lower', '00011110', '00001100', pwm, time, delay)
            byte_data = self.model.get_lower_commands_list()
            self.append_text('Lower', byte_data)
            configure_relatives_buttons(self.lower_motor5_buttons, 0)

            self.upper_motor5_rotate_right([15, time, delay])
            configure_relatives_buttons(self.upper_motor5_buttons, 1)
        else:
            self.model.send_command('Lower', config='00011110', motor_byte='00001100', pwm=args[0],
                               limited_time=args[1], delay=args[2])

    def lower_motor5_rotate_right(self, args=None):
        if not args:
            pwm = self.lower_motor5_pwm_scale.value()
            time = float(self.lower_motor5_time_input.toPlainText())
            delay = float(self.lower_motor5_delay_input.toPlainText())
            self.model.send_command('Lower', '00011110', '00010100', pwm, time, delay)
            byte_data = self.model.get_lower_commands_list()
            self.append_text('Lower', byte_data)
            configure_relatives_buttons(self.lower_motor5_buttons, 1)

            self.upper_motor5_rotate_left([15, time, delay])
            configure_relatives_buttons(self.upper_motor5_buttons, 0)
        else:
            self.model.send_command('Lower', config='00011110', motor_byte='00010100', pwm=args[0],
                               limited_time=args[1], delay=args[2])

    def lower_motor5_rotate_stop(self):
        self.model.stop_command('Lower', config='00000010', motor_byte='00000100')
        configure_relatives_buttons(self.lower_motor5_buttons, 2)
        self.model.stop_command('Upper', config='00000010', motor_byte='00000001')
        configure_relatives_buttons(self.upper_motor5_buttons, 2)

    def update_lower_label_5(self, value):
        self.lower_motor5_scale_label.setText(str(value))


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ManualControl()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
