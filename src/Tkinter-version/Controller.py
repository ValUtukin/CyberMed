from View import View
from Model import Model
from tkinter import *
from pubsub import pub
import comport as com
from MotorController import MotorController


class Controller:
    def __init__(self, parent):
        self.parent = parent
        self.upper_comport = com.ini('COM2')
        self.lower_comport = com.ini('COM3')
        self.model = Model()
        self.view = View(parent)
        self.view.setup()

        self.upper_motor_frame = self.view.upper_motor_frame
        self.lower_motor_frame = self.view.lower_motor_frame

        self.upper_controller = MotorController(self.upper_comport, 'Upper')
        self.lower_controller = MotorController(self.lower_comport, 'Lower')

        self.adc_status = False
        self.global_timer_status = False
        self.global_timer_time = 0.0

        pub.subscribe(self.upper_power_switch, "Upper_power_switch")
        pub.subscribe(self.lower_power_switch, "Lower_power_switch")

        pub.subscribe(self.upper_frame_send_adc, "Upper_frame_send_ADC")
        pub.subscribe(self.lower_frame_send_adc, "Lower_frame_send_ADC")

        pub.subscribe(self.upper_motor1_rotate_left, "Upper_motor1_rotate_left")
        pub.subscribe(self.upper_motor1_rotate_right, "Upper_motor1_rotate_right")
        pub.subscribe(self.upper_motor1_rotate_stop, "Upper_motor1_rotate_stop")

        pub.subscribe(self.upper_motor2_rotate_left, "Upper_motor2_rotate_left")
        pub.subscribe(self.upper_motor2_rotate_right, "Upper_motor2_rotate_right")
        pub.subscribe(self.upper_motor2_rotate_stop, "Upper_motor2_rotate_stop")

        pub.subscribe(self.upper_motor3_rotate_left, "Upper_motor3_rotate_left")
        pub.subscribe(self.upper_motor3_rotate_right, "Upper_motor3_rotate_right")
        pub.subscribe(self.upper_motor3_rotate_stop, "Upper_motor3_rotate_stop")

        pub.subscribe(self.upper_motor4_rotate_left, "Upper_motor4_rotate_left")
        pub.subscribe(self.upper_motor4_rotate_right, "Upper_motor4_rotate_right")
        pub.subscribe(self.upper_motor4_rotate_stop, "Upper_motor4_rotate_stop")

        pub.subscribe(self.upper_motor5_rotate_left, "Upper_motor5_rotate_left")
        pub.subscribe(self.upper_motor5_rotate_right, "Upper_motor5_rotate_right")
        pub.subscribe(self.upper_motor5_rotate_stop, "Upper_motor5_rotate_stop")

        pub.subscribe(self.lower_motor1_rotate_left, "Lower_motor1_rotate_left")
        pub.subscribe(self.lower_motor1_rotate_right, "Lower_motor1_rotate_right")
        pub.subscribe(self.lower_motor1_rotate_stop, "Lower_motor1_rotate_stop")

        pub.subscribe(self.lower_motor2_rotate_left, "Lower_motor2_rotate_left")
        pub.subscribe(self.lower_motor2_rotate_right, "Lower_motor2_rotate_right")
        pub.subscribe(self.lower_motor2_rotate_stop, "Lower_motor2_rotate_stop")

        pub.subscribe(self.lower_motor3_rotate_left, "Lower_motor3_rotate_left")
        pub.subscribe(self.lower_motor3_rotate_right, "Lower_motor3_rotate_right")
        pub.subscribe(self.lower_motor3_rotate_stop, "Lower_motor3_rotate_stop")

        pub.subscribe(self.lower_motor4_rotate_left, "Lower_motor4_rotate_left")
        pub.subscribe(self.lower_motor4_rotate_right, "Lower_motor4_rotate_right")
        pub.subscribe(self.lower_motor4_rotate_stop, "Lower_motor4_rotate_stop")

        pub.subscribe(self.lower_motor5_rotate_left, "Lower_motor5_rotate_left")
        pub.subscribe(self.lower_motor5_rotate_right, "Lower_motor5_rotate_right")
        pub.subscribe(self.lower_motor5_rotate_stop, "Lower_motor5_rotate_stop")

    def power_switch(self, comport, power_status):
        if power_status:
            com.send_command(comport, config='00000001', power_byte='00000001')
        else:
            com.send_command(comport, config='00000001', power_byte='00000000')

    def upper_power_switch(self):
        upper_power_status = self.upper_motor_frame.power_status.get()
        lower_power_status = upper_power_status
        self.power_switch(self.upper_comport, upper_power_status)
        self.power_switch(self.lower_comport, lower_power_status)
        # self.model.send_adc(self.upper_comport, self.upper_motor_frame)

    def lower_power_switch(self):
        lower_power_status = self.lower_motor_frame.power_status.get()
        upper_power_status = lower_power_status
        self.power_switch(self.lower_comport, lower_power_status)
        self.power_switch(self.upper_comport, upper_power_status)
        # self.model.send_adc(self.lower_comport, self.lower_motor_frame)

    def upper_frame_send_adc(self):
        self.model.send_adc(self.upper_comport, self.upper_motor_frame)

    def upper_motor1_rotate_left(self):  # Upper M1 (Pinky) -> Lower M2 (Pinky)
        timer_status = self.view.upper_motor_frame.motor1_timer_status.get()
        pwm = self.upper_motor_frame.motor1_pwm_scale.get()
        delay = self.model.convert_delay(self.view.upper_motor_frame.motor1_delay_entry.get())
        if timer_status:
            time = float(self.view.upper_motor_frame.motor1_timer_entry.get())
            self.upper_controller.motor1_rotate_left(self.adc_status, pwm, time, delay)
            self.lower_motor2_rotate_right([25, time, delay])
            self.lower_motor_frame.configure_relatives_buttons(self.lower_motor_frame.motor2_buttons, 1)
        else:
            self.upper_controller.motor1_rotate_left(self.adc_status, pwm, delay=delay)

    def upper_motor1_rotate_right(self):  # Upper M1 (Pinky) -> Lower M2 (Pinky)
        timer_status = self.view.upper_motor_frame.motor1_timer_status.get()
        pwm = self.upper_motor_frame.motor1_pwm_scale.get()
        delay = self.model.convert_delay(self.view.upper_motor_frame.motor1_delay_entry.get())
        if timer_status:
            time = float(self.view.upper_motor_frame.motor1_timer_entry.get())
            self.upper_controller.motor1_rotate_right(self.adc_status, pwm, time, delay)
            self.lower_motor2_rotate_left([10, time, delay])
            self.lower_motor_frame.configure_relatives_buttons(self.lower_motor_frame.motor2_buttons, 0)
        else:
            self.upper_controller.motor1_rotate_right(self.adc_status, pwm, delay=delay)

    def upper_motor1_rotate_stop(self):
        self.upper_controller.motor1_rotate_stop()

    def upper_motor2_rotate_left(self):  # Upper M2 (Thumb) -> Lower M1 (Thumb)
        timer_status = self.view.upper_motor_frame.motor2_timer_status.get()
        pwm = self.upper_motor_frame.motor2_pwm_scale.get()
        delay = self.model.convert_delay(self.view.upper_motor_frame.motor2_delay_entry.get())
        if timer_status:
            time = float(self.view.upper_motor_frame.motor2_timer_entry.get())
            self.upper_controller.motor2_rotate_left(self.adc_status, pwm, time, delay)
            self.lower_motor1_rotate_right([10, time, delay])
            self.lower_motor_frame.configure_relatives_buttons(self.lower_motor_frame.motor1_buttons, 1)
        else:
            self.upper_controller.motor2_rotate_left(self.adc_status, pwm, delay=delay)

    def upper_motor2_rotate_right(self):  # Upper M2 (Thumb) -> Lower M1 (Thumb)
        timer_status = self.view.upper_motor_frame.motor2_timer_status.get()
        pwm = self.upper_motor_frame.motor2_pwm_scale.get()
        delay = self.model.convert_delay(self.view.upper_motor_frame.motor2_delay_entry.get())
        if timer_status:
            time = float(self.view.upper_motor_frame.motor2_timer_entry.get())
            self.upper_controller.motor2_rotate_right(self.adc_status, pwm, time, delay)
            self.lower_motor1_rotate_left([10, time, delay])
            self.lower_motor_frame.configure_relatives_buttons(self.lower_motor_frame.motor1_buttons, 0)
        else:
            self.upper_controller.motor2_rotate_right(self.adc_status, pwm, delay=delay)

    def upper_motor2_rotate_stop(self):
        self.upper_controller.motor2_rotate_stop()

    def upper_motor3_rotate_left(self):  # Upper M3 (Middle) -> Lower M3 (Middle)
        timer_status = self.view.upper_motor_frame.motor3_timer_status.get()
        pwm = self.upper_motor_frame.motor3_pwm_scale.get()
        delay = self.model.convert_delay(self.view.upper_motor_frame.motor3_delay_entry.get())
        if timer_status:
            time = float(self.view.upper_motor_frame.motor3_timer_entry.get())
            self.upper_controller.motor3_rotate_left(self.adc_status, pwm, time, delay)
            self.lower_motor3_rotate_right([10, time, delay])
            self.lower_motor_frame.configure_relatives_buttons(self.lower_motor_frame.motor3_buttons, 1)
        else:
            self.upper_controller.motor3_rotate_left(self.adc_status, pwm, delay=delay)

    def upper_motor3_rotate_right(self):  # Upper M3 (Middle) -> Lower M3 (Middle)
        timer_status = self.view.upper_motor_frame.motor3_timer_status.get()
        pwm = self.upper_motor_frame.motor3_pwm_scale.get()
        delay = self.model.convert_delay(self.view.upper_motor_frame.motor3_delay_entry.get())
        if timer_status:
            time = float(self.view.upper_motor_frame.motor3_timer_entry.get())
            self.upper_controller.motor3_rotate_right(self.adc_status, pwm, time, delay)
            self.lower_motor3_rotate_left([10, time, delay])
            self.lower_motor_frame.configure_relatives_buttons(self.lower_motor_frame.motor3_buttons, 0)
        else:
            self.upper_controller.motor3_rotate_right(self.adc_status, pwm, delay=delay)

    def upper_motor3_rotate_stop(self):
        self.upper_controller.motor3_rotate_stop()

    def upper_motor4_rotate_left(self):  # Upper M4 (Index) -> Lower M5 (Index)
        timer_status = self.view.upper_motor_frame.motor4_timer_status.get()
        pwm = self.upper_motor_frame.motor4_pwm_scale.get()
        delay = self.model.convert_delay(self.view.upper_motor_frame.motor4_delay_entry.get())
        if timer_status:
            time = float(self.view.upper_motor_frame.motor4_timer_entry.get())
            self.upper_controller.motor4_rotate_left(self.adc_status, pwm, time, delay)
            self.lower_motor5_rotate_right([10, time, delay])
            self.lower_motor_frame.configure_relatives_buttons(self.lower_motor_frame.motor5_buttons, 1)
        else:
            self.upper_controller.motor4_rotate_left(self.adc_status, pwm, delay=delay)

    def upper_motor4_rotate_right(self):  # Upper M4 (Index) -> Lower M5 (Index)
        timer_status = self.view.upper_motor_frame.motor4_timer_status.get()
        pwm = self.upper_motor_frame.motor4_pwm_scale.get()
        delay = self.model.convert_delay(self.view.upper_motor_frame.motor4_delay_entry.get())
        if timer_status:
            time = float(self.view.upper_motor_frame.motor4_timer_entry.get())
            self.upper_controller.motor4_rotate_right(self.adc_status, pwm, time, delay)
            self.lower_motor5_rotate_left([10, time, delay])
            self.lower_motor_frame.configure_relatives_buttons(self.lower_motor_frame.motor5_buttons, 0)
        else:
            self.upper_controller.motor4_rotate_right(self.adc_status, pwm, delay=delay)

    def upper_motor4_rotate_stop(self):
        self.upper_controller.motor4_rotate_stop()

    def upper_motor5_rotate_left(self):  # Upper M5 (Ring) -> Lower M4 (Ring)
        timer_status = self.view.upper_motor_frame.motor5_timer_status.get()
        pwm = self.upper_motor_frame.motor5_pwm_scale.get()
        delay = self.model.convert_delay(self.view.upper_motor_frame.motor5_delay_entry.get())
        if timer_status:
            time = float(self.view.upper_motor_frame.motor5_timer_entry.get())
            self.upper_controller.motor5_rotate_left(self.adc_status, pwm, time, delay)
            self.lower_motor4_rotate_right([10, time, delay])
            self.lower_motor_frame.configure_relatives_buttons(self.lower_motor_frame.motor4_buttons, 1)
        else:
            self.upper_controller.motor5_rotate_left(self.adc_status, pwm, delay=delay)

    def upper_motor5_rotate_right(self):  # Upper M5 (Ring) -> Lower M4 (Ring)
        timer_status = self.view.upper_motor_frame.motor5_timer_status.get()
        pwm = self.upper_motor_frame.motor5_pwm_scale.get()
        delay = self.model.convert_delay(self.view.upper_motor_frame.motor5_delay_entry.get())
        if timer_status:
            time = float(self.view.upper_motor_frame.motor5_timer_entry.get())
            self.upper_controller.motor5_rotate_right(self.adc_status, pwm, time, delay)
            self.lower_motor4_rotate_left([10, time, delay])
            self.lower_motor_frame.configure_relatives_buttons(self.lower_motor_frame.motor4_buttons, 0)
        else:
            self.upper_controller.motor5_rotate_right(self.adc_status, pwm, delay=delay)

    def upper_motor5_rotate_stop(self):
        self.upper_controller.motor5_rotate_stop()

    def lower_frame_send_adc(self):
        self.model.send_adc(self.lower_comport, self.lower_motor_frame)

    def lower_motor1_rotate_left(self, args=None):
        if args is None:  # No given params
            timer_status = self.view.lower_motor_frame.motor1_timer_status.get()
            pwm = self.lower_motor_frame.motor1_pwm_scale.get()
            delay = self.model.convert_delay(self.view.lower_motor_frame.motor1_delay_entry.get())
            if timer_status:
                time = float(self.view.lower_motor_frame.motor1_timer_entry.get())
                self.lower_controller.motor1_rotate_left(self.adc_status, pwm, time, delay)
            else:
                self.lower_controller.motor1_rotate_left(self.adc_status, pwm, delay=delay)
        else:  # Some params was given
            print('LM1L - args len not 0')
            self.lower_controller.motor1_rotate_left(pwm=args[0], time_limited=args[1], delay=args[2])

    def lower_motor1_rotate_right(self, args=None):
        if args is None:
            timer_status = self.view.lower_motor_frame.motor1_timer_status.get()
            pwm = self.lower_motor_frame.motor1_pwm_scale.get()
            delay = self.model.convert_delay(self.view.lower_motor_frame.motor1_delay_entry.get())
            if timer_status:
                time = float(self.view.lower_motor_frame.motor1_timer_entry.get())
                self.lower_controller.motor1_rotate_right(self.adc_status, pwm, time, delay)
            else:
                self.lower_controller.motor1_rotate_right(self.adc_status, pwm, delay=delay)
        else:
            print('LM1R - args len not 0')
            self.lower_controller.motor1_rotate_right(pwm=args[0], time_limited=args[1], delay=args[2])

    def lower_motor1_rotate_stop(self):
        self.lower_controller.motor1_rotate_stop()

    def lower_motor2_rotate_left(self, args=None):
        if args is None:
            timer_status = self.view.lower_motor_frame.motor2_timer_status.get()
            pwm = self.lower_motor_frame.motor2_pwm_scale.get()
            delay = self.model.convert_delay(self.view.lower_motor_frame.motor2_delay_entry.get())
            if timer_status:
                time = float(self.view.lower_motor_frame.motor2_timer_entry.get())
                self.lower_controller.motor2_rotate_left(self.adc_status, pwm, time, delay)
            else:
                self.lower_controller.motor2_rotate_left(self.adc_status, pwm, delay=delay)
        else:
            print('LM2L - args len not 0')
            self.lower_controller.motor2_rotate_left(pwm=args[0], time_limited=args[1], delay=args[2])

    def lower_motor2_rotate_right(self, args=None):
        if args is None:
            timer_status = self.view.lower_motor_frame.motor2_timer_status.get()
            pwm = self.lower_motor_frame.motor2_pwm_scale.get()
            delay = self.model.convert_delay(self.view.lower_motor_frame.motor2_delay_entry.get())
            if timer_status:
                time = float(self.view.lower_motor_frame.motor2_timer_entry.get())
                self.lower_controller.motor2_rotate_right(self.adc_status, pwm, time, delay)
            else:
                self.lower_controller.motor2_rotate_right(self.adc_status, pwm, delay=delay)
        else:
            print('LM2R - args len not 0')
            self.lower_controller.motor2_rotate_right(pwm=args[0], time_limited=args[1], delay=args[2])

    def lower_motor2_rotate_stop(self):
        self.lower_controller.motor2_rotate_stop()

    def lower_motor3_rotate_left(self, args=None):
        if args is None:
            timer_status = self.view.lower_motor_frame.motor3_timer_status.get()
            pwm = self.lower_motor_frame.motor3_pwm_scale.get()
            delay = self.model.convert_delay(self.view.lower_motor_frame.motor3_delay_entry.get())
            if timer_status:
                time = float(self.view.lower_motor_frame.motor3_timer_entry.get())
                self.lower_controller.motor3_rotate_left(self.adc_status, pwm, time, delay)
            else:
                self.lower_controller.motor3_rotate_left(self.adc_status, pwm, delay=delay)
        else:
            print('LM3L - args len not 0')
            self.lower_controller.motor3_rotate_left(pwm=args[0], time_limited=args[1], delay=args[2])

    def lower_motor3_rotate_right(self, args=None):
        if args is None:
            timer_status = self.view.lower_motor_frame.motor3_timer_status.get()
            pwm = self.lower_motor_frame.motor3_pwm_scale.get()
            delay = self.model.convert_delay(self.view.lower_motor_frame.motor3_delay_entry.get())
            if timer_status:
                time = float(self.view.lower_motor_frame.motor3_timer_entry.get())
                self.lower_controller.motor3_rotate_right(self.adc_status, pwm, time, delay)
            else:
                self.lower_controller.motor3_rotate_right(self.adc_status, pwm, delay=delay)
        else:
            print('LM3R - args len not 0')
            self.lower_controller.motor3_rotate_right(pwm=args[0], time_limited=args[1], delay=args[2])

    def lower_motor3_rotate_stop(self):
        self.lower_controller.motor3_rotate_stop()

    def lower_motor4_rotate_left(self, args=None):
        if args is None:
            timer_status = self.view.lower_motor_frame.motor4_timer_status.get()
            pwm = self.lower_motor_frame.motor4_pwm_scale.get()
            delay = self.model.convert_delay(self.view.lower_motor_frame.motor4_delay_entry.get())
            if timer_status:
                time = float(self.view.lower_motor_frame.motor4_timer_entry.get())
                self.lower_controller.motor4_rotate_left(self.adc_status, pwm, time, delay)
            else:
                self.lower_controller.motor4_rotate_left(self.adc_status, pwm, delay=delay)
        else:
            print('LM4L - args len not 0')
            self.lower_controller.motor4_rotate_left(pwm=args[0], time_limited=args[1], delay=args[2])

    def lower_motor4_rotate_right(self, args=None):
        if args is None:
            timer_status = self.view.lower_motor_frame.motor4_timer_status.get()
            pwm = self.lower_motor_frame.motor4_pwm_scale.get()
            delay = self.model.convert_delay(self.view.lower_motor_frame.motor4_delay_entry.get())
            if timer_status:
                time = float(self.view.lower_motor_frame.motor4_timer_entry.get())
                self.lower_controller.motor4_rotate_right(self.adc_status, pwm, time, delay)
            else:
                self.lower_controller.motor4_rotate_right(self.adc_status, pwm, delay=delay)
        else:
            print('LM4R - args len not 0')
            self.lower_controller.motor4_rotate_right(pwm=args[0], time_limited=args[1], delay=args[2])

    def lower_motor4_rotate_stop(self):
        self.lower_controller.motor4_rotate_stop()

    def lower_motor5_rotate_left(self, args=None):
        if args is None:
            timer_status = self.view.lower_motor_frame.motor5_timer_status.get()
            pwm = self.lower_motor_frame.motor5_pwm_scale.get()
            delay = self.model.convert_delay(self.view.lower_motor_frame.motor5_delay_entry.get())
            if timer_status:
                time = float(self.view.lower_motor_frame.motor5_timer_entry.get())
                self.lower_controller.motor5_rotate_left(self.adc_status, pwm, time, delay)
            else:
                self.lower_controller.motor5_rotate_left(self.adc_status, pwm, delay=delay)
        else:
            print('LM5L - args len not 0')
            self.lower_controller.motor5_rotate_left(pwm=args[0], time_limited=args[1], delay=args[2])

    def lower_motor5_rotate_right(self, args=None):
        if args is None:
            timer_status = self.view.lower_motor_frame.motor5_timer_status.get()
            pwm = self.lower_motor_frame.motor5_pwm_scale.get()
            delay = self.model.convert_delay(self.view.lower_motor_frame.motor5_delay_entry.get())
            if timer_status:
                time = float(self.view.lower_motor_frame.motor5_timer_entry.get())
                self.lower_controller.motor5_rotate_right(self.adc_status, pwm, time, delay)
            else:
                self.lower_controller.motor5_rotate_right(self.adc_status, pwm, delay=delay)
        else:
            print('LM5R - args len not 0')
            self.lower_controller.motor5_rotate_right(pwm=args[0], time_limited=args[1], delay=args[2])

    def lower_motor5_rotate_stop(self):
        self.lower_controller.motor5_rotate_stop()


if __name__ == '__main__':
    root = Tk()
    root['bg'] = '#0585e8'
    root.title('Motor Client')
    root.geometry('1600x900')
    photo = PhotoImage(file="../../Images/cyber_hand.png")
    root.iconphoto(False, photo)
    root.resizable(width=False, height=False)

    application = Controller(root)
    root.mainloop()
