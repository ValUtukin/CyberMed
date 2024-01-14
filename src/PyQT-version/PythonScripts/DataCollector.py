from PyQt5.QtCore import QObject, pyqtSignal
import comport as com
import time


class DataCollector(QObject):
    finished = pyqtSignal()  # It doesn't work inside __init__ func. So it's placed outside (don't know why)
    segment_received = pyqtSignal()

    def __init__(self, set_num, args=None, comport=None):
        super().__init__()
        self.data_set_holder = dict()
        self.holder_state = [False] * 5
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

    def set_holder_state(self, state_arr):
        self.delete_all_sets()
        counter = 0
        for i in range(0, len(state_arr)):
            if state_arr[i]:
                self.data_set_holder[f'{counter}'] = list()
                counter += 1

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

    def delete_all_sets(self):
        self.data_set_holder.clear()

    def start_collecting(self):
        time.sleep(self.initial_delay)
        if self.holder_len:
            for i in range(0, self.initial_byte_count, 25):
                data = self.comport.read(25)
                if len(data) == 0:
                    self.add_value_to_set('0', 0)
                else:
                    for j in range(0, len(data)):
                        print(f"{j + 1}) {data[j]}, type {type(data[j])}")
                        new_data = data[j] * 3.3 / 4096
                        set_name = str(j % len(self.data_set_holder))
                        self.add_value_to_set(set_name, new_data)
                self.segment_received.emit()
                print("DataCollector/start_collecting - start sleeping...")
                time.sleep(0.1)
            print(f'Just finished receiving data. Num of bytes {self.initial_byte_count}')
            com.close_comport(self.comport)
        self.finished.emit()


if __name__ == '__main__':
    serial_ins = com.ini('COM2')
    collector = DataCollector(5, serial_ins)
    data_sets, num = collector.get_data_sets()
    print(data_sets)