from PyQt5.QtCore import QObject, pyqtSignal
import comport as com
import time


class DataCollector(QObject):
    finished = pyqtSignal()  # It doesn't work inside __init__ func. So it's placed outside (don't know why)
    segment_received = pyqtSignal()

    def __init__(self, set_num, args=None, comport=None):
        super().__init__()
        self.data_set_holder = dict()
        self.initial_delay = None
        if not args:
            self.initial_byte_count = None
        else:
            self.initial_byte_count = args
        if set_num:
            if set_num > 0:
                for i in range(0, set_num):
                    self.data_set_holder[f'array{i + 1}'] = list()
                self.holder_len = set_num
                print(f'DataCollector/__init__ - Current len is {self.holder_len}')
            else:
                print(f'DataCollector.py/__init__ - set_num is invalid: {set_num}. Must be greater than 0')
                self.holder_len = 0
        else:
            print(f'DataCollector/__init__ - got 0 as parameter. Current holder_len is {len(self.data_set_holder)}')
            self.holder_len = 0
        if not comport:  # Comport is None
            self.comport = None
        else:
            self.comport = comport

    def set_comport(self, serial_inst):
        self.comport = serial_inst

    def get_comport(self):
        return self.comport

    def add_set(self, number):
        if number > 0:
            self.data_set_holder[f'array{number}'] = list()
        else:
            print(f"DataCollector/add_set - number must be greater than 0. Got {number} instead")

    def get_set(self, number=0):
        for arr in self.data_set_holder:
            if str(number) == arr[-1]:
                return self.data_set_holder[f'array{number}']

    def set_delay_for_collecting(self, delay):
        self.initial_delay = delay

    def get_delay_for_collecting(self):
        return self.initial_delay

    def set_byte_count(self, byte_count):
        self.initial_byte_count = byte_count

    def get_byte_count(self):
        return self.initial_byte_count

    def get_data_sets(self):
        return self.data_set_holder, len(self.data_set_holder)

    def set_number_of_sets(self, number):
        if self.holder_len == number:
            print(f"Current holder len is already = {number}")
        else:
            if number > 0:
                self.data_set_holder.clear()
                for i in range(0, number):
                    self.data_set_holder[f'array{i + 1}'] = list()
                self.holder_len = number
                print(f'DataCollector/set_number_of_sets - Current len is {self.holder_len}')
            else:
                print(f'DataCollector/set_number_of_sets - num is invalid: {number}. Must be greater than 0')

    def add_value_to_set(self, set_name, value):
        self.data_set_holder[set_name].append(value)

    def clear_set(self, set_name):
        set_to_clear = self.data_set_holder[set_name]
        set_to_clear.clear()

    def start_collecting(self, byte_count=0):
        print(f"DataCollector/start_collecting - Delay before collecting: {self.initial_delay}")
        time.sleep(self.initial_delay)

        if not byte_count:
            print(f'DataCollector/start_collecting - got no params, byte_count is {byte_count}. Read initial number of bytes.')
            if not self.initial_byte_count:
                print(f'DataCollector/start_collecting - initial_byte_count also None: self.initial_byte_count is {self.initial_byte_count}')
            else:
                print(f'DataCollector/start_collecting - initial_byte_count not None: {self.initial_byte_count}')
                if self.holder_len:
                    print(f'DataCollector/start_collecting - start to read from {self.comport.name}, bytes to read: {self.initial_byte_count}')
                    for i in range(0, self.initial_byte_count, 25):
                        data = self.comport.read(25)
                        if len(data) == 0:
                            self.add_value_to_set('array1', 0)
                        else:
                            for j in range(0, len(data)):
                                print(f"{j + 1}) {data[j]}, type {type(data[j])}")
                                new_data = data[j] * 3.3 / 4096
                                self.add_value_to_set('array1', new_data)
                        self.segment_received.emit()
                        print("DataCollector/start_collecting - start sleeping...")
                        time.sleep(0.5)
                    print(f'Just finished receiving data. Num of bytes {self.initial_byte_count}')
                    com.close_comport(self.comport)
                else:
                    print(f"DataCollector.start_collecting - data_set_holder's len is 0")
        else:
            if self.holder_len:
                for i in range(0, byte_count):
                    data = int(self.comport.read().hex())
                    self.add_value_to_set('array1', data)
            else:
                print(f"DataCollector.start_collecting - data_set_holder's len is 0")
        self.finished.emit()

    def collect_infinitely(self):
        while True:
            data = int(self.comport.read().hex(), 16)
            self.add_value_to_set("array1", data)


if __name__ == '__main__':
    serial_ins = com.ini('COM2')
    collector = DataCollector(5, serial_ins)
    data_sets, num = collector.get_data_sets()
    print(data_sets)

    print(collector.get_set(3))
    # collector.start_collecting(2000)
    # data_sets, num = collector.get_data_sets()
    # print(data_sets)
    # print(len(data_sets['array1']))