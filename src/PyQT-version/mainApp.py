import sys
import View
from Model import *
import comport as com
from PyQt5 import QtWidgets, QtCore
from PyQt5 import uic


def send_power(comport):
    com.send_command(comport, config='00000001', power_byte='00000001')  # Send power ON


class App(QtWidgets.QMainWindow, View.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.upper_comport = com.ini('COM2')
        self.lower_comport = com.ini('COM3')
        self.model = Model(self.upper_comport, self.lower_comport)

        self.upper_send_power_btn.clicked.connect(self.upper_send_power)
        self.lower_send_power_btn.clicked.connect(self.lower_send_power)

        self.upper_send_adc.clicked.connect(self.upper_collect_adc)
        self.lower_send_adc.clicked.connect(self.lower_collect_adc)

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

    def switch_button_color(self, button, color='#19e676'):
        if button.styleSheet() == 'background-color:' or button.styleSheet() == '':
            button.setStyleSheet(f"background-color:{color}")
        else:
            button.setStyleSheet(f"background-color:")

    def configure_relatives_buttons(self, group_buttons, pressed_button):
        if group_buttons[pressed_button].styleSheet() == 'background-color:' or group_buttons[pressed_button].styleSheet() == '':
            self.switch_button_color(group_buttons[pressed_button])
            current_button_group_copy = group_buttons.copy()
            del current_button_group_copy[pressed_button]
            for i in range(0, len(current_button_group_copy)):
                self.switch_button_color(current_button_group_copy[i], color='')
        else:
            return 0  # Current color is not default

    def upper_send_power(self):
        send_power(self.upper_comport)
        send_power(self.lower_comport)

    def upper_collect_adc(self):
        m1_status = self.upper_motor1_adc_box.isChecked()
        m2_status = self.upper_motor2_adc_box.isChecked()
        m3_status = self.upper_motor3_adc_box.isChecked()
        m4_status = self.upper_motor4_adc_box.isChecked()
        m5_status = self.upper_motor5_adc_box.isChecked()
        adc_number = int(m1_status + m2_status + m3_status + m4_status + m5_status)
        adc_decimal = m1_status*2**0 + m2_status*2**1 + m3_status*2**2 + m4_status*2**3 + m5_status*2**4
        if adc_number != 0:
            self.model.upper_send_adc(adc_decimal)
        else:
            print('mainApp.py/upper_collect_adc - adc_number is zero')

    def upper_motor1_rotate_left(self, args=None):
        if not args:  # Without args
            pwm = self.upper_motor1_pwm_scale.value()
            time = float(self.upper_motor1_time_input.toPlainText())
            delay = float(self.upper_motor1_delay_input.toPlainText())
            time_limited_motion(self.upper_comport, '00011110', '00001100', pwm, time, delay)
            self.configure_relatives_buttons(self.upper_motor1_buttons, 0)

            self.lower_motor1_rotate_right([15, time, delay])
            self.configure_relatives_buttons(self.lower_motor1_buttons, 1)
        else:  # With args
            time_limited_motion(self.upper_comport, config='00011110', motor_byte='00001100', pwm=args[0],
                                limited_time=args[1], delay=args[2])

    def upper_motor1_rotate_right(self, args=None):
        if not args:
            pwm = self.upper_motor1_pwm_scale.value()
            time = float(self.upper_motor1_time_input.toPlainText())
            delay = float(self.upper_motor1_delay_input.toPlainText())
            time_limited_motion(self.upper_comport, '00011110', '00010100', pwm, time, delay)
            self.configure_relatives_buttons(self.upper_motor1_buttons, 1)

            self.lower_motor1_rotate_left([15, time, delay])
            self.configure_relatives_buttons(self.lower_motor1_buttons, 0)
        else:
            time_limited_motion(self.upper_comport, config='00011110', motor_byte='00010100', pwm=args[0],
                                limited_time=args[1], delay=args[2])

    def upper_motor1_rotate_stop(self):
        com.send_command(self.upper_comport, config='00000010', motor_byte='00000100')
        self.configure_relatives_buttons(self.upper_motor1_buttons, 2)
        com.send_command(self.lower_comport, config='00000010', motor_byte='00000001')
        self.configure_relatives_buttons(self.lower_motor1_buttons, 2)

    def update_upper_label_1(self, value):
        self.upper_motor1_scale_label.setText(str(value))

    def upper_motor2_rotate_left(self, args=None):
        if not args:
            pwm = self.upper_motor2_pwm_scale.value()
            time = float(self.upper_motor2_time_input.toPlainText())
            delay = float(self.upper_motor2_delay_input.toPlainText())
            time_limited_motion(self.upper_comport, '00011110', '00001000', pwm, time, delay)
            self.configure_relatives_buttons(self.upper_motor2_buttons, 0)

            self.lower_motor2_rotate_right([15, time, delay])
            self.configure_relatives_buttons(self.lower_motor2_buttons, 1)
        else:
            time_limited_motion(self.upper_comport, config='00011110', motor_byte='00001000', pwm=args[0],
                                limited_time=args[1], delay=args[2])

    def upper_motor2_rotate_right(self, args=None):
        if not args:
            pwm = self.upper_motor2_pwm_scale.value()
            time = float(self.upper_motor2_time_input.toPlainText())
            delay = float(self.upper_motor2_delay_input.toPlainText())
            time_limited_motion(self.upper_comport, '00011110', '00010000', pwm, time, delay)
            self.configure_relatives_buttons(self.upper_motor2_buttons, 1)

            self.lower_motor2_rotate_left([15, time, delay])
            self.configure_relatives_buttons(self.lower_motor2_buttons, 0)
        else:
            time_limited_motion(self.upper_comport, config='00011110', motor_byte='00010000', pwm=args[0],
                                limited_time=args[1], delay=args[2])

    def upper_motor2_rotate_stop(self):
        com.send_command(self.upper_comport, config='00000010', motor_byte='00000000')
        self.configure_relatives_buttons(self.upper_motor2_buttons, 2)
        com.send_command(self.lower_comport, config='00000010', motor_byte='00000011')
        self.configure_relatives_buttons(self.lower_motor2_buttons, 2)

    def update_upper_label_2(self, value):
        self.upper_motor2_scale_label.setText(str(value))

    def upper_motor3_rotate_left(self, args=None):
        if not args:
            pwm = self.upper_motor3_pwm_scale.value()
            time = float(self.upper_motor3_time_input.toPlainText())
            delay = float(self.upper_motor3_delay_input.toPlainText())
            time_limited_motion(self.upper_comport, '00011110', '00001010', pwm, time, delay)
            self.configure_relatives_buttons(self.upper_motor3_buttons, 0)

            self.lower_motor3_rotate_right([15, time, delay])
            self.configure_relatives_buttons(self.lower_motor3_buttons, 1)
        else:
            time_limited_motion(self.upper_comport, config='00011110', motor_byte='00001010', pwm=args[0],
                                limited_time=args[1], delay=args[2])

    def upper_motor3_rotate_right(self, args=None):
        if not args:
            pwm = self.upper_motor3_pwm_scale.value()
            time = float(self.upper_motor3_time_input.toPlainText())
            delay = float(self.upper_motor3_delay_input.toPlainText())
            time_limited_motion(self.upper_comport, '00011110', '00010010', pwm, time, delay)
            self.configure_relatives_buttons(self.upper_motor3_buttons, 1)

            self.lower_motor3_rotate_left([15, time, delay])
            self.configure_relatives_buttons(self.lower_motor3_buttons, 0)
        else:
            time_limited_motion(self.upper_comport, config='00011110', motor_byte='00010010', pwm=args[0],
                                limited_time=args[1], delay=args[2])

    def upper_motor3_rotate_stop(self):
        com.send_command(self.upper_comport, config='00000010', motor_byte='00000010')
        self.configure_relatives_buttons(self.upper_motor3_buttons, 2)
        com.send_command(self.lower_comport, config='00000010', motor_byte='00000010')
        self.configure_relatives_buttons(self.lower_motor3_buttons, 2)

    def update_upper_label_3(self, value):
        self.upper_motor3_scale_label.setText(str(value))

    def upper_motor4_rotate_left(self, args=None):
        if not args:
            pwm = self.upper_motor4_pwm_scale.value()
            time = float(self.upper_motor4_time_input.toPlainText())
            delay = float(self.upper_motor4_delay_input.toPlainText())
            time_limited_motion(self.upper_comport, '00011110', '00001011', pwm, time, delay)
            self.configure_relatives_buttons(self.upper_motor4_buttons, 0)

            self.lower_motor4_rotate_right([15, time, delay])
            self.configure_relatives_buttons(self.lower_motor4_buttons, 1)
        else:
            time_limited_motion(self.upper_comport, config='00011110', motor_byte='00001011', pwm=args[0],
                                limited_time=args[1], delay=args[2])

    def upper_motor4_rotate_right(self, args=None):
        if not args:
            pwm = self.upper_motor4_pwm_scale.value()
            time = float(self.upper_motor4_time_input.toPlainText())
            delay = float(self.upper_motor4_delay_input.toPlainText())
            time_limited_motion(self.upper_comport, '00011110', '00010011', pwm, time, delay)
            self.configure_relatives_buttons(self.upper_motor4_buttons, 1)

            self.lower_motor4_rotate_left([15, time, delay])
            self.configure_relatives_buttons(self.lower_motor4_buttons, 0)
        else:
            time_limited_motion(self.upper_comport, config='00011110', motor_byte='00010011', pwm=args[0],
                                limited_time=args[1], delay=args[2])

    def upper_motor4_rotate_stop(self):
        com.send_command(self.upper_comport, config='00000010', motor_byte='00000011')
        self.configure_relatives_buttons(self.upper_motor4_buttons, 2)
        com.send_command(self.lower_comport, config='00000010', motor_byte='00000100')
        self.configure_relatives_buttons(self.lower_motor4_buttons, 2)

    def update_upper_label_4(self, value):
        self.upper_motor4_scale_label.setText(str(value))

    def upper_motor5_rotate_left(self, args=None):
        if not args:
            pwm = self.upper_motor5_pwm_scale.value()
            time = float(self.upper_motor5_time_input.toPlainText())
            delay = float(self.upper_motor5_delay_input.toPlainText())
            time_limited_motion(self.upper_comport, '00011110', '00001001', pwm, time, delay)
            self.configure_relatives_buttons(self.upper_motor5_buttons, 0)

            self.lower_motor5_rotate_right([15, time, delay])
            self.configure_relatives_buttons(self.lower_motor5_buttons, 1)
        else:
            time_limited_motion(self.upper_comport, config='00011110', motor_byte='00001001', pwm=args[0],
                                limited_time=args[1], delay=args[2])

    def upper_motor5_rotate_right(self, args=None):
        if not args:
            pwm = self.upper_motor5_pwm_scale.value()
            time = float(self.upper_motor5_time_input.toPlainText())
            delay = float(self.upper_motor5_delay_input.toPlainText())
            time_limited_motion(self.upper_comport, '00011110', '00010001', pwm, time, delay)
            self.configure_relatives_buttons(self.upper_motor5_buttons, 1)

            self.lower_motor5_rotate_left([15, time, delay])
            self.configure_relatives_buttons(self.lower_motor5_buttons, 0)
        else:
            time_limited_motion(self.upper_comport, config='00011110', motor_byte='00010001', pwm=args[0],
                                limited_time=args[1], delay=args[2])

    def upper_motor5_rotate_stop(self):
        com.send_command(self.upper_comport, config='00000010', motor_byte='00000001')
        self.configure_relatives_buttons(self.upper_motor5_buttons, 2)
        com.send_command(self.lower_comport, config='00000010', motor_byte='00000000')
        self.configure_relatives_buttons(self.lower_motor5_buttons, 2)

    def update_upper_label_5(self, value):
        self.upper_motor5_scale_label.setText(str(value))

    # LOWER PART Methods
    def lower_send_power(self):
        send_power(self.lower_comport)
        send_power(self.upper_comport)

    def lower_collect_adc(self):
        print('main.py/lower_collect_adc')
        m1_status = self.lower_motor1_adc_box.isChecked()
        m2_status = self.lower_motor2_adc_box.isChecked()
        m3_status = self.lower_motor3_adc_box.isChecked()
        m4_status = self.lower_motor4_adc_box.isChecked()
        m5_status = self.lower_motor5_adc_box.isChecked()
        adc_number = int(m1_status + m2_status + m3_status + m4_status + m5_status)
        adc_decimal = m1_status*2**0 + m2_status*2**1 + m3_status*2**2 + m4_status*2**3 + m5_status*2**4
        if adc_number != 0:
            self.model.lower_send_adc(adc_decimal)
        else:
            print('main.py/lower_collect_adc - adc_number is zero')

    def lower_motor1_rotate_left(self, args=None):
        if not args:
            pwm = self.lower_motor1_pwm_scale.value()
            time = float(self.lower_motor1_time_input.toPlainText())
            delay = float(self.lower_motor1_delay_input.toPlainText())
            time_limited_motion(self.lower_comport, '00011110', '00001001', pwm, time, delay)
            self.configure_relatives_buttons(self.lower_motor1_buttons, 0)

            self.upper_motor1_rotate_right([15, time, delay])
            self.configure_relatives_buttons(self.upper_motor1_buttons, 1)
        else:
            time_limited_motion(self.lower_comport, config='00011110', motor_byte='00001001', pwm=args[0],
                                limited_time=args[1], delay=args[2])

    def lower_motor1_rotate_right(self, args=None):
        if not args:
            pwm = self.lower_motor1_pwm_scale.value()
            time = float(self.lower_motor1_time_input.toPlainText())
            delay = float(self.lower_motor1_delay_input.toPlainText())
            time_limited_motion(self.lower_comport, '00011110', '00010001', pwm, time, delay)
            self.configure_relatives_buttons(self.lower_motor1_buttons, 1)

            self.upper_motor1_rotate_left([15, time, delay])
            self.configure_relatives_buttons(self.upper_motor1_buttons, 0)
        else:
            time_limited_motion(self.lower_comport, config='00011110', motor_byte='00010001', pwm=args[0],
                                limited_time=args[1], delay=args[2])

    def lower_motor1_rotate_stop(self):
        com.send_command(self.lower_comport, config='00000010', motor_byte='00000001')
        self.configure_relatives_buttons(self.lower_motor1_buttons, 2)
        com.send_command(self.upper_comport, config='00000010', motor_byte='00000100')
        self.configure_relatives_buttons(self.upper_motor1_buttons, 2)

    def update_lower_label_1(self, value):
        self.lower_motor1_scale_label.setText(str(value))

    def lower_motor2_rotate_left(self, args=None):
        if not args:
            pwm = self.lower_motor2_pwm_scale.value()
            time = float(self.lower_motor2_time_input.toPlainText())
            delay = float(self.lower_motor2_delay_input.toPlainText())
            time_limited_motion(self.lower_comport, '00011110', '00001011', pwm, time, delay)
            self.configure_relatives_buttons(self.lower_motor2_buttons, 0)

            self.upper_motor2_rotate_right([15, time, delay])
            self.configure_relatives_buttons(self.upper_motor2_buttons, 1)
        else:
            time_limited_motion(self.lower_comport, config='00011110', motor_byte='00001011', pwm=args[0],
                                limited_time=args[1], delay=args[2])

    def lower_motor2_rotate_right(self, args=None):
        if not args:
            pwm = self.lower_motor2_pwm_scale.value()
            time = float(self.lower_motor2_time_input.toPlainText())
            delay = float(self.lower_motor2_delay_input.toPlainText())
            time_limited_motion(self.lower_comport, '00011110', '00010011', pwm, time, delay)
            self.configure_relatives_buttons(self.lower_motor2_buttons, 1)

            self.upper_motor2_rotate_left([15, time, delay])
            self.configure_relatives_buttons(self.upper_motor2_buttons, 0)
        else:
            time_limited_motion(self.lower_comport, config='00011110', motor_byte='00010011', pwm=args[0],
                                limited_time=args[1], delay=args[2])

    def lower_motor2_rotate_stop(self):
        com.send_command(self.lower_comport, config='00000010', motor_byte='00000011')
        self.configure_relatives_buttons(self.lower_motor2_buttons, 2)
        com.send_command(self.upper_comport, config='00000010', motor_byte='00000000')
        self.configure_relatives_buttons(self.upper_motor2_buttons, 2)

    def update_lower_label_2(self, value):
        self.lower_motor2_scale_label.setText(str(value))

    def lower_motor3_rotate_left(self, args=None):
        if not args:
            pwm = self.lower_motor3_pwm_scale.value()
            time = float(self.lower_motor3_time_input.toPlainText())
            delay = float(self.lower_motor3_delay_input.toPlainText())
            time_limited_motion(self.lower_comport, '00011110', '00001010', pwm, time, delay)
            self.configure_relatives_buttons(self.lower_motor3_buttons, 0)

            self.upper_motor3_rotate_right([15, time, delay])
            self.configure_relatives_buttons(self.upper_motor3_buttons, 1)
        else:
            time_limited_motion(self.lower_comport, config='00011110', motor_byte='00001010', pwm=args[0],
                                limited_time=args[1], delay=args[2])

    def lower_motor3_rotate_right(self, args=None):
        if not args:
            pwm = self.lower_motor3_pwm_scale.value()
            time = float(self.lower_motor3_time_input.toPlainText())
            delay = float(self.lower_motor3_delay_input.toPlainText())
            time_limited_motion(self.lower_comport, '00011110', '00010010', pwm, time, delay)
            self.configure_relatives_buttons(self.lower_motor3_buttons, 1)

            self.upper_motor3_rotate_left([15, time, delay])
            self.configure_relatives_buttons(self.upper_motor3_buttons, 0)
        else:
            time_limited_motion(self.lower_comport, config='00011110', motor_byte='00010010', pwm=args[0],
                                limited_time=args[1], delay=args[2])

    def lower_motor3_rotate_stop(self):
        com.send_command(self.lower_comport, config='00000010', motor_byte='00000010')
        self.configure_relatives_buttons(self.lower_motor3_buttons, 2)
        com.send_command(self.upper_comport, config='00000010', motor_byte='00000010')
        self.configure_relatives_buttons(self.upper_motor3_buttons, 2)

    def update_lower_label_3(self, value):
        self.lower_motor3_scale_label.setText(str(value))

    def lower_motor4_rotate_left(self, args=None):
        if not args:
            pwm = self.lower_motor4_pwm_scale.value()
            time = float(self.lower_motor4_time_input.toPlainText())
            delay = float(self.lower_motor4_delay_input.toPlainText())
            time_limited_motion(self.lower_comport, '00011110', '00001100', pwm, time, delay)
            self.configure_relatives_buttons(self.lower_motor4_buttons, 0)

            self.upper_motor4_rotate_right([15, time, delay])
            self.configure_relatives_buttons(self.upper_motor4_buttons, 1)
        else:
            time_limited_motion(self.lower_comport, config='00011110', motor_byte='00001100', pwm=args[0],
                                limited_time=args[1], delay=args[2])

    def lower_motor4_rotate_right(self, args=None):
        if not args:
            pwm = self.lower_motor4_pwm_scale.value()
            time = float(self.lower_motor4_time_input.toPlainText())
            delay = float(self.lower_motor4_delay_input.toPlainText())
            time_limited_motion(self.lower_comport, '00011110', '00010100', pwm, time, delay)
            self.configure_relatives_buttons(self.lower_motor4_buttons, 1)

            self.upper_motor4_rotate_left([15, time, delay])
            self.configure_relatives_buttons(self.upper_motor4_buttons, 0)
        else:
            time_limited_motion(self.lower_comport, config='00011110', motor_byte='00010100', pwm=args[0],
                                limited_time=args[1], delay=args[2])

    def lower_motor4_rotate_stop(self):
        com.send_command(self.lower_comport, config='00000010', motor_byte='00000100')
        self.configure_relatives_buttons(self.lower_motor4_buttons, 2)
        com.send_command(self.upper_comport, config='00000010', motor_byte='00000011')
        self.configure_relatives_buttons(self.upper_motor4_buttons, 2)

    def update_lower_label_4(self, value):
        self.lower_motor4_scale_label.setText(str(value))

    def lower_motor5_rotate_left(self, args=None):
        if not args:
            pwm = self.lower_motor5_pwm_scale.value()
            time = float(self.lower_motor5_time_input.toPlainText())
            delay = float(self.lower_motor5_delay_input.toPlainText())
            time_limited_motion(self.lower_comport, '00011110', '00001000', pwm, time, delay)
            self.configure_relatives_buttons(self.lower_motor5_buttons, 0)

            self.upper_motor5_rotate_right([15, time, delay])
            self.configure_relatives_buttons(self.upper_motor5_buttons, 1)
        else:
            time_limited_motion(self.lower_comport, config='00011110', motor_byte='00001000', pwm=args[0],
                                limited_time=args[1], delay=args[2])

    def lower_motor5_rotate_right(self, args=None):
        if not args:
            pwm = self.lower_motor5_pwm_scale.value()
            time = float(self.lower_motor5_time_input.toPlainText())
            delay = float(self.lower_motor5_delay_input.toPlainText())
            time_limited_motion(self.lower_comport, '00011110', '00010000', pwm, time, delay)
            self.configure_relatives_buttons(self.lower_motor5_buttons, 1)

            self.upper_motor5_rotate_left([15, time, delay])
            self.configure_relatives_buttons(self.upper_motor5_buttons, 0)
        else:
            time_limited_motion(self.lower_comport, config='00011110', motor_byte='00010000', pwm=args[0],
                                limited_time=args[1], delay=args[2])

    def lower_motor5_rotate_stop(self):
        com.send_command(self.lower_comport, config='00000010', motor_byte='00000000')
        self.configure_relatives_buttons(self.lower_motor5_buttons, 2)
        com.send_command(self.upper_comport, config='00000010', motor_byte='00000001')
        self.configure_relatives_buttons(self.upper_motor5_buttons, 2)

    def update_lower_label_5(self, value):
        self.lower_motor5_scale_label.setText(str(value))


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
