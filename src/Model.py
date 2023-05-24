import comport as com
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pubsub import pub
from PlotDataHolder import PlotDataHolder
import threading as thread


class Model:
    def __init__(self):
        self.adc_data = None
        self.holder = None

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
                        if 0 <= int(pwm) <= 100:
                            return True
                        else:
                            return False  # PWM needs to be an integer between 0 and 50
                else:
                    return False  # PWM must be 1, 2 digits long
        else:
            return False  # PWM neither a number nor a string

    def convert_delay(self, delay):
        if len(delay) != 0:
            return float(delay)
        else:
            return 0.0

    def hexstr_to_dec_int(self, hexstr, reverse_flag=False):
        target_hexstr = hexstr[::-1] if reverse_flag else hexstr
        hex_bytes_list = [target_hexstr[i - 1:i + 1] for i in range(1, len(target_hexstr) + 1, 2)]
        final_decimal_list = [int(hex_byte, 16) for hex_byte in hex_bytes_list if int(hex_byte, 16) != 0]
        return final_decimal_list[-1] if final_decimal_list else 0

    def send_adc(self, comport, motor_frame):
        m1_adc = motor_frame.motor1_adc_status.get()
        m2_adc = motor_frame.motor2_adc_status.get()
        m3_adc = motor_frame.motor3_adc_status.get()
        m4_adc = motor_frame.motor4_adc_status.get()
        m5_adc = motor_frame.motor5_adc_status.get()

        adc_number = int(m1_adc + m2_adc + m3_adc + m4_adc + m5_adc)

        if adc_number == 0:
            print('Model/send_adc() - ADC is 0')
        else:
            adc_decimal = m1_adc*2**0 + m2_adc*2**1 + m3_adc*2**2 + m4_adc*2**3 + m5_adc*2**4
            com.send_adc(comport, '00100000', adc_decimal)
            self.holder = PlotDataHolder(adc_number)
            print(f'We just sent ADC info from {motor_frame.who_are_you()}')
            self.holder.start_animate(comport)

    def draw_adc_figure(self, motor_title='Default plot title'):
        plt.cla()
        data = self.adc_data
        for i in range(0, len(data)):
            data[i] *= 3.3
            data[i] /= 265
        x = [i for i in range(0, len(data))]
        plt.plot(x, data)
        plt.title(motor_title)
        plt.xlabel('time')
        plt.ylabel('Some Voltage')
        plt.grid()
        plt.savefig('../Images/AdcFigure.png')
        pub.sendMessage('Adc figure updated')

    def time_limited_motion(self, comport, config, motor_byte, pwm, limited_time, delay):
        if self.validate_pwm(pwm):
            time_int = int(limited_time / 0.1)
            delay_int = int(delay / 0.1)
            com.send_command(comport, config, motor_byte=motor_byte, pwm_bytes=pwm, time_bytes=time_int, delay=delay_int)
        else:
            print('Model - Bad pwm')
