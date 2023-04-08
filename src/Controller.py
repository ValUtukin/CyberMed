from View import View
from Model import Model
from tkinter import *
from pubsub import pub
import comport as com
import threading as thread
import time


class Controller:
    def __init__(self, parent):
        self.parent = parent
        self.comport = com.ini('COM2')
        self.model = Model(self.comport)
        self.view = View(parent)
        self.view.setup()

        pub.subscribe(self.power_switch, "Power_switch")

        pub.subscribe(self.motor1_rotate_left, "Motor1_rotate_left")
        pub.subscribe(self.motor1_rotate_right, "Motor1_rotate_right")
        pub.subscribe(self.motor1_rotate_stop, "Motor1_rotate_stop")
        pub.subscribe(self.motor1_pwm_scal_change, "Motor1_pwm_scale_change")

        pub.subscribe(self.motor2_rotate_left, "Motor2_rotate_left")
        pub.subscribe(self.motor2_rotate_right, "Motor2_rotate_right")
        pub.subscribe(self.motor2_rotate_stop, "Motor2_rotate_stop")

        pub.subscribe(self.motor3_rotate_left, "Motor3_rotate_left")
        pub.subscribe(self.motor3_rotate_right, "Motor3_rotate_right")
        pub.subscribe(self.motor3_rotate_stop, "Motor3_rotate_stop")

        pub.subscribe(self.motor4_rotate_left, "Motor4_rotate_left")
        pub.subscribe(self.motor4_rotate_right, "Motor4_rotate_right")
        pub.subscribe(self.motor4_rotate_stop, "Motor4_rotate_stop")

        pub.subscribe(self.motor5_rotate_left, "Motor5_rotate_left")
        pub.subscribe(self.motor5_rotate_right, "Motor5_rotate_right")
        pub.subscribe(self.motor5_rotate_stop, "Motor5_rotate_stop")

    def power_switch(self):
        power_status = self.view.power_status.get()
        if power_status:
            com.send_command(self.comport, config='00000001', power_byte='00000001')
        else:
            com.send_command(self.comport, config='00000001', power_byte='00000000')

    def motor1_pwm_scal_change(self):  # code for get scale value and send it in dynamic mode
        pass
    #     pwm = self.view.motor1_pwm_scale.get()
    #     char_pwm = bytes(chr(pwm), 'ascii')
    #     com.send_command(self.comport, config='00000110', motor_byte='00001000', pwm_int=char_pwm)

    def motor1_rotate_left(self):
        pwm = self.view.motor1_pwm_scale.get()
        global_timer_status = self.view.global_timer_status.get()
        adc_status = self.view.adc_status.get()
        if adc_status:
            com.send_adc(self.comport, '00001000', '00000001')
            adc_thread = thread.Thread(target=self.model.get_adc_data)
            adc_thread.start()
        if self.model.validate_pwm(pwm):
            if global_timer_status:
                sec = float(self.view.global_timer_entry.get())
                time_limited_thread = thread.Thread(target=self.model.time_limited_motion,
                                                    args=('00000110', '00001000', pwm, sec,))
                time_limited_thread.start()
            elif self.view.motor1_timer_status.get():
                sec = float(self.view.motor1_timer_entry.get())
                time_limited_thread = thread.Thread(target=self.model.time_limited_motion,
                                                    args=('00000110', '00001000', pwm, sec,))
                time_limited_thread.start()
            else:
                char_pwm = bytes(chr(pwm), 'ascii')
                com.send_command(self.comport, config='00000110', motor_byte='00001000', pwm_int=char_pwm)
        else:
            print("Incorrect PWM")

    def motor1_rotate_right(self):
        pwm = self.view.motor1_pwm_scale.get()
        global_timer_status = self.view.global_timer_status.get()
        adc_status = self.view.adc_status.get()
        if adc_status:
            com.send_adc(self.comport, '00001000', '00000001')
            adc_thread = thread.Thread(target=self.model.get_adc_data)
            adc_thread.start()
        if self.model.validate_pwm(pwm):
            if global_timer_status:
                sec = float(self.view.global_timer_entry.get())
                time_limited_thread = thread.Thread(target=self.model.time_limited_motion,
                                                    args=('00000110', '00010000', pwm, sec,))
                time_limited_thread.start()
            elif self.view.motor1_timer_status.get():
                sec = float(self.view.motor1_timer_entry.get())
                time_limited_thread = thread.Thread(target=self.model.time_limited_motion,
                                                    args=('00000110', '00010000', pwm, sec,))
                time_limited_thread.start()
            else:
                char_pwm = bytes(chr(pwm), 'ascii')
                com.send_command(self.comport, config='00000110', motor_byte='00010000', pwm_int=char_pwm)
        else:
            print("Incorrect PWM")

    def motor1_rotate_stop(self):
        com.send_command(self.comport, config='00000010', motor_byte='00000000')

    def motor2_rotate_left(self):
        pwm = self.view.motor2_pwm_scale.get()
        global_timer_status = self.view.global_timer_status.get()
        adc_status = self.view.adc_status.get()
        if adc_status:
            com.send_adc(self.comport, '00001000', '00000001')
            adc_thread = thread.Thread(target=self.model.get_adc_data)
            adc_thread.start()
        if self.model.validate_pwm(pwm):
            if global_timer_status:
                sec = float(self.view.global_timer_entry.get())
                time_limited_thread = thread.Thread(target=self.model.time_limited_motion,
                                                    args=('00000110', '00001001', pwm, sec,))
                time_limited_thread.start()
            elif self.view.motor2_timer_status.get():
                sec = float(self.view.motor2_timer_entry.get())
                time_limited_thread = thread.Thread(target=self.model.time_limited_motion,
                                                    args=('00000110', '00001001', pwm, sec,))
                time_limited_thread.start()
            else:
                char_pwm = bytes(chr(pwm), 'ascii')
                com.send_command(self.comport, config='00000110', motor_byte='00001001', pwm_int=char_pwm)
        else:
            print("Incorrect PWM")

    def motor2_rotate_right(self):
        pwm = self.view.motor2_pwm_scale.get()
        global_timer_status = self.view.global_timer_status.get()
        adc_status = self.view.adc_status.get()
        if adc_status:
            com.send_adc(self.comport, '00001000', '00000001')
            adc_thread = thread.Thread(target=self.model.get_adc_data)
            adc_thread.start()
        if self.model.validate_pwm(pwm):
            if global_timer_status:
                sec = float(self.view.global_timer_entry.get())
                time_limited_thread = thread.Thread(target=self.model.time_limited_motion,
                                                    args=('00000110', '00010001', pwm, sec,))
                time_limited_thread.start()
            elif self.view.motor2_timer_status.get():
                sec = float(self.view.motor2_timer_entry.get())
                time_limited_thread = thread.Thread(target=self.model.time_limited_motion,
                                                    args=('00000110', '00010001', pwm, sec,))
                time_limited_thread.start()
            else:
                char_pwm = bytes(chr(pwm), 'ascii')
                com.send_command(self.comport, config='00000110', motor_byte='00010001', pwm_int=char_pwm)
        else:
            print("Incorrect PWM")

    def motor2_rotate_stop(self):
        com.send_command(self.comport, config='00000010', motor_byte='00000001')

    def motor3_rotate_left(self):
        pwm = self.view.motor3_pwm_scale.get()
        global_timer_status = self.view.global_timer_status.get()
        adc_status = self.view.adc_status.get()
        if adc_status:
            com.send_adc(self.comport, '00001000', '00000001')
            adc_thread = thread.Thread(target=self.model.get_adc_data)
            adc_thread.start()
        if self.model.validate_pwm(pwm):
            if global_timer_status:
                sec = float(self.view.global_timer_entry.get())
                time_limited_thread = thread.Thread(target=self.model.time_limited_motion,
                                                    args=('00000110', '00001010', pwm, sec,))
                time_limited_thread.start()
            elif self.view.motor3_timer_status.get():
                sec = float(self.view.motor3_timer_entry.get())
                time_limited_thread = thread.Thread(target=self.model.time_limited_motion,
                                                    args=('00000110', '00001010', pwm, sec,))
                time_limited_thread.start()
            else:
                char_pwm = bytes(chr(pwm), 'ascii')
                com.send_command(self.comport, config='00000110', motor_byte='00001010', pwm_int=char_pwm)
        else:
            print("Incorrect PWM")

    def motor3_rotate_right(self):
        pwm = self.view.motor3_pwm_scale.get()
        global_timer_status = self.view.global_timer_status.get()
        adc_status = self.view.adc_status.get()
        if adc_status:
            com.send_adc(self.comport, '00001000', '00000001')
            adc_thread = thread.Thread(target=self.model.get_adc_data)
            adc_thread.start()
        if self.model.validate_pwm(pwm):
            if global_timer_status:
                sec = float(self.view.global_timer_entry.get())
                time_limited_thread = thread.Thread(target=self.model.time_limited_motion,
                                                    args=('00000110', '00010010', pwm, sec,))
                time_limited_thread.start()
            elif self.view.motor3_timer_status.get():
                sec = float(self.view.motor3_timer_entry.get())
                time_limited_thread = thread.Thread(target=self.model.time_limited_motion,
                                                    args=('00000110', '00010010', pwm, sec,))
                time_limited_thread.start()
            else:
                char_pwm = bytes(chr(pwm), 'ascii')
                com.send_command(self.comport, config='00000110', motor_byte='00010010', pwm_int=char_pwm)
        else:
            print("Incorrect PWM")

    def motor3_rotate_stop(self):
        com.send_command(self.comport, config='00000010', motor_byte='00000010')

    def motor4_rotate_left(self):
        pwm = self.view.motor4_pwm_scale.get()
        global_timer_status = self.view.global_timer_status.get()
        adc_status = self.view.adc_status.get()
        if adc_status:
            com.send_adc(self.comport, '00001000', '00000001')
            adc_thread = thread.Thread(target=self.model.get_adc_data)
            adc_thread.start()
        if self.model.validate_pwm(pwm):
            if global_timer_status:
                sec = float(self.view.global_timer_entry.get())
                time_limited_thread = thread.Thread(target=self.model.time_limited_motion,
                                                    args=('00000110', '00001011', pwm, sec,))
                time_limited_thread.start()
            elif self.view.motor4_timer_status.get():
                sec = float(self.view.motor4_timer_entry.get())
                time_limited_thread = thread.Thread(target=self.model.time_limited_motion,
                                                    args=('00000110', '00001011', pwm, sec,))
                time_limited_thread.start()
            else:
                char_pwm = bytes(chr(pwm), 'ascii')
                com.send_command(self.comport, config='00000110', motor_byte='00001011', pwm_int=char_pwm)
        else:
            print("Incorrect PWM")

    def motor4_rotate_right(self):
        pwm = self.view.motor4_pwm_scale.get()
        global_timer_status = self.view.global_timer_status.get()
        adc_status = self.view.adc_status.get()
        if adc_status:
            com.send_adc(self.comport, '00001000', '00000001')
            adc_thread = thread.Thread(target=self.model.get_adc_data)
            adc_thread.start()
        if self.model.validate_pwm(pwm):
            if global_timer_status:
                sec = float(self.view.global_timer_entry.get())
                time_limited_thread = thread.Thread(target=self.model.time_limited_motion,
                                                    args=('00000110', '00010011', pwm, sec,))
                time_limited_thread.start()
            elif self.view.motor4_timer_status.get():
                sec = float(self.view.motor4_timer_entry.get())
                time_limited_thread = thread.Thread(target=self.model.time_limited_motion,
                                                    args=('00000110', '00010011', pwm, sec,))
                time_limited_thread.start()
            else:
                char_pwm = bytes(chr(pwm), 'ascii')
                com.send_command(self.comport, config='00000110', motor_byte='00010011', pwm_int=char_pwm)
        else:
            print("Incorrect PWM")

    def motor4_rotate_stop(self):
        com.send_command(self.comport, config='00000010', motor_byte='00000011')

    def motor5_rotate_left(self):
        pwm = self.view.motor1_pwm_scale.get()
        global_timer_status = self.view.global_timer_status.get()
        adc_status = self.view.adc_status.get()
        if adc_status:
            com.send_adc(self.comport, '00001000', '00000001')
            adc_thread = thread.Thread(target=self.model.get_adc_data)
            adc_thread.start()
        if self.model.validate_pwm(pwm):
            if global_timer_status:
                sec = float(self.view.global_timer_entry.get())
                time_limited_thread = thread.Thread(target=self.model.time_limited_motion,
                                                    args=('00000110', '00001100', pwm, sec,))
                time_limited_thread.start()
            elif self.view.motor5_timer_status.get():
                sec = float(self.view.motor5_timer_entry.get())
                time_limited_thread = thread.Thread(target=self.model.time_limited_motion,
                                                    args=('00000110', '00001100', pwm, sec,))
                time_limited_thread.start()
            else:
                char_pwm = bytes(chr(pwm), 'ascii')
                com.send_command(self.comport, config='00000110', motor_byte='00001100', pwm_int=char_pwm)
        else:
            print("Incorrect PWM")

    def motor5_rotate_right(self):
        pwm = self.view.motor1_pwm_scale.get()
        global_timer_status = self.view.global_timer_status.get()
        adc_status = self.view.adc_status.get()
        if adc_status:
            com.send_adc(self.comport, '00001000', '00000001')
            adc_thread = thread.Thread(target=self.model.get_adc_data)
            adc_thread.start()
        if self.model.validate_pwm(pwm):
            if global_timer_status:
                sec = float(self.view.global_timer_entry.get())
                time_limited_thread = thread.Thread(target=self.model.time_limited_motion,
                                                    args=('00000110', '00010100', pwm, sec,))
                time_limited_thread.start()
            elif self.view.motor5_timer_status.get():
                sec = float(self.view.motor5_timer_entry.get())
                time_limited_thread = thread.Thread(target=self.model.time_limited_motion,
                                                    args=('00000110', '00010100', pwm, sec,))
                time_limited_thread.start()
            else:
                char_pwm = bytes(chr(pwm), 'ascii')
                com.send_command(self.comport, config='00000110', motor_byte='00010100', pwm_int=char_pwm)
        else:
            print("Incorrect PWM")

    def motor5_rotate_stop(self):
        com.send_command(self.comport, config='00000010', motor_byte='00000100')


if __name__ == '__main__':
    root = Tk()
    root['bg'] = '#0585e8'
    root.title('Motor Client')
    root.geometry('800x600')
    photo = PhotoImage(file="../Images/cyber_hand.png")
    root.iconphoto(False, photo)
    root.resizable(width=False, height=True)

    application = Controller(root)
    root.mainloop()
