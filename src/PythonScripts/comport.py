import time
import datetime
import serial


def show_available_ports():
    import serial.tools.list_ports
    ports = serial.tools.list_ports.comports()
    port_list = []  # Show all available COM-PORTs
    for port in ports:
        port_list.append(str(port))
        print(str(port))
    return port_list


def convert_string_to_bytes(binary_string):
    decimal = 0
    reverse_string = binary_string[::-1]
    for i in range(0, len(reverse_string)):
        if reverse_string[i] == '1':
            decimal += 2 ** i
        else:
            continue
    return bytes(chr(decimal), 'ascii')


class ComportInstance(serial.Serial):
    def __init__(self, comport_name: str, part_id: str):
        super().__init__()
        self.baudrate = 115200
        self.bytesize = 8
        self.parity = 'N'
        self.stopbits = 1
        self.timeout = 2.0
        self.port = comport_name

        self.open_comport()
        self.command_log_file_path = r"C:/PyCharmProjects/PyQt_withHub/CyberMed/Data/command_log.txt"
        self.part_id = part_id

        # Uses for correct logging
        self.last_time = None
        self.last_delay = None

        # Need to separate sessions for more readability
        self.service_dict = {'service_msg': "Start New Session"}
        self.write_command_log(self.service_dict, 'SERVICE')

    def open_comport(self):
        print(f"comport.py/open_comport - opening port {self.name}")
        if self.is_open:
            print(f'Port - {self.name} is already open')
        else:
            self.open()
            self.reset_input_buffer()
            self.reset_output_buffer()

    def close_comport(self):
        print(f"comport.py/close_comport - closing port {self.name}")
        if self.is_open:
            self.reset_input_buffer()
            self.reset_output_buffer()
            self.close()

    def write_comport(self, data):
        self.write(data)

    def send_com(self, config, power_byte='0', motor_byte='0', pwm_byte=0, time_int=0, delay=0):
        data_bytearray = bytearray()

        readable_command = {'config': None,
                            'power_byte': None,
                            'motor_byte': None,
                            'pwm_byte': None,
                            'time_byte': None,
                            'delay_byte': None,
                            'adc_byte': None}
        command_type = None

        config_stm = convert_string_to_bytes(config)
        power_stm = convert_string_to_bytes(power_byte)
        motor_stm = convert_string_to_bytes(motor_byte)
        char_pwm = bytes(chr(pwm_byte), 'ascii')
        char_time = bytes(chr(time_int), 'ascii')
        char_delay = bytes(chr(delay), 'ascii')

        data_bytearray += config_stm
        readable_command['config'] = config

        if power_byte != '0':
            data_bytearray += power_stm
            readable_command['power_byte'] = power_byte
            command_type = 'POWER'
        else:
            if motor_byte != '0':
                data_bytearray += motor_stm
                readable_command['motor_byte'] = motor_byte
                command_type = 'MOVE'
            if pwm_byte != 0:
                data_bytearray += char_pwm
                readable_command['pwm_byte'] = pwm_byte
            # if time_int != 0:
            #     data_bytearray += char_time
            #     readable_command['time_byte'] = time_int
            data_bytearray += char_time
            readable_command['time_byte'] = time_int
            # if delay > 0:
            #     data_bytearray += char_delay
            #     readable_command.append(delay)
            data_bytearray += char_delay
            readable_command['delay_byte'] = delay

        self.write_comport(data_bytearray)
        print(f"ComportInst - sending command: {data_bytearray}")
        self.write_command_log(readable_command, command_type)
        return data_bytearray

    def send_adc(self, config_byte, adc_int=0):
        bytearray_str = bytearray()
        readable_command = {'config_byte': config_byte,
                            'adc_byte': str(adc_int)}
        command_type = 'ADC'

        config_stm = convert_string_to_bytes(config_byte)
        adc_stm = bytes(chr(adc_int), 'ascii')
        print(f"comport/send_adc - we about to send: config - {config_stm}, adc - {adc_stm}")

        bytearray_str += config_stm
        if adc_stm != 0:
            bytearray_str += adc_stm

        print(f"comport/send_adc - send {bytearray_str}")
        self.write_comport(bytearray_str)
        self.write_command_log(readable_command, command_type)
        # write_comport(config_stm, serial_inst)
        # write_comport(adc_stm, serial_inst)

    def send_bytearray(self, data):
        print(f"comport/send_bytearray - send {data}")
        self.write_comport(data)

    def write_command_log(self, command: dict, command_type: str):
        dt = datetime.datetime.now()
        print(command)
        target_str = ''
        target_str += str(dt) + ': '
        target_str += self.part_id + ': '
        target_str += self.name + ': '
        if command_type == 'POWER':
            target_str += command_type + ': '
            target_str += f'config=({command["config"]}), power_byte=({command["power_byte"]})'
        elif command_type == 'MOVE':
            target_str += command_type + ': '
            target_str += f'config=({command["config"]}), '
            target_str += f'motor=({command["motor_byte"]}), '
            target_str += f'pwm={str(command["pwm_byte"])}, '
            target_str += f'time={str(command["time_byte"] * 0.1)}, '
            target_str += f'delay={str(command["delay_byte"] * 0.1)}'
        elif command_type == 'ADC':
            target_str += command_type + ': '
            target_str += f'config=({command["config_byte"]}), '
            target_str += f'adc_byte=({command["adc_byte"]})'
        elif command_type == 'SERVICE':
            target_str += command_type + ': '
            target_str += command['service_msg']
        else:
            print(f'Command type unknown: {command_type}')
        with open(self.command_log_file_path, 'a') as f:
            if command_type == 'SERVICE':
                f.write(target_str + '\n')
                f.write('\n')
            else:
                f.write(target_str + '\n')
