import serial
import time


def ini(comport_name='COM2'):
    serial_inst = serial.Serial()
    serial_inst.baudrate = 115200
    serial_inst.timeout = 5.0
    serial_inst.bytesize = 8
    serial_inst.parity = 'N'
    serial_inst.stopbits = 1
    serial_inst.port = comport_name
    serial_inst.open()
    return serial_inst


def show_available_ports():
    import serial.tools.list_ports
    ports = serial.tools.list_ports.comports()
    port_list = []  # Show all available COM-PORTs
    for port in ports:
        port_list.append(str(port))
        print(str(port))
    return port_list


def write_comport(data, serial_inst):
    serial_inst.write(data)


def read_com_port(serial_inst):
    while True:
        if serial_inst.inWaiting():
            packet = serial_inst.read(3)
            if packet is None:
                return "No data"
            else:
                return packet.decode('ascii')
        else:
            pass


def convert_string_to_bytes(binary_string):
    decimal = 0
    reverse_string = binary_string[::-1]
    for i in range(0, len(reverse_string)):
        if reverse_string[i] == '1':
            decimal += 2 ** i
        else:
            continue
    return bytes(chr(decimal), 'ascii')


def send_adc(serial_inst, config, adc='0'):
    config_stm = convert_string_to_bytes(config)
    adc_stm = convert_string_to_bytes(adc)
    write_comport(config_stm, serial_inst)
    write_comport(adc_stm, serial_inst)


def send_command(serial_inst, config, power_byte='0', motor_byte='0', pwm_int=0):
    config_stm = convert_string_to_bytes(config)
    power_stm = convert_string_to_bytes(power_byte)
    motor_stm = convert_string_to_bytes(motor_byte)

    write_comport(config_stm, serial_inst)
    time.sleep(0.0005)
    if power_byte != '0':
        write_comport(power_stm, serial_inst)
    if motor_byte != '0':
        write_comport(motor_stm, serial_inst)
    if pwm_int != 0:
        write_comport(pwm_int, serial_inst)


def main():
    show_available_ports()


if __name__ == "__main__":
    main()
