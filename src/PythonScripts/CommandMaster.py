from comport import ComportInstance


def time_limited_motion(comport, config, motor_byte, pwm=0, work_time=0, delay=0):
    print(f"time_limited_motion: time = {work_time}, delay = {delay}")
    time_int = int(work_time / 0.1)
    delay_int = int(delay / 0.1)
    print(f"time_limited_motion: time = {time_int}, delay = {delay_int}")
    if isinstance(comport, ComportInstance):
        print(f'Model/time_limited_motion - send: (conf={config}, motor={motor_byte}, {pwm}, {time_int}, {delay_int})')
        byte_data = comport.send_com(config=config, motor_byte=motor_byte, pwm_byte=pwm, time_int=time_int,
                                     delay=delay_int)
    else:
        print(f"Model/time_limited_motion - given comport is not instance of ComportInstance: {type(comport)}")
        byte_data = [00, 00, 00, 00, 00]
    return byte_data


class CommandMaster:
    def __init__(self):
        self.upper_comport = None
        self.lower_comport = None
        self.upper_commands_list = list()
        self.lower_commands_list = list()

    def set_upper_comport(self, port: ComportInstance):
        self.upper_comport = port

    def set_lower_comport(self, port: ComportInstance):
        self.lower_comport = port

    def upper_send_adc(self, adc_decimal):
        self.upper_comport.send_adc(config_byte='00100000', adc_int=adc_decimal)

    def lower_send_adc(self, adc_decimal):
        self.lower_comport.send_adc(config_byte='00100000', adc_int=adc_decimal)

    def get_upper_commands_list(self):
        return self.upper_commands_list

    def get_lower_commands_list(self):
        return self.lower_commands_list

    def add_command_to_upper_list(self, command):
        appended_str = " ".join(format(x, '02x') for x in command)
        self.upper_commands_list.append(appended_str)

    def add_command_to_lower_list(self, command):
        appended_str = " ".join(format(x, '02x') for x in command)
        self.lower_commands_list.append(appended_str)

    def clear_upper_command_list(self):
        self.upper_commands_list.clear()

    def clear_lower_command_list(self):
        self.lower_commands_list.clear()

    def send_command(self, part, config, motor_byte, pwm=0, work_time=0, delay=0):
        if part == 'Upper':
            byte_command = time_limited_motion(comport=self.upper_comport, config=config, motor_byte=motor_byte,
                                               pwm=pwm, work_time=work_time, delay=delay)
            self.add_command_to_upper_list(byte_command)
        elif part == 'Lower':
            byte_command = time_limited_motion(comport=self.lower_comport, config=config, motor_byte=motor_byte,
                                               pwm=pwm, work_time=work_time, delay=delay)
            self.add_command_to_lower_list(byte_command)
        else:
            print(f'Model/send_command - unknown part: {part}')

    def stop_command(self, part, config, motor_byte):
        if part == 'Upper':
            self.upper_comport.send_com(config, motor_byte)
        elif part == 'Lower':
            self.lower_comport.send_com(config, motor_byte)
        else:
            print(f'Model/stop_command - unknown part: {part}')

    def power_command(self, part, config, power_byte):
        print(f'Model/power_command - got power command: {part}, {config}, {power_byte}')
        if part == 'Upper':
            self.upper_comport.send_com(config=config, power_byte=power_byte)
        elif part == 'Lower':
            self.lower_comport.send_com(config=config, power_byte=power_byte)
        else:
            print(f'Model/stop_command - unknown part: {part}')

    def send_command_bytes(self, part, data):
        if part == 'Upper':
            self.upper_comport.send_bytearray(data)
        elif part == 'Lower':
            self.lower_comport.send_bytearray(data)
        else:
            print(f'Model/send_command_bytes - unknown part: {part}')

    # Close and Open COMPORTS after collector thread finish. Like COMPORT ReFresh
    def release_upper_comport_after_thread(self):
        # com.close_comport(self.upper_comport)
        # com.open_comport(self.upper_comport)
        self.upper_comport.close_comport()
        self.upper_comport.open_comport()

    def release_lower_comport_after_thread(self):
        # com.close_comport(self.lower_comport)
        # com.open_comport(self.lower_comport)
        self.lower_comport.close_comport()
        self.lower_comport.open_comport()


if __name__ == '__main__':
    pass