#
#
# def write_comport(data, serial_inst):
#     serial_inst.write(data)
#
#
# def send_adc(serial_inst, config, adc=0):
#     bytearray_str = bytearray()
#
#     config_stm = convert_string_to_bytes(config)
#     adc_stm = bytes(chr(adc), 'ascii')
#     print(f"comport/send_adc - we about to send: config - {config_stm}, adc - {adc_stm}")
#
#     bytearray_str += config_stm
#     if adc_stm != 0:
#         bytearray_str += adc_stm
#
#     print(f"comport/send_adc - send {bytearray_str}")
#     write_comport(bytearray_str, serial_inst)
#     # write_comport(config_stm, serial_inst)
#     # write_comport(adc_stm, serial_inst)
#

# def send_command(serial_inst, config, power_byte='0', motor_byte='0', pwm_bytes=0, time_int=0, delay=0):
#     bytearray_str = bytearray()
#
#     config_stm = convert_string_to_bytes(config)
#     power_stm = convert_string_to_bytes(power_byte)
#     motor_stm = convert_string_to_bytes(motor_byte)
#     char_pwm = bytes(chr(pwm_bytes), 'ascii')
#     char_time = bytes(chr(time_int), 'ascii')
#     char_delay = bytes(chr(delay), 'ascii')
#
#     bytearray_str += config_stm
#     if power_byte != '0':
#         bytearray_str += power_stm
#     if motor_byte != '0':
#         bytearray_str += motor_stm
#     if pwm_bytes != 0:
#         bytearray_str += char_pwm
#     if time_int != 0:
#         bytearray_str += char_time
#     if delay >= 0:
#         bytearray_str += char_delay
#     write_comport(bytearray_str, serial_inst)
#     return bytearray_str


# def open_comport(serial_inst):
#     print(f"comport.py/open_comport - opening port {serial_inst.name}")
#     serial_inst.open()
#     serial_inst.reset_input_buffer()
#     serial_inst.reset_output_buffer()
#
#
# def close_comport(serial_inst):
#     print(f"comport.py/close_comport - closing port {serial_inst.name}")
#     if serial_inst.is_open:
#         serial_inst.reset_input_buffer()
#         serial_inst.reset_output_buffer()
#         serial_inst.close()


def main():
    show_available_ports()


if __name__ == "__main__":
    main()
    inst = ComportInstance('COM6', "Lower")
    inst.send_com(config='00011110', motor_byte='00001010', pwm_byte=100, time_int=10, delay=5)
    inst.send_com(config='00000001', power_byte='00000001')
