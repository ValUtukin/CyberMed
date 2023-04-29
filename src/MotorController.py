from Model import Model
import comport as com
import threading as thread


class MotorController:
    def __init__(self, comport, identifier):
        self.comport = comport
        self.identifier = identifier
        self.model = Model(self.comport)

    def who_are_you(self):
        return f'{self.identifier}MotorController'

    def start_adc_thread(self):
        com.send_adc(self.comport, '00001000', '00000001')
        adc_thread = thread.Thread(target=self.model.get_adc_data)
        adc_thread.start()

    def start_limited_motion_thread(self, bytes_tuple, pwm, time):
        time_limited_thread = thread.Thread(target=self.model.time_limited_motion, args=(bytes_tuple[0], bytes_tuple[1],
                                                                                         pwm, time))
        time_limited_thread.start()

    def motor1_rotate_left(self, adc_flag=False, pwm=0, time_limited=0.0):
        if adc_flag:
            self.start_adc_thread()
        if self.model.validate_pwm(pwm):
            if time_limited > 0.0:
                self.start_limited_motion_thread(('00000110', '00001000',), pwm, time_limited)
            else:
                char_pwm = bytes(chr(pwm), 'ascii')
                com.send_command(self.comport, config='00000110', motor_byte='00001000', pwm_int=char_pwm)
        else:
            print("Incorrect PWM")

    def motor1_rotate_right(self, adc_flag=False, pwm=0, time_limited=0.0):
        if adc_flag:
            self.start_adc_thread()
        if self.model.validate_pwm(pwm):
            if time_limited > 0.0:
                self.start_limited_motion_thread(('00000110', '00010000',), pwm, time_limited)
            else:
                char_pwm = bytes(chr(pwm), 'ascii')
                com.send_command(self.comport, config='00000110', motor_byte='00010000', pwm_int=char_pwm)
        else:
            print("Incorrect PWM")

    def motor1_rotate_stop(self):
        com.send_command(self.comport, config='00000010', motor_byte='00000000')

    def motor2_rotate_left(self, adc_flag=False, pwm=0, time_limited=0.0):
        if adc_flag:
            self.start_adc_thread()
        if self.model.validate_pwm(pwm):
            if time_limited > 0.0:
                self.start_limited_motion_thread(('00000110', '00001001',), pwm, time_limited)
            else:
                char_pwm = bytes(chr(pwm), 'ascii')
                com.send_command(self.comport, config='00000110', motor_byte='00001001', pwm_int=char_pwm)
        else:
            print("Incorrect PWM")

    def motor2_rotate_right(self, adc_flag=False, pwm=0, time_limited=0.0):
        if adc_flag:
            self.start_adc_thread()
        if self.model.validate_pwm(pwm):
            if time_limited > 0.0:
                self.start_limited_motion_thread(('00000110', '00010001',), pwm, time_limited)
            else:
                char_pwm = bytes(chr(pwm), 'ascii')
                com.send_command(self.comport, config='00000110', motor_byte='00010001', pwm_int=char_pwm)
        else:
            print("Incorrect PWM")

    def motor2_rotate_stop(self):
        com.send_command(self.comport, config='00000010', motor_byte='00000001')

    def motor3_rotate_left(self, adc_flag=False, pwm=0, time_limited=0.0):
        if adc_flag:
            self.start_adc_thread()
        if self.model.validate_pwm(pwm):
            if time_limited > 0.0:
                self.start_limited_motion_thread(('00000110', '00001010',), pwm, time_limited)
            else:
                char_pwm = bytes(chr(pwm), 'ascii')
                com.send_command(self.comport, config='00000110', motor_byte='00001010', pwm_int=char_pwm)
        else:
            print("Incorrect PWM")

    def motor3_rotate_right(self, adc_flag=False, pwm=0, time_limited=0.0):
        if adc_flag:
            self.start_adc_thread()
        if self.model.validate_pwm(pwm):
            if time_limited > 0.0:
                self.start_limited_motion_thread(('00000110', '00010010',), pwm, time_limited)
            else:
                char_pwm = bytes(chr(pwm), 'ascii')
                com.send_command(self.comport, config='00000110', motor_byte='00010010', pwm_int=char_pwm)
        else:
            print("Incorrect PWM")

    def motor3_rotate_stop(self):
        com.send_command(self.comport, config='00000010', motor_byte='00000010')

    def motor4_rotate_left(self, adc_flag=False, pwm=0, time_limited=0.0):
        if adc_flag:
            self.start_adc_thread()
        if self.model.validate_pwm(pwm):
            if time_limited > 0.0:
                self.start_limited_motion_thread(('00000110', '00001011',), pwm, time_limited)
            else:
                char_pwm = bytes(chr(pwm), 'ascii')
                com.send_command(self.comport, config='00000110', motor_byte='00001011', pwm_int=char_pwm)
        else:
            print("Incorrect PWM")

    def motor4_rotate_right(self, adc_flag=False, pwm=0, time_limited=0.0):
        if adc_flag:
            self.start_adc_thread()
        if self.model.validate_pwm(pwm):
            if time_limited > 0.0:
                self.start_limited_motion_thread(('00000110', '00010011',), pwm, time_limited)
            else:
                char_pwm = bytes(chr(pwm), 'ascii')
                com.send_command(self.comport, config='00000110', motor_byte='00010011', pwm_int=char_pwm)
        else:
            print("Incorrect PWM")

    def motor4_rotate_stop(self):
        com.send_command(self.comport, config='00000010', motor_byte='00000011')

    def motor5_rotate_left(self, adc_flag=False, pwm=0, time_limited=0.0):
        if adc_flag:
            self.start_adc_thread()
        if self.model.validate_pwm(pwm):
            if time_limited > 0.0:
                self.start_limited_motion_thread(('00000110', '00001100',), pwm, time_limited)
            else:
                char_pwm = bytes(chr(pwm), 'ascii')
                com.send_command(self.comport, config='00000110', motor_byte='00001100', pwm_int=char_pwm)
        else:
            print("Incorrect PWM")

    def motor5_rotate_right(self, adc_flag=False, pwm=0, time_limited=0.0):
        if adc_flag:
            self.start_adc_thread()
        if self.model.validate_pwm(pwm):
            if time_limited > 0.0:
                self.start_limited_motion_thread(('00000110', '00010100',), pwm, time_limited)
            else:
                char_pwm = bytes(chr(pwm), 'ascii')
                com.send_command(self.comport, config='00000110', motor_byte='00010100', pwm_int=char_pwm)
        else:
            print("Incorrect PWM")

    def motor5_rotate_stop(self):
        com.send_command(self.comport, config='00000010', motor_byte='00000100')