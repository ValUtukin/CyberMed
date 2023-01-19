import serial.tools.list_ports
import time


ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()

portList = []  # Show all available COM-PORTs
for port in ports:
    portList.append(str(port))
    print(str(port))

serialInst.baudrate = 9600
serialInst.bytesize = 8
serialInst.parity = 'N'
serialInst.stopbits = 1
serialInst.port = 'COM2'
res = serialInst.open()

while True:
    if serialInst.inWaiting():
        print('Listening...')
        time.sleep(2.0)
        print('Reading data...')
        packet = serialInst.read()
        if packet is None:
            print('No data')
        else:
            print(f'packet data type is {type(packet)}')
            data = packet.decode('ascii')
            ba = bytearray(packet)
            print(f'Usind ascii table convert data to bytearray and show it as decimal: {ba}')
            print(f'packet data is {data}')
            print(f'packet data type if {type(data)}')
        packet = None
