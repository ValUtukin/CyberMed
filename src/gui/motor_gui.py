from tkinter import *
import src.comports as comport
import src.gui.motor_buttons as mb


def get_bytestring():
    config_byte = str(config_byte_entry.get())
    pwm_int = int(pwm_byte_entry.get())
    warning_label = Label(root, text='8 bits!', background='#f65e05', font=('Arial', 10))
    if len(config_byte) == 8:
        for i in range(0, 8):
            if config_byte[i] in '01':
                continue
            else:
                warning_label["text"] = '1 and 0'
                warning_label["background"] = '#f65e05'
                warning_label["font"] = ('Arial', 10)
                warning_label.place(relx=0.81, rely=0.01, relheight=0.056, relwidth=0.15)
                break
        else:
            warning_label["text"] = 'Sent!'
            warning_label["background"] = '#08fa46'
            warning_label["font"] = ('Arial', 10)
            warning_label.place(relx=0.81, rely=0.01, relheight=0.056, relwidth=0.15)
            comport.main(config_byte, pwm_int)
    else:
        warning_label.place(relx=0.81, rely=0.01, relheight=0.056, relwidth=0.15)


def motor1_rotate_left():
    pwm = motor1_pwm_entry.get()
    motor1_pwm_entry.delete(0, 'end')
    mb.motor1_left(pwm)


def motor1_rotate_right():
    pwm = motor1_pwm_entry.get()
    motor1_pwm_entry.delete(0, 'end')
    mb.motor1_right(pwm)


def motor1_rotate_stop():
    mb.motor1_stop()


def motor2_rotate_left():
    pwm = motor2_pwm_entry.get()
    motor2_pwm_entry.delete(0, 'end')
    mb.motor2_left(pwm)


def motor2_rotate_right():
    pwm = motor2_pwm_entry.get()
    motor2_pwm_entry.delete(0, 'end')
    mb.motor2_right(pwm)


def motor2_rotate_stop():
    mb.motor2_stop()


root = Tk()
root['bg'] = '#0585e8'
root.title('Motor Client')
root.geometry('480x320')
photo = PhotoImage(file="../../Images/cyber_hand.png")
root.iconphoto(False, photo)
root.resizable(width=False, height=True)

bytestring_label = Label(root, text='Enter byte string e.g. "00110110" (7 <= 0)', background='#b8dffe', font=('Arial', 10))
bytestring_label.place(relx=0.01, rely=0.01, relheight=0.05)

bytestring_label = Label(root, text='Enter integer PWM (0 - 100)', background='#b8dffe', font=('Arial', 10))
bytestring_label.place(relx=0.17, rely=0.07, relheight=0.05)

config_byte_entry = Entry()
config_byte_entry.place(relx=0.54, rely=0.01, relheight=0.05, relwidth=0.15)

pwm_byte_entry = Entry()
pwm_byte_entry.place(relx=0.54, rely=0.07, relheight=0.05, relwidth=0.15)

bytestring_button = Button(root, text='Send', command=get_bytestring)
bytestring_button.place(relx=0.7, rely=0.01, relheight=0.1, relwidth=0.1)

motor1_label = Label(root, text='Motor 1', background='#b8dffe', font=('Arial', 10))
motor1_label.place(relx=0.01, rely=0.15, relheight=0.05)

motor1_left_button = Button(root, text='Left', command=motor1_rotate_left)
motor1_left_button.place(relx=0.01, rely=0.21, relheight=0.05, relwidth=0.1)

motor1_right_button = Button(root, text='Right', command=motor1_rotate_right)
motor1_right_button.place(relx=0.01, rely=0.27, relheight=0.06, relwidth=0.1)

motor1_stop_button = Button(root, text='Stop', command=motor1_rotate_stop)
motor1_stop_button.place(relx=0.01, rely=0.34, relheight=0.06, relwidth=0.1)

motor1_pwm_entry = Entry()
motor1_pwm_entry.place(relx=0.01, rely=0.41, relheight=0.05, relwidth=0.1)

motor2_label = Label(root, text='Motor 2', background='#b8dffe', font=('Arial', 10))
motor2_label.place(relx=0.12, rely=0.15, relheight=0.05)

motor2_left_button = Button(root, text='Left', command=motor2_rotate_left)
motor2_left_button.place(relx=0.12, rely=0.21, relheight=0.05, relwidth=0.1)

motor2_right_button = Button(root, text='Right', command=motor2_rotate_right)
motor2_right_button.place(relx=0.12, rely=0.27, relheight=0.06, relwidth=0.1)

motor2_stop_button = Button(root, text='Stop', command=motor2_rotate_stop)
motor2_stop_button.place(relx=0.12, rely=0.34, relheight=0.06, relwidth=0.1)

motor2_pwm_entry = Entry()
motor2_pwm_entry.place(relx=0.12, rely=0.41, relheight=0.05, relwidth=0.1)

root.mainloop()
