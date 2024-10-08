import time
import timeit
import datetime


def sandbox():
    last_values = [num/100 for num in range(1, 10)]
    ys = []
    x0 = 0.01
    x1 = 0.2
    y0 = 80
    y1 = 7
    for i in range(len(last_values)):
        x = (last_values[i] * 10) / 24.39
        y = (((y1 - y0) * (x - x0)) / (x1 - x0)) + y0
        ys.append(y)
    print(*last_values)
    print(*ys)

def sandbox1():
    array1 = [True, True, True]
    array2 = [True, False, True]

    if array1 == array2:
        print("Arrays are equal")
    else:
        print("Not equal")


def time_test():
    dt1 = datetime.datetime.now()
    print(dt1)
    for i in range(5):
        time.sleep(1.0)
    dt2 = datetime.datetime.now()
    print(dt2)
    dt2_str = str(dt2)
    print(f'str - {dt2_str}, type - {type(dt2_str)}')


if __name__ == '__main__':
    # sandbox()
    delay = 0
    char_delay = bytes(chr(delay), 'ascii')
    print(char_delay)
