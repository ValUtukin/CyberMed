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
    def __init__(self):
        self.upper_comport = None
        self.lower_comport = None
        self.upper_commands_list = list()
        self.lower_commands_list = list()

    def set_upper_comport(self, port):
        self.upper_comport = port

    def set_lower_comport(self, port):
        self.lower_comport = port

    def upper_send_adc(self, adc_decimal):
        com.send_adc(self.upper_comport, '00100000', adc_decimal)

    def lower_send_adc(self, adc_decimal):
        com.send_adc(self.lower_comport, '00100000', adc_decimal)

    def get_upper_commands_list(self):
        return self.upper_commands_list

    def get_lower_commands_list(self):
        return self.lower_commands_list

    def add_command_to_upper_list(self, command):
        appended_str = " ".join(format(x, '02x') for x in command)
        self.upper_commands_list.append(appended_str)
        print(f'Model/add_command_to_upper_list - appending command to upper list: {appended_str}')

    def add_command_to_lower_list(self, command):
        appended_str = " ".join(format(x, '02x') for x in command)
        self.lower_commands_list.append(appended_str)
        print(f'Model/add_command_to_lower_list - appending command to lower list: {appended_str}')

    def send_command(self, part, config, motor_byte, pwm, limited_time, delay):
        if part == 'Upper':
            byte_command = time_limited_motion(self.upper_comport, config, motor_byte, pwm, limited_time, delay)
            self.add_command_to_upper_list(byte_command)
        elif part == 'Lower':
            byte_command = time_limited_motion(self.lower_comport, config, motor_byte, pwm, limited_time, delay)
            self.add_command_to_lower_list(byte_command)
        else:
            print(f'Model/send_command - unknown part: {part}')

    def stop_command(self, part, config, motor_byte):
        if part == 'Upper':
            com.send_command(self.upper_comport, config, motor_byte)
        elif part == 'Lower':
            com.send_command(self.lower_comport, config, motor_byte)
        else:
            print(f'Model/stop_command - unknown part: {part}')

    def power_command(self, part, config, power_byte):
        print(f'Model/power_command - got power command: {part}, {config}, {power_byte}')
        if part == 'Upper':
            com.send_command(self.upper_comport, config, power_byte)
        elif part == 'Lower':
            com.send_command(self.lower_comport, config, power_byte)
        else:
            print(f'Model/stop_command - unknown part: {part}')

    def send_command_bytes(self, part, data):
        if part == 'Upper':
            com.send_bytearray(self.upper_comport, data)
        elif part == 'Lower':
            com.send_bytearray(self.lower_comport, data)
        else:
            print(f'Model/send_command_bytes - unknown part: {part}')


if __name__ == '__main__':
    upper_com = com.ini('COM2')
    lower_com = com.ini('COM3')
    model = Model()
    model.set_upper_comport(upper_com)
    model.set_lower_comport(lower_com)
