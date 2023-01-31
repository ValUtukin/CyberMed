import src.comports as comport


def validate_pwm(pwm):
    if pwm == '':
        return False
    else:
        if 1 <= len(pwm) <= 3:
            for i in range(0, len(pwm)):
                if pwm[i] in '0123456789':
                    continue
                else:
                    return False  # PWM must be a number
            else:
                if 0 <= int(pwm) <= 100:
                    return True
                else:
                    return False  # PWM needs to be an integer between 0 and 100
        else:
            return False  # PWM must be 1, 2 or 3 digits long


def motor1_left(pwm):
    if validate_pwm(pwm):
        int_pwm = int(pwm)
        config_byte = '01010001'  # 1st Motor, left rotation
        print('Motor #1 - left')
        print(f"We're about to send {config_byte} with PWM:{int_pwm} \n")
        comport.main(config_byte, int_pwm)
        return 'All sent'
    else:
        return 'Incorrect PWM'


def motor1_right(pwm):
    if validate_pwm(pwm):
        int_pwm = int(pwm)
        config_byte = '01100001'  # 1st Motor, right rotation
        print('Motor #1 - right')
        print(f"We're about to send {config_byte} with PWM:{int_pwm} \n")
        comport.main(config_byte, int_pwm)
        return 'All sent'
    else:
        return 'Incorrect PWM'


def motor1_stop():
    config_byte = '01000000'
    comport.main(config_byte, 0)


def motor2_left(pwm):
    if validate_pwm(pwm):
        int_pwm = int(pwm)
        config_byte = '01010011'  # 2nd Motor, left rotation
        print('Motor #2 - left')
        print(f"We're about to send {config_byte} with PWM:{int_pwm} \n")
        comport.main(config_byte, int_pwm)
        return 'All sent'
    else:
        return 'Incorrect PWM'


def motor2_right(pwm):
    if validate_pwm(pwm):
        int_pwm = int(pwm)
        config_byte = '01100011'  # 2nd Motor, right rotation
        print('Motor #2 - right')
        print(f"We're about to send {config_byte} with PWM:{int_pwm} \n")
        comport.main(config_byte, int_pwm)
        return 'All sent'
    else:
        return 'Incorrect PWM'


def motor2_stop():
    config_byte = '01000010'
    comport.main(config_byte, 0)


def main():
    pass


if __name__ == '__main__':
    main()
