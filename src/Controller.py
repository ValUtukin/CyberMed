from View import View
from Model import Model
from tkinter import *
from pubsub import pub
import comport as com
from MotorController import MotorController


class Controller:
    def __init__(self, parent):
        self.parent = parent
        self.upper_comport = com.ini('COM7')
        self.lower_comport = com.ini('COM2')
        self.model = Model()
        self.view = View(parent)
        self.view.setup()

        self.upper_motors_frame = self.view.upper_motors_frame
        self.lower_motors_frame = self.view.lower_motors_frame

        self.upper_controller = MotorController(self.upper_comport, 'Upper')
        self.lower_controller = MotorController(self.lower_comport, 'Lower')

        self.adc_status = False
        self.global_timer_status = False
        self.global_timer_time = 0.0

        pub.subscribe(self.upper_power_switch, "Upper_power_switch")
        pub.subscribe(self.lower_power_switch, "Lower_power_switch")

        pub.subscribe(self.upper_motor1_rotate_left, "Upper_motor1_rotate_left")
        pub.subscribe(self.upper_motor1_rotate_right, "Upper_motor1_rotate_right")
        pub.subscribe(self.upper_motor1_rotate_stop, "Upper_motor1_rotate_stop")
        pub.subscribe(self.upper_motor1_adc_change, "Upper_motor1_adc_change")

        pub.subscribe(self.upper_motor2_rotate_left, "Upper_motor2_rotate_left")
        pub.subscribe(self.upper_motor2_rotate_right, "Upper_motor2_rotate_right")
        pub.subscribe(self.upper_motor2_rotate_stop, "Upper_motor2_rotate_stop")
        pub.subscribe(self.upper_motor2_adc_change, "Upper_motor2_adc_change")

        pub.subscribe(self.upper_motor3_rotate_left, "Upper_motor3_rotate_left")
        pub.subscribe(self.upper_motor3_rotate_right, "Upper_motor3_rotate_right")
        pub.subscribe(self.upper_motor3_rotate_stop, "Upper_motor3_rotate_stop")
        pub.subscribe(self.upper_motor3_adc_change, "Upper_motor3_adc_change")

        pub.subscribe(self.upper_motor4_rotate_left, "Upper_motor4_rotate_left")
        pub.subscribe(self.upper_motor4_rotate_right, "Upper_motor4_rotate_right")
        pub.subscribe(self.upper_motor4_rotate_stop, "Upper_motor4_rotate_stop")
        pub.subscribe(self.upper_motor4_adc_change, "Upper_motor4_adc_change")

        pub.subscribe(self.upper_motor5_rotate_left, "Upper_motor5_rotate_left")
        pub.subscribe(self.upper_motor5_rotate_right, "Upper_motor5_rotate_right")
        pub.subscribe(self.upper_motor5_rotate_stop, "Upper_motor5_rotate_stop")
        pub.subscribe(self.upper_motor5_adc_change, "Upper_motor5_adc_change")

        pub.subscribe(self.lower_motor1_rotate_left, "Lower_motor1_rotate_left")
        pub.subscribe(self.lower_motor1_rotate_right, "Lower_motor1_rotate_right")
        pub.subscribe(self.lower_motor1_rotate_stop, "Lower_motor1_rotate_stop")
        pub.subscribe(self.lower_motor1_adc_change, "Lower_motor1_adc_change")

        pub.subscribe(self.lower_motor2_rotate_left, "Lower_motor2_rotate_left")
        pub.subscribe(self.lower_motor2_rotate_right, "Lower_motor2_rotate_right")
        pub.subscribe(self.lower_motor2_rotate_stop, "Lower_motor2_rotate_stop")
        pub.subscribe(self.lower_motor2_adc_change, "Lower_motor2_adc_change")

        pub.subscribe(self.lower_motor3_rotate_left, "Lower_motor3_rotate_left")
        pub.subscribe(self.lower_motor3_rotate_right, "Lower_motor3_rotate_right")
        pub.subscribe(self.lower_motor3_rotate_stop, "Lower_motor3_rotate_stop")
        pub.subscribe(self.lower_motor3_adc_change, "Lower_motor3_adc_change")

        pub.subscribe(self.lower_motor4_rotate_left, "Lower_motor4_rotate_left")
        pub.subscribe(self.lower_motor4_rotate_right, "Lower_motor4_rotate_right")
        pub.subscribe(self.lower_motor4_rotate_stop, "Lower_motor4_rotate_stop")
        pub.subscribe(self.lower_motor4_adc_change, "Lower_motor4_adc_change")

        pub.subscribe(self.lower_motor5_rotate_left, "Lower_motor5_rotate_left")
        pub.subscribe(self.lower_motor5_rotate_right, "Lower_motor5_rotate_right")
        pub.subscribe(self.lower_motor5_rotate_stop, "Lower_motor5_rotate_stop")
        pub.subscribe(self.lower_motor5_adc_change, "Lower_motor5_adc_change")

    def power_switch(self, comport, power_status):
        if power_status:
            com.send_command(comport, config='00000001', power_byte='00000001')
        else:
            com.send_command(comport, config='00000001', power_byte='00000000')

    def upper_power_switch(self):
        upper_power_status = self.upper_motors_frame.power_status.get()
        self.power_switch(self.upper_comport, upper_power_status)

    def lower_power_switch(self):
        lower_power_status = self.lower_motors_frame.power_status.get()
        self.power_switch(self.lower_comport, lower_power_status)

    def upper_motor1_rotate_left(self):
        timer_status = self.view.upper_motors_frame.motor1_timer_status.get()
        pwm = self.upper_motors_frame.motor1_pwm_scale.get()
        delay = self.model.convert_delay(self.view.upper_motors_frame.motor1_delay_entry.get())
        if timer_status:
            time = float(self.view.upper_motors_frame.motor1_timer_entry.get())
            self.upper_controller.motor1_rotate_left(self.adc_status, pwm, time, delay)
        else:
            self.upper_controller.motor1_rotate_left(self.adc_status, pwm, delay=delay)

    def upper_motor1_rotate_right(self):
        timer_status = self.view.upper_motors_frame.motor1_timer_status.get()
        pwm = self.upper_motors_frame.motor1_pwm_scale.get()
        delay = self.model.convert_delay(self.view.upper_motors_frame.motor1_delay_entry.get())
        if timer_status:
            time = float(self.view.upper_motors_frame.motor1_timer_entry.get())
            self.upper_controller.motor1_rotate_right(self.adc_status, pwm, time, delay)
        else:
            self.upper_controller.motor1_rotate_right(self.adc_status, pwm, delay=delay)

    def upper_motor1_rotate_stop(self):
        self.upper_controller.motor1_rotate_stop()

    def upper_motor1_adc_change(self):
        self.model.send_adc(self.upper_comport, self.upper_motors_frame)

    def upper_motor2_rotate_left(self):
        timer_status = self.view.upper_motors_frame.motor2_timer_status.get()
        pwm = self.upper_motors_frame.motor2_pwm_scale.get()
        delay = self.model.convert_delay(self.view.upper_motors_frame.motor2_delay_entry.get())
        if timer_status:
            time = float(self.view.upper_motors_frame.motor2_timer_entry.get())
            self.upper_controller.motor2_rotate_left(self.adc_status, pwm, time, delay)
        else:
            self.upper_controller.motor2_rotate_left(self.adc_status, pwm, delay=delay)

    def upper_motor2_rotate_right(self):
        timer_status = self.view.upper_motors_frame.motor2_timer_status.get()
        pwm = self.upper_motors_frame.motor2_pwm_scale.get()
        delay = self.model.convert_delay(self.view.upper_motors_frame.motor2_delay_entry.get())
        if timer_status:
            time = float(self.view.upper_motors_frame.motor2_timer_entry.get())
            self.upper_controller.motor2_rotate_right(self.adc_status, pwm, time, delay)
        else:
            self.upper_controller.motor2_rotate_right(self.adc_status, pwm, delay=delay)

    def upper_motor2_rotate_stop(self):
        self.upper_controller.motor2_rotate_stop()

    def upper_motor2_adc_change(self):
        self.model.send_adc(self.upper_comport, self.upper_motors_frame)

    def upper_motor3_rotate_left(self):
        timer_status = self.view.upper_motors_frame.motor3_timer_status.get()
        pwm = self.upper_motors_frame.motor3_pwm_scale.get()
        delay = self.model.convert_delay(self.view.upper_motors_frame.motor3_delay_entry.get())
        if timer_status:
            time = float(self.view.upper_motors_frame.motor3_timer_entry.get())
            self.upper_controller.motor3_rotate_left(self.adc_status, pwm, time, delay)
        else:
            self.upper_controller.motor3_rotate_left(self.adc_status, pwm, delay=delay)

    def upper_motor3_rotate_right(self):
        timer_status = self.view.upper_motors_frame.motor3_timer_status.get()
        pwm = self.upper_motors_frame.motor3_pwm_scale.get()
        delay = self.model.convert_delay(self.view.upper_motors_frame.motor3_delay_entry.get())
        if timer_status:
            time = float(self.view.upper_motors_frame.motor3_timer_entry.get())
            self.upper_controller.motor3_rotate_right(self.adc_status, pwm, time, delay)
        else:
            self.upper_controller.motor3_rotate_right(self.adc_status, pwm, delay=delay)

    def upper_motor3_rotate_stop(self):
        self.upper_controller.motor3_rotate_stop()

    def upper_motor3_adc_change(self):
        self.model.send_adc(self.upper_comport, self.upper_motors_frame)

    def upper_motor4_rotate_left(self):
        timer_status = self.view.upper_motors_frame.motor4_timer_status.get()
        pwm = self.upper_motors_frame.motor4_pwm_scale.get()
        delay = self.model.convert_delay(self.view.upper_motors_frame.motor4_delay_entry.get())
        if timer_status:
            time = float(self.view.upper_motors_frame.motor4_timer_entry.get())
            self.upper_controller.motor4_rotate_left(self.adc_status, pwm, time, delay)
        else:
            self.upper_controller.motor4_rotate_left(self.adc_status, pwm, delay=delay)

    def upper_motor4_rotate_right(self):
        timer_status = self.view.upper_motors_frame.motor4_timer_status.get()
        pwm = self.upper_motors_frame.motor4_pwm_scale.get()
        delay = self.model.convert_delay(self.view.upper_motors_frame.motor4_delay_entry.get())
        if timer_status:
            time = float(self.view.upper_motors_frame.motor4_timer_entry.get())
            self.upper_controller.motor4_rotate_right(self.adc_status, pwm, time, delay)
        else:
            self.upper_controller.motor4_rotate_right(self.adc_status, pwm, delay=delay)

    def upper_motor4_rotate_stop(self):
        self.upper_controller.motor4_rotate_stop()

    def upper_motor4_adc_change(self):
        self.model.send_adc(self.upper_comport, self.upper_motors_frame)

    def upper_motor5_rotate_left(self):
        timer_status = self.view.upper_motors_frame.motor5_timer_status.get()
        pwm = self.upper_motors_frame.motor5_pwm_scale.get()
        delay = self.model.convert_delay(self.view.upper_motors_frame.motor5_delay_entry.get())
        if timer_status:
            time = float(self.view.upper_motors_frame.motor5_timer_entry.get())
            self.upper_controller.motor5_rotate_left(self.adc_status, pwm, time, delay)
        else:
            self.upper_controller.motor5_rotate_left(self.adc_status, pwm, delay=delay)

    def upper_motor5_rotate_right(self):
        timer_status = self.view.upper_motors_frame.motor5_timer_status.get()
        pwm = self.upper_motors_frame.motor5_pwm_scale.get()
        delay = self.model.convert_delay(self.view.upper_motors_frame.motor5_delay_entry.get())
        if timer_status:
            time = float(self.view.upper_motors_frame.motor5_timer_entry.get())
            self.upper_controller.motor5_rotate_right(self.adc_status, pwm, time, delay)
        else:
            self.upper_controller.motor5_rotate_right(self.adc_status, pwm, delay=delay)

    def upper_motor5_rotate_stop(self):
        self.upper_controller.motor5_rotate_stop()

    def upper_motor5_adc_change(self):
        self.model.send_adc(self.upper_comport, self.upper_motors_frame)

    def lower_motor1_rotate_left(self):
        timer_status = self.view.lower_motors_frame.motor1_timer_status.get()
        pwm = self.lower_motors_frame.motor1_pwm_scale.get()
        delay = self.model.convert_delay(self.view.lower_motors_frame.motor1_delay_entry.get())
        if timer_status:
            time = float(self.view.lower_motors_frame.motor1_timer_entry.get())
            self.lower_controller.motor1_rotate_left(self.adc_status, pwm, time, delay)
        else:
            self.lower_controller.motor1_rotate_left(self.adc_status, pwm, delay=delay)

    def lower_motor1_rotate_right(self):
        timer_status = self.view.lower_motors_frame.motor1_timer_status.get()
        pwm = self.lower_motors_frame.motor1_pwm_scale.get()
        delay = self.model.convert_delay(self.view.lower_motors_frame.motor1_delay_entry.get())
        if timer_status:
            time = float(self.view.lower_motors_frame.motor1_timer_entry.get())
            self.lower_controller.motor1_rotate_right(self.adc_status, pwm, time, delay)
        else:
            self.lower_controller.motor1_rotate_right(self.adc_status, pwm, delay=delay)

    def lower_motor1_rotate_stop(self):
        self.lower_controller.motor1_rotate_stop()

    def lower_motor1_adc_change(self):
        self.model.send_adc(self.lower_comport, self.lower_motors_frame)

    def lower_motor2_rotate_left(self):
        timer_status = self.view.lower_motors_frame.motor2_timer_status.get()
        pwm = self.lower_motors_frame.motor2_pwm_scale.get()
        delay = self.model.convert_delay(self.view.lower_motors_frame.motor2_delay_entry.get())
        if timer_status:
            time = float(self.view.lower_motors_frame.motor2_timer_entry.get())
            self.lower_controller.motor2_rotate_left(self.adc_status, pwm, time, delay)
        else:
            self.lower_controller.motor2_rotate_left(self.adc_status, pwm, delay=delay)

    def lower_motor2_rotate_right(self):
        timer_status = self.view.lower_motors_frame.motor2_timer_status.get()
        pwm = self.lower_motors_frame.motor2_pwm_scale.get()
        delay = self.model.convert_delay(self.view.lower_motors_frame.motor2_delay_entry.get())
        if timer_status:
            time = float(self.view.lower_motors_frame.motor2_timer_entry.get())
            self.lower_controller.motor2_rotate_right(self.adc_status, pwm, time, delay)
        else:
            self.lower_controller.motor2_rotate_right(self.adc_status, pwm, delay=delay)

    def lower_motor2_rotate_stop(self):
        self.lower_controller.motor2_rotate_stop()

    def lower_motor2_adc_change(self):
        self.model.send_adc(self.lower_comport, self.lower_motors_frame)

    def lower_motor3_rotate_left(self):
        timer_status = self.view.lower_motors_frame.motor3_timer_status.get()
        pwm = self.lower_motors_frame.motor3_pwm_scale.get()
        delay = self.model.convert_delay(self.view.lower_motors_frame.motor3_delay_entry.get())
        if timer_status:
            time = float(self.view.lower_motors_frame.motor3_timer_entry.get())
            self.lower_controller.motor3_rotate_left(self.adc_status, pwm, time, delay)
        else:
            self.lower_controller.motor3_rotate_left(self.adc_status, pwm, delay=delay)

    def lower_motor3_rotate_right(self):
        timer_status = self.view.lower_motors_frame.motor3_timer_status.get()
        pwm = self.lower_motors_frame.motor3_pwm_scale.get()
        delay = self.model.convert_delay(self.view.lower_motors_frame.motor3_delay_entry.get())
        if timer_status:
            time = float(self.view.lower_motors_frame.motor3_timer_entry.get())
            self.lower_controller.motor3_rotate_right(self.adc_status, pwm, time, delay)
        else:
            self.lower_controller.motor3_rotate_right(self.adc_status, pwm, delay=delay)

    def lower_motor3_rotate_stop(self):
        self.lower_controller.motor3_rotate_stop()

    def lower_motor3_adc_change(self):
        self.model.send_adc(self.lower_comport, self.lower_motors_frame)

    def lower_motor4_rotate_left(self):
        timer_status = self.view.lower_motors_frame.motor4_timer_status.get()
        pwm = self.lower_motors_frame.motor4_pwm_scale.get()
        delay = self.model.convert_delay(self.view.lower_motors_frame.motor4_delay_entry.get())
        if timer_status:
            time = float(self.view.lower_motors_frame.motor4_timer_entry.get())
            self.lower_controller.motor4_rotate_left(self.adc_status, pwm, time, delay)
        else:
            self.lower_controller.motor4_rotate_left(self.adc_status, pwm, delay=delay)

    def lower_motor4_rotate_right(self):
        timer_status = self.view.lower_motors_frame.motor4_timer_status.get()
        pwm = self.lower_motors_frame.motor4_pwm_scale.get()
        delay = self.view.lower_motors_frame.motor4_delay_entry.get()
        if delay == '':
            delay = 0.0
        else:
            delay = float(self.view.lower_motors_frame.motor4_delay_entry.get())
        if timer_status:
            time = float(self.view.lower_motors_frame.motor4_timer_entry.get())
            self.lower_controller.motor4_rotate_right(self.adc_status, pwm, time, delay)
        else:
            self.lower_controller.motor4_rotate_right(self.adc_status, pwm, delay=delay)

    def lower_motor4_rotate_stop(self):
        self.lower_controller.motor4_rotate_stop()

    def lower_motor4_adc_change(self):
        self.model.send_adc(self.lower_comport, self.lower_motors_frame)

    def lower_motor5_rotate_left(self):
        timer_status = self.view.lower_motors_frame.motor5_timer_status.get()
        pwm = self.lower_motors_frame.motor5_pwm_scale.get()
        delay = self.view.lower_motors_frame.motor5_delay_entry.get()
        if delay == '':
            delay = 0.0
        else:
            delay = float(self.view.lower_motors_frame.motor5_delay_entry.get())
        if timer_status:
            time = float(self.view.lower_motors_frame.motor5_timer_entry.get())
            self.lower_controller.motor5_rotate_left(self.adc_status, pwm, time, delay)
        else:
            self.lower_controller.motor5_rotate_left(self.adc_status, pwm, delay=delay)

    def lower_motor5_rotate_right(self):
        timer_status = self.view.lower_motors_frame.motor5_timer_status.get()
        pwm = self.lower_motors_frame.motor5_pwm_scale.get()
        delay = self.view.lower_motors_frame.motor5_delay_entry.get()
        if delay == '':
            delay = 0.0
        else:
            delay = float(self.view.lower_motors_frame.motor5_delay_entry.get())
        if timer_status:
            time = float(self.view.lower_motors_frame.motor5_timer_entry.get())
            self.lower_controller.motor5_rotate_right(self.adc_status, pwm, time, delay)
        else:
            self.lower_controller.motor5_rotate_right(self.adc_status, pwm, delay=delay)

    def lower_motor5_rotate_stop(self):
        self.lower_controller.motor5_rotate_stop()

    def lower_motor5_adc_change(self):
        self.model.send_adc(self.lower_comport, self.lower_motors_frame)


if __name__ == '__main__':
    root = Tk()
    root['bg'] = '#0585e8'
    root.title('Motor Client')
    root.geometry('1600x900')
    photo = PhotoImage(file="../Images/cyber_hand.png")
    root.iconphoto(False, photo)
    root.resizable(width=False, height=False)

    application = Controller(root)
    root.mainloop()
