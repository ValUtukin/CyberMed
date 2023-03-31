import comport as com
import time


class Model:
    def __init__(self, serial_inst):
        self.comport = serial_inst

    def validate_pwm(self, pwm):
        pwm_type = type(pwm)
        if pwm_type == int:
            return True
        elif pwm_type == str:
            if pwm == '':
                return False
            else:
                if 1 <= len(pwm) <= 3:
                    for i in range(0, len(pwm)):
                        if pwm[i] in '0123456789':
                            continue
                        else:
                            return False  # PWM must be a number
                    else:
                        if 0 <= int(pwm) <= 50:
                            return True
                        else:
                            return False  # PWM needs to be an integer between 0 and 100
                else:
                    return False  # PWM must be 1, 2 or 3 digits long
        else:
            return False  # PWM neither a number nor a string

    def motor1_save_adc_data(self):
        if self.comport.isOpen():
            data = self.comport.read(1)
            print(f'Data is {data}, len = {len(data)}, type is {type(data)}')
        else:
            self.comport.open()
            data = self.comport.read(1)
            print(f'Data is {data}, len = {len(data)}, type is {type(data)}')
            self.comport.close()

    def time_limited_motion(self, config, motor_byte, pwm, limited_lime):
        if self.validate_pwm(pwm):
            char_pwm = bytes(chr(pwm), 'ascii')
            com.send_command(self.comport, config, motor_byte=motor_byte, pwm_int=char_pwm)
            time.sleep(limited_lime)  # Wait until motor rotate for "limited_time" sec and then stop it
            motor_number_str = motor_byte[5::]
            motor_stop_byte = '00000' + motor_number_str
            com.send_command(self.comport, config='00000010', motor_byte=motor_stop_byte)
        else:
            print('Model - Bad pwm')
