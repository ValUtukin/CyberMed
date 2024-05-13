def get_lower_opposite_pwm(up_pwm):
    opposite_coefficient = 69/70
    yield int(up_pwm * opposite_coefficient)


def get_upper_opposite_pwm(low_pwm):
    opposite_coefficient = 1/2
    yield int(low_pwm * opposite_coefficient)


upper_pwm_generator = get_upper_opposite_pwm
print(upper_pwm_generator(60))

print("Home changes to test new develop branch")

print("Home second changes to test new develop branch")

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
target_key = 3
for key in lower_motors_rotation_dict.keys():
    pass