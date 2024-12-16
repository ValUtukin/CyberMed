import comport as com
import time
from logging import getLogger
from PyQt5.QtCore import QObject, pyqtSignal


class DataCollector(QObject):
    finished = pyqtSignal()  # It doesn't work inside __init__ func. So it's placed outside (don't know why)
    segment_received = pyqtSignal()
    upper_segment_received_both = pyqtSignal()
    lower_segment_received_both = pyqtSignal()
    upper_both_finished = pyqtSignal()
    lower_both_finished = pyqtSignal()
    adc_check_complete = pyqtSignal()

    def __init__(self, set_num, name, args=None):
        super().__init__()
        self.collector_name = name
        self.data_set_holder = dict()

        self.data_set_holder_matrix = []

        self.holder_state = [False] * 5
        self.initial_delay = None
        self.initial_delay_both = None

        self.default_comport = None
        self.upper_comport_both = None
        self.lower_comport_both = None

        self.test_adc_byte_count = None
        self.test_adc_delay = None
        self.testing_data = list()

        self.logger = getLogger(f"{self.collector_name} Collector")
        self.logger.info(f"Collector Init: {self.collector_name}")

        self.current_ema_list = list()

        if not args:
            self.initial_byte_count = None
        else:
            self.initial_byte_count = args
        if set_num:
            # logging.debug(f"set_num != 0 ({set_num}) --> prepare data_set_holder")
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

    def ema_convertion(self, data: list, pc) -> list[float]:
        alpha = 0.01
        if pc != 1:  # If packet counter > 1 so first elem in result list = data[0]
            result = [self.current_ema_list[-1]]
        elif pc == 1:  # If packet counter == 1 so first elem in result list = data[0]
            result = [data[0]]
        else:
            result = 0

        for i in range(1, len(data)):
            next_ema = alpha * data[i] + (1 - alpha) * result[-1]
            result.append(next_ema)
            self.current_ema_list.append(next_ema)
        return result

    def clear_ema_list(self):
        self.current_ema_list.clear()

    def set_upper_comport_both(self, serial_inst):
        self.upper_comport_both = serial_inst

    def set_lower_comport_both(self, serial_inst):
        self.lower_comport_both = serial_inst

    def set_default_comport(self, serial_inst):
        self.default_comport = serial_inst

    def set_holder_state(self, state_arr):
        self.logger.debug(f"Setting data holder state: {state_arr}")
        self.delete_all_sets()
        counter = 0
        for i in range(0, len(state_arr)):
            if state_arr[i]:
                self.data_set_holder[f'{counter}'] = list()
                counter += 1
        self.logger.debug(f"Current holder state: {self.data_set_holder}")

    def get_set(self, number='0'):
        return self.data_set_holder[f'{number}']

    def set_delay_for_collecting(self, delay):
        self.logger.debug(f"Setting collector delay: {delay}")
        self.initial_delay = delay

    def set_delay_for_collecting_both(self, delay):
        self.initial_delay_both = delay

    def set_byte_count(self, byte_count):
        self.logger.debug(f"Setting collector byte_count: {byte_count}")
        self.initial_byte_count = byte_count

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
        self.logger.info("Start Collecting")
        self.logger.debug(f"Sleep before work: {self.initial_delay}")
        time.sleep(self.initial_delay)

        packet_counter = 0
        '''target_packet_amount needed to emit signal every N packet. Essentially this variable need to control 
        the amount of correcting PWM commands. When target segment is received (e.g. 100) emitting signal and calling
        upper_/lower_process_segment in ManualControl class. This method firstly calculate the opposite PWM, then
        sends correcting command to opposite side and then either plot data on graph or not.'''
        target_packet_amount = 100
        less = self.initial_byte_count % 20
        self.logger.debug(f"Less bytes: {less}")
        if self.holder_len:
            # Receive full packets - 20 bytes
            for _ in range(0, self.initial_byte_count - less, 20):
                data = self.default_comport.read(20)
                packet_counter += 1
                # self.logger.debug(f"{packet_counter} Packet received. Len: {len(data)}")
                print(f"{packet_counter} Packet received. Len: {len(data)}")
                # self.logger.debug(f"Packet #{packet_counter}: {data}")
                if len(data) == 0:
                    self.logger.warning(f"Packet #{packet_counter} len is 0. Add 20 zeros")
                    for k in range(20):
                        set_name = str(k % len(self.data_set_holder))
                        self.add_value_to_set(set_name, 0)
                        # self.logger.debug(f"Add 0 to set with key {set_name}")
                else:
                    temp_data = []
                    # Data calculation
                    for j in range(1, len(data), 2):
                        # print(f"data[{j-1}] = {data[j-1]}, data[{j}] = {data[j]}")
                        new_data = (data[j - 1] + data[j] * 256) * 3.3 / 4096
                        # print(f"{j + 1}) {new_data}, type {type(new_data)}")
                        temp_data.append(new_data)

                    ema_data = self.ema_convertion(data=temp_data, pc=packet_counter)

                    # Sorting data to sets
                    for i in range(len(ema_data)):
                        set_name = str(i % len(self.data_set_holder))
                        self.add_value_to_set(set_name, ema_data[i])
                        # self.logger.debug(f"Add {temp_data[i]} to set with key {set_name}")

                # Emitting signal only if packet with target number is received. See definition of target_packet_amount
                if packet_counter % target_packet_amount == 0:
                    print(f"Segment {packet_counter} received. Emitting signal")
                    self.segment_received.emit()

            # Receive left bytes < 20
            if less != 0:
                temp_data = []
                self.logger.debug(f"Receiving less bytes: {less}")
                less_data = self.default_comport.read(less)
                packet_counter += 1
                print(f"Packet #{packet_counter}, len: {len(less_data)}")
                self.logger.debug(f"Packet #{packet_counter}: {less_data}")
                # Less data calculation
                for i in range(1, len(less_data), 2):
                    print(f"data[{i-1}] = {less_data[i-1]}, data[{i}] = {less_data[i]}")
                    new_data = (less_data[i - 1] + less_data[i] * 256) * 3.3 / 4096
                    print(f"{i + 1}) {new_data}, type {type(new_data)}")
                # Sorting less data to sets
                for j in range(len(temp_data)):
                    set_name = str(j % len(self.data_set_holder))
                    self.add_value_to_set(set_name, temp_data[j])
                    # self.logger.debug(f"Add {temp_data[j]} to set with key {set_name}")
                self.logger.debug(f"Segment {packet_counter} received. Emitting signal")
                self.segment_received.emit()

            print(f'Just finished receiving data. Num of bytes {self.initial_byte_count}')
            print(f"All amount of packets: {packet_counter}")
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

    # ADC-Testing block. Used by MainApp to test ADC work
    def set_test_adc_byte_count(self, time_to_work):
        self.test_adc_byte_count = int(time_to_work * 50)

    def set_test_adc_delay(self, delay_before_work):
        self.test_adc_delay = delay_before_work

    def simple_adc_test(self):
        time.sleep(self.test_adc_delay)
        packet_counter = 0
        for i in range(0, self.test_adc_byte_count, 20):
            data = self.default_comport.read(20)
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

                    self.testing_data.append(round(new_data, 3))
        time.sleep(0.5)
        self.adc_check_complete.emit()
        self.finished.emit()

    def get_test_data(self):
        return self.testing_data

    def clear_test_data(self):
        self.testing_data.clear()
