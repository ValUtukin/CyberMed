from PyQt5.QtCore import QObject, pyqtSignal
import comport as com
import time


class DataCollector(QObject):
    finished = pyqtSignal()  # It doesn't work inside __init__ func. So it's placed outside (don't know why)
    segment_received = pyqtSignal()
    upper_segment_received_both = pyqtSignal()
    lower_segment_received_both = pyqtSignal()
    upper_both_finished = pyqtSignal()
    lower_both_finished = pyqtSignal()
    adc_check_complete = pyqtSignal()

    def __init__(self, set_num, args=None):
        super().__init__()
        self.data_set_holder = dict()
        self.holder_state = [False] * 5
        self.initial_delay = None
        self.initial_delay_both = None

        self.default_comport = None
        self.upper_comport_both = None
        self.lower_comport_both = None

        self.testing_data = []

        if not args:
            self.initial_byte_count = None
        else:
            self.initial_byte_count = args
        if set_num:
            if set_num > 0:
                for i in range(0, set_num):
                    self.data_set_holder[f'array{i + 1}'] = list()
                self.holder_len = set_num
            else:
                print(f'DataCollector.py/__init__ - set_num is invalid: {set_num}. Must be greater than 0')
                self.holder_len = 0
        else:
            print(f'DataCollector/__init__ - got 0 as parameter. Current holder_len is {len(self.data_set_holder)}')
            self.holder_len = 0

    def set_upper_comport_both(self, serial_inst):
        self.upper_comport_both = serial_inst

    def get_upper_comport_both(self):
        return self.upper_comport_both

    def set_lower_comport_both(self, serial_inst):
        self.lower_comport_both = serial_inst

    def get_lower_comport_both(self):
        return self.lower_comport_both

    def set_default_comport(self, serial_inst):
        self.default_comport = serial_inst

    def get_default_comport(self):
        return self.default_comport

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

    def set_delay_for_collecting_both(self, delay):
        self.initial_delay_both = delay

    def get_delay_for_collecting_together(self):
        return self.initial_delay_both

    def set_byte_count(self, byte_count):
        print(f"DataCollector/set_byte_count - byte count: {byte_count}")
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
        packet_counter = 0
        time.sleep(self.initial_delay)
        less = self.initial_byte_count % 20
        if self.holder_len:
            # Receive full packets - 20 bytes
            for i in range(0, self.initial_byte_count - less, 20):
                data = self.default_comport.read(20)
                packet_counter += 1
                print(f"Packet #{packet_counter}, len: {len(data)}")
                if len(data) == 0:
                    print("Packet len is 0")
                    # self.add_value_to_set('0', 0)
                else:
                    for j in range(1, len(data), 2):
                        print(f"data[{j-1}] = {data[j-1]}, data[{j}] = {data[j]}")
                        new_data = (data[j - 1] + data[j] * 256) * 3.3 / 4096
                        print(f"{j + 1}) {new_data}, type {type(new_data)}")
                        set_name = str(j % len(self.data_set_holder))
                        self.add_value_to_set(set_name, new_data)
                self.segment_received.emit()

            # Receive left bytes < 20
            print(f"Try to receive {less} bytes")
            less_data = self.default_comport.read(less)
            packet_counter += 1
            print(f"Packet #{packet_counter}, len: {len(less_data)}")
            for i in range(1, len(less_data), 2):
                print(f"data[{i - 1}] = {less_data[i - 1]}, data[{i}] = {less_data[i]}")
                new_data = (less_data[i - 1] + data[i] * 256) * 3.3 / 4096
                print(f"{i + 1}) {new_data}, type {type(new_data)}")
                set_name = str(i % len(self.data_set_holder))
                self.add_value_to_set(set_name, new_data)
            self.segment_received.emit()

            print(f'Just finished receiving data. Num of bytes {self.initial_byte_count}')
            com.close_comport(self.default_comport)
        self.finished.emit()

    def upper_start_collecting_both(self):
        print("DataCollector/upper_start_collecting_both - start collecting...")
        time.sleep(self.initial_delay_both)
        if self.holder_len:
            for i in range(0, self.initial_byte_count, 40):
                data = self.upper_comport_both.read(40)
                if len(data) == 0:
                    self.add_value_to_set('0', 0)
                else:
                    for j in range(0, len(data)):
                        print(f"{j + 1}) {data[j]}, type {type(data[j])}")
                        new_data = data[j] * 3.3 / 4096
                        set_name = str(j % len(self.data_set_holder))
                        self.add_value_to_set(set_name, new_data)  # self.add_value_to_set(set_name, new_data)
                self.upper_segment_received_both.emit()
                time.sleep(0.01)
            print(f'DataCollector/collect_both - Just finished receiving data. Num of bytes {self.initial_byte_count}')
            com.close_comport(self.upper_comport_both)
        self.upper_both_finished.emit()

    def lower_start_collecting_both(self):
        print("DataCollector/start_collecting_both - start collecting...")
        time.sleep(self.initial_delay_both)
        if self.holder_len:
            for i in range(0, self.initial_byte_count, 40):
                data = self.lower_comport_both.read(40)
                if len(data) == 0:
                    self.add_value_to_set('0', 0)
                else:
                    for j in range(0, len(data)):
                        print(f"{j + 1}) {data[j]}, type {type(data[j])}")
                        new_data = data[j] * 3.3 / 4096
                        set_name = str(j % len(self.data_set_holder))
                        self.add_value_to_set(set_name, new_data)  # self.add_value_to_set(set_name, new_data)
                self.lower_segment_received_both.emit()
                time.sleep(0.01)
            print(f'DataCollector/collect_both - Just finished receiving data. Num of bytes {self.initial_byte_count}')
            com.close_comport(self.lower_comport_both)
        self.lower_both_finished.emit()

    def upper_thread_test(self):
        packet_counter = 0
        time.sleep(self.initial_delay_both)
        if self.holder_len:
            for i in range(0, self.initial_byte_count, 20):
                data = self.upper_comport_both.read(20)
                packet_counter += 1
                print(f"Packet #{packet_counter}, len: {len(data)}")
                if len(data) == 0:
                    print("Packet len is 0")
                    # self.add_value_to_set('0', 0)
                else:
                    for j in range(1, len(data), 2):
                        print(f"data[{j - 1}] = {data[j - 1]}, data[{j}] = {data[j]}")
                        new_data = (data[j - 1] + data[j] * 256) * 3.3 / 4096
                        print(f"{j + 1}) {new_data}, type {type(new_data)}")
                        set_name = str(j % len(self.data_set_holder))
                        self.add_value_to_set(set_name, new_data)
                self.upper_segment_received_both.emit()
                time.sleep(0.01)
            print(f'Just finished receiving data. Num of bytes {self.initial_byte_count}')
            # com.close_comport(self.upper_comport_both)
        self.upper_both_finished.emit()

    def lower_thread_test(self):
        packet_counter = 0
        time.sleep(self.initial_delay_both)
        if self.holder_len:
            for i in range(0, self.initial_byte_count, 20):
                data = self.lower_comport_both.read(20)
                packet_counter += 1
                print(f"Packet #{packet_counter}, len: {len(data)}")
                if len(data) == 0:
                    print("Packet len is 0")
                    # self.add_value_to_set('0', 0)
                else:
                    for j in range(1, len(data), 2):
                        print(f"data[{j - 1}] = {data[j - 1]}, data[{j}] = {data[j]}")
                        new_data = (data[j - 1] + data[j] * 256) * 3.3 / 4096
                        print(f"{j + 1}) {new_data}, type {type(new_data)}")
                        set_name = str(j % len(self.data_set_holder))
                        self.add_value_to_set(set_name, new_data)
                self.lower_segment_received_both.emit()
                time.sleep(0.01)
            print(f'Just finished receiving data. Num of bytes {self.initial_byte_count}')
            # com.close_comport(self.lower_comport_both)
        self.lower_both_finished.emit()

    def simple_adc_test(self):
        for i in range(100):
            self.testing_data.append(i + 1)
            if len(self.testing_data) % 10 == 0:
                self.adc_check_complete.emit()
                time.sleep(0.5)
        self.finished.emit()

    def get_test_data(self):
        return self.testing_data


if __name__ == '__main__':
    collector = DataCollector(5)
    data_sets, num = collector.get_data_sets()
    print(data_sets)
