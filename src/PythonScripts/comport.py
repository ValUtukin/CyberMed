import datetime
import serial
from logging import getLogger
from decimal import Decimal


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


def convert_decimal_int_to_binary_str(data: int) -> str:
    total = ""
    while data > 0:
        if data % 2 == 0:
            total += '0'
            data /= 2
        else:
            total += '1'
            data //= 2
    target_line = total[::-1]

    # return string representation of given int into byte e.g. 00110101
    return target_line.zfill(8)


class ComportInstance(serial.Serial):
    def __init__(self, comport_name, part_id):
        super().__init__()
        self.baudrate = 115200
        self.bytesize = 8
        self.parity = 'N'
        self.stopbits = 1
        self.timeout = 2.0
        self.port = comport_name  # Actual Windows comport name (COM1, COM2, etc.) !Obligatory to confire comport!
        self.part_id = part_id  # Uses to identify Upper and Lower port in command log file

        # Uses for correct logging
        self.last_time = None
        self.last_delay = None

        self.logger = getLogger(f"{self.part_id} {__name__}")
        self.command_log_file_path = None
        self.open_comport()

    def open_comport(self):
        self.logger.info(f"Open port: {self.name}")
        if self.is_open:
            self.logger.warning(f"Port - {self.name} is already open")
        else:
            self.open()
            self.reset_input_buffer()
            self.reset_output_buffer()

    def close_comport(self):
        self.logger.info(f"Close port: {self.name}")
        if self.is_open:
            self.reset_input_buffer()
            self.reset_output_buffer()
            self.close()

    def set_command_log_file_path(self, file_path):
        self.command_log_file_path = file_path
        self.write_command_log({'service_msg': "Start New Session"}, 'SERVICE')

    def write_comport(self, data):
        self.write(data)

    def send_com(self, config, power_byte='0', motor_byte='0', pwm_byte=0, time_int=0, delay=0, command_type=None):
        data_bytearray = bytearray()
        readable_command = {'config': None,
                            'power_byte': None,
                            'motor_byte': None,
                            'pwm_byte': None,
                            'time_byte': None,
                            'delay_byte': None,
                            'adc_byte': None}

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
                if not command_type:
                    '''Motor byte not empty and command_type = None (not specified). Probably it's MOVE command.
                       If command_type specified (not None), then give that type to command logger
                       For example: TENSE, RELEASE etc.'''
                    command_type = 'MOVE'
                data_bytearray += motor_stm
                readable_command['motor_byte'] = motor_byte

            if pwm_byte != 0:
                data_bytearray += char_pwm
                readable_command['pwm_byte'] = pwm_byte

            data_bytearray += char_time
            readable_command['time_byte'] = time_int

            data_bytearray += char_delay
            readable_command['delay_byte'] = delay

        self.write_comport(data_bytearray)

        # Logging
        self.write_command_log(readable_command, command_type)
        return data_bytearray

    def send_adc(self, config_byte, adc_int=0):
        bytearray_str = bytearray()
        adc_byte = convert_decimal_int_to_binary_str(adc_int)
        readable_command = {'config_byte': config_byte,
                            'adc_byte': adc_byte}
        command_type = 'ADC'

        config_stm = convert_string_to_bytes(config_byte)
        adc_stm = bytes(chr(adc_int), 'ascii')

        bytearray_str += config_stm
        if adc_stm != 0:
            bytearray_str += adc_stm

        self.write_comport(bytearray_str)

        # Logging
        self.logger.debug(f"Send ADC command: {bytearray_str} to {self.name}")
        self.write_command_log(readable_command, command_type)

    def send_bytearray(self, data):
        self.logger.debug(f"Send command (FROM BYTES): {data} to {self.name}")
        command_dict = {'config': None,
                        'power_byte': None,
                        'motor_byte': None,
                        'pwm_byte': None,
                        'time_byte': None,
                        'delay_byte': None,
                        'adc_byte': None
                        }
        if len(data) == 5:
            '''We need string representation of bytes for config_byte and motor_byte.
               So call convert_decimal_int_to_binary_str'''
            command_dict['config'] = convert_decimal_int_to_binary_str(data[0])
            command_dict['motor_byte'] = convert_decimal_int_to_binary_str(data[1])
            command_dict['pwm_byte'] = data[2]
            command_dict['time_byte'] = data[3]
            command_dict['delay_byte'] = data[4]
            self.write_command_log(command=command_dict, command_type='MOVE')
        else:
            self.logger.debug(f"Command from bytes less than 5: {data}, len = {len(data)}")
        self.write_comport(data)

    def write_command_log(self, command: dict, command_type: str):
        dt = datetime.datetime.now()
        target_str = ''
        target_str += str(dt) + ': '
        target_str += self.part_id + ': '
        target_str += self.name + ': '
        if command_type == 'POWER':
            target_str += command_type + ': '
            target_str += f'config=({command["config"]}), power_byte=({command["power_byte"]})'
        elif command_type == 'MOVE' or command_type == 'TENSE' or command_type == 'RELEASE':
            decimal_coefficient = Decimal('0.1')  # All Decimal stuff need to avoid results like: 0.3000000000000004
            target_str += command_type + ': '
            target_str += f'config=({command["config"]}), '
            target_str += f'motor=({command["motor_byte"]}), '
            target_str += f'pwm={str(command["pwm_byte"])}, '
            target_str += f'time={str(command["time_byte"] * decimal_coefficient)}, '
            target_str += f'delay={str(command["delay_byte"] * decimal_coefficient)}'
        elif command_type == 'ADC':
            target_str += command_type + ': '
            target_str += f'config=({command["config_byte"]}), '
            target_str += f'adc_byte=({command["adc_byte"]})'
        elif command_type == 'SERVICE':
            target_str += command_type + ': '
            target_str += command['service_msg']
        else:
            self.logger.warning(f"Command type unknown: {command_type}")

        # Write command to command_log file
        with open(self.command_log_file_path, 'a') as f:
            f.write(target_str + '\n')

    def __del__(self):
        self.logger.info(f"Disconnect port: {self.port}")
