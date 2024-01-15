import serial


def ini(comport_name='COM2'):
    serial_inst = serial.Serial()
    serial_inst.baudrate = 115200
    serial_inst.bytesize = 8
    serial_inst.parity = 'N'
    serial_inst.stopbits = 1
    serial_inst.timeout = 2.0
    serial_inst.port = comport_name
    open_comport(serial_inst)
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
                return packet.decode('utf-8')
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


def send_adc(serial_inst, config, adc=0):
    bytearray_str = bytearray()

    config_stm = convert_string_to_bytes(config)
    adc_stm = bytes(chr(adc), 'ascii')
    print(f"comport/send_adc - we about to send: config - {config_stm}, adc - {adc_stm}")

    bytearray_str += config_stm
    if adc_stm != 0:
        bytearray_str += adc_stm

    print(f"comport/send_adc - send {bytearray_str}")
    write_comport(bytearray_str, serial_inst)
    # write_comport(config_stm, serial_inst)
    # write_comport(adc_stm, serial_inst)


def send_command(serial_inst, config, power_byte='0', motor_byte='0', pwm_bytes=0, time_int=0, delay=0):
    bytearray_str = bytearray()

    config_stm = convert_string_to_bytes(config)
    power_stm = convert_string_to_bytes(power_byte)
    motor_stm = convert_string_to_bytes(motor_byte)
    char_pwm = bytes(chr(pwm_bytes), 'ascii')
    char_time = bytes(chr(time_int), 'ascii')
    char_delay = bytes(chr(delay), 'ascii')

    bytearray_str += config_stm
    if power_byte != '0':
        bytearray_str += power_stm
    if motor_byte != '0':
        bytearray_str += motor_stm
    if pwm_bytes != 0:
        bytearray_str += char_pwm
    if time_int != 0:
        bytearray_str += char_time
    if delay != 0:
        bytearray_str += char_delay
    print(f"comport/send_command - send {bytearray_str}")
    write_comport(bytearray_str, serial_inst)
    return bytearray_str


def open_comport(serial_inst):
    serial_inst.open()
    serial_inst.reset_input_buffer()
    serial_inst.reset_output_buffer()


def close_comport(serial_inst):
    if serial_inst.is_open:
        serial_inst.reset_input_buffer()
        serial_inst.reset_output_buffer()
        serial_inst.close()


def main():
    show_available_ports()


if __name__ == "__main__":
    main()
