import serial
import time


def ini():
    serial_inst = serial.Serial()
    serial_inst.baudrate = 115200
    serial_inst.bytesize = 8
    serial_inst.parity = 'N'
    serial_inst.stopbits = 1
    serial_inst.port = 'COM8'
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
    # time.sleep(0.1)
    serial_inst.write(data)
    # print(f'we sent {data}')


def read_com_port(serial_inst):
    while True:
        if serial_inst.inWaiting():
            packet = serial_inst.read()
            if packet is None:
                return "No data"
            else:
                return packet.decode('utf-8')


def convert_string_to_bytes(binary_string):
    decimal = 0
    reverse_string = binary_string[::-1]
    for i in range(0, len(reverse_string)):
        if reverse_string[i] == '1':
            decimal += 2 ** i
        else:
            continue
    stm_key_char = chr(decimal)
    return bytes(stm_key_char, 'ascii')


def main(config, pwm_int):
    serial_instance = ini()
    data_stm = convert_string_to_bytes(config)
    write_comport(data_stm, serial_instance)
    time.sleep(0.0005)
    write_comport(pwm_int, serial_instance)


if __name__ == "__main__":
    main('01100011', 20)
