def get_lower_opposite_pwm(up_pwm):
    opposite_coefficient = 69/70
    yield int(up_pwm * opposite_coefficient)


def get_upper_opposite_pwm(low_pwm):
    opposite_coefficient = 1/2
    yield int(low_pwm * opposite_coefficient)


upper_pwm_generator = get_upper_opposite_pwm
print(upper_pwm_generator(60))
