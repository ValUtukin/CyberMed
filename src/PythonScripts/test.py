import time
import timeit
import datetime
from decimal import Decimal


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


def enumerate_test():
    for i, value in enumerate(range(0, 100, 2)):
        print(f"{i}: {value}")


def sandbox1():
    my_dict = {
        '0': [0, 0, 0],
        '1': [1, 1, 1],
        '2': [2, 2, 2]
    }

    for j in range(20):
        set_name = str(j % len(my_dict))
        print(set_name)


def zip_test():
    a = [1, 4, 3, 4]
    b = [1, 5, 3]
    for i, pair in enumerate(zip(a, b)):
        print(f"{i}: {pair}")


def hex_convert(hex_str):
    print(int(hex_str, 16))


def time_test():
    dt1 = datetime.datetime.now()
    print(dt1)
    for i in range(5):
        time.sleep(1.0)
    dt2 = datetime.datetime.now()
    print(dt2)
    dt2_str = str(dt2)
    print(f'str - {dt2_str}, type - {type(dt2_str)}')


def test():
    target = 3
    for i in range(10):
        if i % target == 0:
            print(i)


if __name__ == '__main__':
    test()
