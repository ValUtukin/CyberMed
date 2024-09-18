
def sandbox():
    lower_motors_rotation_dict = {
        '1': '01',
        '2': '01',
        '3': '01',
        '4': '01',
        '5': '01',
        '6': '01',
        '_1': '10',
        '_2': '10',
        '_3': '10',
        '_4': '10',
        '_5': '10',
        '_6': '10'
    }
    upper_motors_finger_dict = {
        '1': '000',
        '2': '001',
        '3': '010',
        '4': '011',
        '5': '100',
        '6': '101'
    }
    target_key = '2'
    target_value = '100'
    for key, value in upper_motors_finger_dict.items():
        if value == target_value:
            print(f'Find a match: key -> {key}, value -> {value}')
            temp = upper_motors_finger_dict[target_key]
            upper_motors_finger_dict[target_key] = target_value
            upper_motors_finger_dict[key] = temp
    print(upper_motors_finger_dict)


def sandbox1():
    array1 = [True, True, True]
    array2 = [True, False, True]

    if array1 == array2:
        print("Arrays are equal")
    else:
        print("Not equal")


if __name__ == '__main__':
    # sandbox1()
    print(1 & 1)

