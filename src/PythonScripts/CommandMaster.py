from comport import ComportInstance
from logging import getLogger
from decimal import Decimal


def time_limited_motion(comport, config, motor_byte, pwm=0, work_time='0.0', delay='0.0', command_type=None):
    time_int = int(Decimal(work_time) / Decimal('0.1'))
    delay_int = int(Decimal(delay) / Decimal('0.1'))
    if isinstance(comport, ComportInstance):
        byte_data = comport.send_com(config=config, motor_byte=motor_byte, pwm_byte=pwm, time_int=time_int,
                                     delay=delay_int, command_type=command_type)
    else:
        print(f"Model/time_limited_motion - given comport is not instance of ComportInstance: {type(comport)}")
        byte_data = [00, 00, 00, 00, 00]
    return byte_data


class CommandMaster:
    def __init__(self):
        self.logger = getLogger(__name__)
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

    def __add_command_to_upper_list(self, command):
        appended_str = " ".join(format(x, '02x') for x in command)
        self.upper_commands_list.append(appended_str)

    def __add_command_to_lower_list(self, command):
        appended_str = " ".join(format(x, '02x') for x in command)
        self.lower_commands_list.append(appended_str)

    def clear_upper_command_list(self):
        if len(self.upper_commands_list) != 0:
            self.upper_commands_list.clear()
        else:
            self.logger.debug("Upper command list is already empty")

    def clear_lower_command_list(self):
        if len(self.lower_commands_list) != 0:
            self.lower_commands_list.clear()
        else:
            self.logger.debug("Lower command list is already empty")

    def send_command(self, part: str, config: str, motor_byte: str, pwm=0, work_time='0.0', delay='0.0',
                     write_to_script_file=True, command_type=None):
        if part == 'Upper':
            if self.upper_comport is not None:
                byte_command = time_limited_motion(comport=self.upper_comport, config=config, motor_byte=motor_byte,
                                                   pwm=pwm, work_time=work_time, delay=delay, command_type=command_type)
                if write_to_script_file:
                    self.__add_command_to_upper_list(byte_command)
            else:
                self.logger.warning(f"Can't send {command_type} command, Upper comport is None")
        elif part == 'Lower':
            if self.lower_comport is not None:
                byte_command = time_limited_motion(comport=self.lower_comport, config=config, motor_byte=motor_byte,
                                                   pwm=pwm, work_time=work_time, delay=delay, command_type=command_type)
                if write_to_script_file:
                    self.__add_command_to_lower_list(byte_command)
            else:
                self.logger.warning(f"Can't send {command_type} command, Lower comport is None")
        else:
            self.logger.warning(f"Cannot send command (move), unknown part: {part}")

    def stop_command(self, part, config, motor_byte):
        if part == 'Upper':
            if self.upper_comport is not None:
                self.upper_comport.send_com(config, motor_byte)
            else:
                self.logger.warning("Can't send STOP command, Upper comport is None")
        elif part == 'Lower':
            if self.lower_comport is not None:
                self.lower_comport.send_com(config, motor_byte)
            else:
                self.logger.warning("Can't send STOP command, Lower comport is None")
        else:
            self.logger.warning(f"Can't send STOP command, unknown part: {part}")

    def power_command(self, part, config, power_byte):
        if part == 'Upper':
            if self.upper_comport is not None:
                self.upper_comport.send_com(config=config, power_byte=power_byte)
            else:
                self.logger.warning("Can't send POWER command, Upper comport is None")
        elif part == 'Lower':
            if self.lower_comport is not None:
                self.lower_comport.send_com(config=config, power_byte=power_byte)
            else:
                self.logger.warning("Can't send POWER command, Lower comport is None")
        else:
            self.logger.warning(f"Can't send POWER command, unknown part: {part}")

    def send_command_bytes(self, part, data):
        if part == 'Upper':
            if self.upper_comport is not None:
                self.upper_comport.send_bytearray(data)
            else:
                self.logger.warning(f"Can't send FROM BYTES command, Upper comport is None")
        elif part == 'Lower':
            if self.lower_comport is not None:
                self.lower_comport.send_bytearray(data)
            else:
                self.logger.warning(f"Can't send FROM BYTES command, Lower comport is None")
        else:
            self.logger.warning(f"Cannot send command (from bytes), unknown part: {part}")

    # Close and Open COMPORTS after collector thread finish. Like COMPORT ReFresh
    def release_upper_comport_after_thread(self):
        self.upper_comport.close_comport()
        self.upper_comport.open_comport()

    def release_lower_comport_after_thread(self):
        self.lower_comport.close_comport()
        self.lower_comport.open_comport()
