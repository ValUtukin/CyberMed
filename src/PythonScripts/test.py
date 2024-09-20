
def sandbox():
    init_byte = 50
    print(init_byte % 20)
    print(init_byte // 20)


def sandbox1():
    array1 = [True, True, True]
    array2 = [True, False, True]

    if array1 == array2:
        print("Arrays are equal")
    else:
        print("Not equal")


if __name__ == '__main__':
    sandbox()

