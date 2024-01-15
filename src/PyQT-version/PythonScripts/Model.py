import comport as com


def time_limited_motion(comport, config, motor_byte, pwm, limited_time, delay):
    time_int = int(limited_time / 0.1)
    delay_int = int(delay / 0.1)
    print(f'Model/time_limited_motion - we send: (conf={config}, motor={motor_byte}, {pwm}, {time_int}, {delay_int})')
    byte_data = com.send_command(comport, config, motor_byte=motor_byte, pwm_bytes=pwm, time_int=time_int,
                                 delay=delay_int)
    print(f'Model get this data: {byte_data} from comport. Type: {type(byte_data)}')
    return byte_data


class Model:
    def __init__(self, upper_comport, lower_comport):
        self.upper_comport = upper_comport
        self.lower_comport = lower_comport
        self.__move_script_default_text = "Move script is now empty"

    def get_move_script_default_text(self):
        return self.__move_script_default_text

    def upper_send_adc(self, adc_decimal):
        com.send_adc(self.upper_comport, '00100000', adc_decimal)

    def lower_send_adc(self, adc_decimal):
        com.send_adc(self.lower_comport, '00100000', adc_decimal)


if __name__ == '__main__':
    upper_com = com.ini('COM2')
    lower_com = com.ini('COM3')
    model = Model(upper_com, lower_com)
