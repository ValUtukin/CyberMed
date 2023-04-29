from View import View
from Model import Model
from tkinter import *
from pubsub import pub
import comport as com
from MotorController import MotorController


class Controller:
    def __init__(self, parent):
        self.parent = parent
        self.comport = com.ini('COM3')
        self.model = Model(self.comport)
        self.view = View(parent)
        self.view.setup()

        self.upper_motors_frame = self.view.upper_motors_frame
        self.lower_motors_frame = self.view.lower_motors_frame

        self.upper_controller = MotorController(self.comport, 'Upper')
        self.lower_controller = MotorController(self.comport, 'Lower')

        self.adc_status = False
        self.global_timer_status = False
        self.global_timer_time = 0.0

        pub.subscribe(self.adc_switch, "Adc_switch")
        pub.subscribe(self.global_timer_switch, "Global_timer_switch")
        pub.subscribe(self.power_switch, "Power_switch")

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

    def adc_switch(self):
        self.adc_status = self.view.adc_status.get()

    def global_timer_switch(self):
        self.global_timer_status = self.view.global_timer_status.get()
        if self.global_timer_status:
            self.global_timer_time = float(self.view.global_timer_entry.get())

    def power_switch(self):
        power_status = self.view.power_status.get()
        if power_status:
            com.send_command(self.comport, config='00000001', power_byte='00000001')
        else:
            com.send_command(self.comport, config='00000001', power_byte='00000000')

    def upper_motor1_rotate_left(self):
        local_timer_status = self.view.upper_motors_frame.motor1_timer_status.get()
        pwm = self.upper_motors_frame.motor1_pwm_scale.get()
        if local_timer_status:  # Local timer has bigger priority. So if local time was given, so here we go that time
            time = float(self.view.upper_motors_frame.motor1_timer_entry.get())
            self.upper_controller.motor1_rotate_left(self.adc_status, pwm, time)
        else:
            if self.global_timer_status:  # If local time is False, we check is there global time (low priority).
                time = self.global_timer_time
                self.upper_controller.motor1_rotate_left(self.adc_status, pwm, time)
            else:  # If no time limits, here we go in unlimited rotation
                self.upper_controller.motor1_rotate_left(self.adc_status, pwm)

    def upper_motor1_rotate_right(self):
        local_timer_status = self.view.upper_motors_frame.motor1_timer_status.get()
        pwm = self.upper_motors_frame.motor1_pwm_scale.get()
        if local_timer_status:
            time = float(self.view.upper_motors_frame.motor1_timer_entry.get())
            self.upper_controller.motor1_rotate_right(self.adc_status, pwm, time)
        else:
            if self.global_timer_status:
                time = self.global_timer_time
                self.upper_controller.motor1_rotate_right(self.adc_status, pwm, time)
            else:
                self.upper_controller.motor1_rotate_right(self.adc_status, pwm)

    def upper_motor1_rotate_stop(self):
        self.upper_controller.motor1_rotate_stop()

    def upper_motor2_rotate_left(self):
        local_timer_status = self.view.upper_motors_frame.motor2_timer_status.get()
        pwm = self.upper_motors_frame.motor2_pwm_scale.get()
        if local_timer_status:
            time = float(self.view.upper_motors_frame.motor2_timer_entry.get())
            self.upper_controller.motor2_rotate_left(self.adc_status, pwm, time)
        else:
            if self.global_timer_status:
                time = self.global_timer_time
                self.upper_controller.motor2_rotate_left(self.adc_status, pwm, time)
            else:
                self.upper_controller.motor2_rotate_left(self.adc_status, pwm)

    def upper_motor2_rotate_right(self):
        local_timer_status = self.view.upper_motors_frame.motor2_timer_status.get()
        pwm = self.upper_motors_frame.motor2_pwm_scale.get()
        if local_timer_status:
            time = float(self.view.upper_motors_frame.motor2_timer_entry.get())
            self.upper_controller.motor2_rotate_right(self.adc_status, pwm, time)
        else:
            if self.global_timer_status:
                time = self.global_timer_time
                self.upper_controller.motor2_rotate_right(self.adc_status, pwm, time)
            else:
                self.upper_controller.motor2_rotate_right(self.adc_status, pwm)

    def upper_motor2_rotate_stop(self):
        self.upper_controller.motor2_rotate_stop()

    def upper_motor3_rotate_left(self):
        local_timer_status = self.view.upper_motors_frame.motor3_timer_status.get()
        pwm = self.upper_motors_frame.motor3_pwm_scale.get()
        if local_timer_status:
            time = float(self.view.upper_motors_frame.motor3_timer_entry.get())
            self.upper_controller.motor3_rotate_left(self.adc_status, pwm, time)
        else:
            if self.global_timer_status:
                time = self.global_timer_time
                self.upper_controller.motor3_rotate_left(self.adc_status, pwm, time)
            else:
                self.upper_controller.motor3_rotate_left(self.adc_status, pwm)

    def upper_motor3_rotate_right(self):
        local_timer_status = self.view.upper_motors_frame.motor3_timer_status.get()
        pwm = self.upper_motors_frame.motor3_pwm_scale.get()
        if local_timer_status:
            time = float(self.view.upper_motors_frame.motor3_timer_entry.get())
            self.upper_controller.motor3_rotate_right(self.adc_status, pwm, time)
        else:
            if self.global_timer_status:
                time = self.global_timer_time
                self.upper_controller.motor3_rotate_right(self.adc_status, pwm, time)
            else:
                self.upper_controller.motor3_rotate_right(self.adc_status, pwm)

    def upper_motor3_rotate_stop(self):
        self.upper_controller.motor3_rotate_stop()

    def upper_motor4_rotate_left(self):
        local_timer_status = self.view.upper_motors_frame.motor4_timer_status.get()
        pwm = self.upper_motors_frame.motor4_pwm_scale.get()
        if local_timer_status:
            time = float(self.view.upper_motors_frame.motor4_timer_entry.get())
            self.upper_controller.motor4_rotate_left(self.adc_status, pwm, time)
        else:
            if self.global_timer_status:
                time = self.global_timer_time
                self.upper_controller.motor4_rotate_left(self.adc_status, pwm, time)
            else:
                self.upper_controller.motor4_rotate_left(self.adc_status, pwm)

    def upper_motor4_rotate_right(self):
        local_timer_status = self.view.upper_motors_frame.motor4_timer_status.get()
        pwm = self.upper_motors_frame.motor4_pwm_scale.get()
        if local_timer_status:
            time = float(self.view.upper_motors_frame.motor4_timer_entry.get())
            self.upper_controller.motor4_rotate_right(self.adc_status, pwm, time)
        else:
            if self.global_timer_status:
                time = self.global_timer_time
                self.upper_controller.motor4_rotate_right(self.adc_status, pwm, time)
            else:
                self.upper_controller.motor4_rotate_right(self.adc_status, pwm)

    def upper_motor4_rotate_stop(self):
        self.upper_controller.motor4_rotate_stop()

    def upper_motor5_rotate_left(self):
        local_timer_status = self.view.upper_motors_frame.motor5_timer_status.get()
        pwm = self.upper_motors_frame.motor5_pwm_scale.get()
        if local_timer_status:
            time = float(self.view.upper_motors_frame.motor5_timer_entry.get())
            self.upper_controller.motor5_rotate_left(self.adc_status, pwm, time)
        else:
            if self.global_timer_status:
                time = self.global_timer_time
                self.upper_controller.motor5_rotate_left(self.adc_status, pwm, time)
            else:
                self.upper_controller.motor5_rotate_left(self.adc_status, pwm)

    def upper_motor5_rotate_right(self):
        local_timer_status = self.view.upper_motors_frame.motor5_timer_status.get()
        pwm = self.upper_motors_frame.motor5_pwm_scale.get()
        if local_timer_status:
            time = float(self.view.upper_motors_frame.motor5_timer_entry.get())
            self.upper_controller.motor5_rotate_right(self.adc_status, pwm, time)
        else:
            if self.global_timer_status:
                time = self.global_timer_time
                self.upper_controller.motor5_rotate_right(self.adc_status, pwm, time)

    def upper_motor5_rotate_stop(self):
        self.upper_controller.motor5_rotate_stop()

    def lower_motor1_rotate_left(self):
        local_timer_status = self.view.lower_motors_frame.motor1_timer_status.get()
        pwm = self.lower_motors_frame.motor1_pwm_scale.get()
        if local_timer_status:  # Local timer has bigger priority. So if local time was given, so here we go that time
            time = float(self.view.lower_motors_frame.motor1_timer_entry.get())
            self.lower_controller.motor1_rotate_left(self.adc_status, pwm, time)
        else:
            if self.global_timer_status:  # If local time is False, we check is there global time (low priority).
                time = self.global_timer_time
                self.lower_controller.motor1_rotate_left(self.adc_status, pwm, time)
            else:  # If no time limits, here we go in unlimited rotation
                self.lower_controller.motor1_rotate_left(self.adc_status, pwm)

    def lower_motor1_rotate_right(self):
        local_timer_status = self.view.lower_motors_frame.motor1_timer_status.get()
        pwm = self.lower_motors_frame.motor1_pwm_scale.get()
        if local_timer_status:
            time = float(self.view.lower_motors_frame.motor1_timer_entry.get())
            self.lower_controller.motor1_rotate_right(self.adc_status, pwm, time)
        else:
            if self.global_timer_status:
                time = self.global_timer_time
                self.lower_controller.motor1_rotate_right(self.adc_status, pwm, time)
            print("Incorrect PWM")

    def lower_motor1_rotate_stop(self):
        self.lower_controller.motor1_rotate_stop()

    def lower_motor2_rotate_left(self):
        local_timer_status = self.view.lower_motors_frame.motor2_timer_status.get()
        pwm = self.lower_motors_frame.motor2_pwm_scale.get()
        if local_timer_status:
            time = float(self.view.lower_motors_frame.motor2_timer_entry.get())
            self.lower_controller.motor2_rotate_left(self.adc_status, pwm, time)
        else:
            if self.global_timer_status:
                time = self.global_timer_time
                self.lower_controller.motor2_rotate_left(self.adc_status, pwm, time)
            else:
                self.lower_controller.motor2_rotate_left(self.adc_status, pwm)

    def lower_motor2_rotate_right(self):
        local_timer_status = self.view.lower_motors_frame.motor2_timer_status.get()
        pwm = self.lower_motors_frame.motor2_pwm_scale.get()
        if local_timer_status:
            time = float(self.view.lower_motors_frame.motor2_timer_entry.get())
            self.lower_controller.motor2_rotate_right(self.adc_status, pwm, time)
        else:
            if self.global_timer_status:
                time = self.global_timer_time
                self.lower_controller.motor2_rotate_right(self.adc_status, pwm, time)
            else:
                self.lower_controller.motor2_rotate_right(self.adc_status, pwm)

    def lower_motor2_rotate_stop(self):
        self.lower_controller.motor2_rotate_stop()

    def lower_motor3_rotate_left(self):
        local_timer_status = self.view.lower_motors_frame.motor3_timer_status.get()
        pwm = self.lower_motors_frame.motor3_pwm_scale.get()
        if local_timer_status:
            time = float(self.view.lower_motors_frame.motor3_timer_entry.get())
            self.lower_controller.motor3_rotate_left(self.adc_status, pwm, time)
        else:
            if self.global_timer_status:
                time = self.global_timer_time
                self.lower_controller.motor3_rotate_left(self.adc_status, pwm, time)
            else:
                self.lower_controller.motor3_rotate_left(self.adc_status, pwm)

    def lower_motor3_rotate_right(self):
        local_timer_status = self.view.lower_motors_frame.motor3_timer_status.get()
        pwm = self.lower_motors_frame.motor3_pwm_scale.get()
        if local_timer_status:
            time = float(self.view.lower_motors_frame.motor3_timer_entry.get())
            self.lower_controller.motor3_rotate_right(self.adc_status, pwm, time)
        else:
            if self.global_timer_status:
                time = self.global_timer_time
                self.lower_controller.motor3_rotate_right(self.adc_status, pwm, time)
            else:
                self.lower_controller.motor3_rotate_right(self.adc_status, pwm)

    def lower_motor3_rotate_stop(self):
        self.lower_controller.motor3_rotate_stop()

    def lower_motor4_rotate_left(self):
        local_timer_status = self.view.lower_motors_frame.motor4_timer_status.get()
        pwm = self.lower_motors_frame.motor4_pwm_scale.get()
        if local_timer_status:
            time = float(self.view.lower_motors_frame.motor4_timer_entry.get())
            self.lower_controller.motor4_rotate_left(self.adc_status, pwm, time)
        else:
            if self.global_timer_status:
                time = self.global_timer_time
                self.lower_controller.motor4_rotate_left(self.adc_status, pwm, time)
            else:
                self.lower_controller.motor4_rotate_left(self.adc_status, pwm)

    def lower_motor4_rotate_right(self):
        local_timer_status = self.view.lower_motors_frame.motor4_timer_status.get()
        pwm = self.lower_motors_frame.motor4_pwm_scale.get()
        if local_timer_status:
            time = float(self.view.lower_motors_frame.motor4_timer_entry.get())
            self.lower_controller.motor4_rotate_right(self.adc_status, pwm, time)
        else:
            if self.global_timer_status:
                time = self.global_timer_time
                self.lower_controller.motor4_rotate_right(self.adc_status, pwm, time)
            else:
                self.lower_controller.motor4_rotate_right(self.adc_status, pwm)

    def lower_motor4_rotate_stop(self):
        self.lower_controller.motor4_rotate_stop()

    def lower_motor5_rotate_left(self):
        local_timer_status = self.view.lower_motors_frame.motor5_timer_status.get()
        pwm = self.lower_motors_frame.motor5_pwm_scale.get()
        if local_timer_status:
            time = float(self.view.lower_motors_frame.motor5_timer_entry.get())
            self.lower_controller.motor5_rotate_left(self.adc_status, pwm, time)
        else:
            if self.global_timer_status:
                time = self.global_timer_time
                self.lower_controller.motor5_rotate_left(self.adc_status, pwm, time)
            else:
                self.lower_controller.motor5_rotate_left(self.adc_status, pwm)

    def lower_motor5_rotate_right(self):
        local_timer_status = self.view.lower_motors_frame.motor5_timer_status.get()
        pwm = self.lower_motors_frame.motor5_pwm_scale.get()
        if local_timer_status:
            time = float(self.view.lower_motors_frame.motor5_timer_entry.get())
            self.lower_controller.motor5_rotate_right(self.adc_status, pwm, time)
        else:
            if self.global_timer_status:
                time = self.global_timer_time
                self.lower_controller.motor5_rotate_right(self.adc_status, pwm, time)
            else:
                self.lower_controller.motor5_rotate_right(self.adc_status, pwm)

    def lower_motor5_rotate_stop(self):
        self.lower_controller.motor5_rotate_stop()


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
