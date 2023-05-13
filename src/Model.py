import comport as com
# import matplotlib.pyplot as plt
from pubsub import pub


class Model:
    def __init__(self):
        self.adc_data = None

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

    def hexstr_to_decint(self, hexstr, reverse_flag=False):
        final_decimal_list = list()
        if reverse_flag:
            target_hexstr = hexstr[::-1]
        else:
            target_hexstr = hexstr
        if len(target_hexstr) % 2 == 0:
            hex_bytes_list = [target_hexstr[i - 1:i + 1] for i in range(1, len(target_hexstr), 2)]
        else:
            hex_bytes_list = [target_hexstr[i - 1:i + 1] for i in range(1, len(target_hexstr), 2)]
            hex_bytes_list.append(target_hexstr[len(target_hexstr) - 1])
        for i in range(0, len(hex_bytes_list)):
            decimal = int(hex_bytes_list[i], 16)
            if decimal != 0:
                final_decimal_list.append(decimal)
            else:
                continue
        return final_decimal_list

    def get_adc_data(self, comport):
        # time.sleep(5.0)
        if comport.isOpen():
            data = comport.read(2000)
            # print(f'Data is {data}, len = {len(data)}, type is {type(data)}')
            data_hexstr = data.hex()
            # print(f'data_str is {data_hexstr}, type is {type(data_hexstr)}')
            decimal_list = self.hexstr_to_decint(data_hexstr, reverse_flag=False)
            # print(*decimal_list)
            self.adc_data = decimal_list
        else:
            print('Model/get_adc_data() - COM Port is closed')

    def send_adc(self, comport, motor_frame):
        m1_adc_status = motor_frame.motor1_adc_status.get()
        m2_adc_status = motor_frame.motor2_adc_status.get()
        m3_adc_status = motor_frame.motor3_adc_status.get()
        m4_adc_status = motor_frame.motor4_adc_status.get()
        m5_adc_status = motor_frame.motor5_adc_status.get()

        adc_decimal = m1_adc_status*2**0 + m2_adc_status*2**1 + m3_adc_status*2**2 + m4_adc_status*2**3 + m5_adc_status*2**4
        com.send_adc(comport, '01000000', adc_decimal)

    # def draw_adc_figure(self, motor_title='Default plot title'):
    #     plt.cla()
    #     data = self.adc_data
    #     for i in range(0, len(data)):
    #         data[i] *= 3.3
    #         data[i] /= 265
    #     x = [i for i in range(0, len(data))]
    #     plt.plot(x, data)
    #     plt.title(motor_title)
    #     plt.xlabel('time')
    #     plt.ylabel('Some Voltage')
    #     plt.grid()
    #     plt.savefig('../Images/AdcFigure.png')
    #     pub.sendMessage('Adc figure updated')

    def time_limited_motion(self, comport, config, motor_byte, pwm, limited_time, delay):
        if self.validate_pwm(pwm):
            time_int = int(limited_time / 0.1)
            delay_int = int(delay / 0.1)
            com.send_command(comport, config, motor_byte=motor_byte, pwm_bytes=pwm, time_bytes=time_int, delay=delay_int)
        else:
            print('Model - Bad pwm')
