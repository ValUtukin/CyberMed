import tkinter as tk
from pubsub import pub
from tkinter import *


class View:
    def __init__(self, parent):
        self.container = parent

    def setup(self):
        self.create_widgets()
        self.setup_layout()

    def create_widgets(self):
        self.power_status = BooleanVar()
        self.power_switch_checkbox = Checkbutton(self.container, text="Power", background='#b8dffe',
                                                 command=self.power_switch, variable=self.power_status,
                                                 onvalue=True, offvalue=False)
        self.adc_status = BooleanVar()
        self.adc_checkbox = Checkbutton(self.container, text='with ADC', background='#b8dffe',
                                               command=self.adc_change, variable=self.adc_status,
                                               onvalue=True, offvalue=False)
        self.global_timer_frame = tk.Frame(self.container, bg='#b8dffe')
        self.global_timer_label = Label(self.global_timer_frame, text='Global Time-limited motion', background='#b8dffe', font=('Arial', 10))
        self.global_timer_entry = Entry(self.global_timer_frame)
        self.global_timer_sec_label = Label(self.global_timer_frame, text='sec', background='#b8dffe', font=('Arial', 10))
        self.global_timer_status = BooleanVar()
        self.global_timer_checkbox = Checkbutton(self.global_timer_frame, background='#b8dffe',
                                                 variable=self.global_timer_status, onvalue=True, offvalue=False)

        self.motor1_label = Label(self.container, text='Motor 1', background='#b8dffe', font=('Arial', 10))
        self.motor1_left_button = Button(self.container, text='Left', command=self.motor1_rotate_left)
        self.motor1_right_button = Button(self.container, text='Right', command=self.motor1_rotate_right)
        self.motor1_stop_button = Button(self.container, text='Stop', command=self.motor1_rotate_stop)
        self.motor1_buttons = [self.motor1_left_button, self.motor1_right_button, self.motor1_stop_button]
        self.motor1_pwm_scale = Scale(self.container, from_=0, to=50, orient=HORIZONTAL, length=100, width=10,
                                      label="PWM", command=self.motor1_pwm_scale_change)

        self.motor1_timer_frame = tk.Frame(self.container, bg='#b8dffe')
        self.motor1_timer_label = Label(self.motor1_timer_frame, text='Motor#1 Time-limited motion', background='#b8dffe', font=('Arial', 10))
        self.motor1_timer_entry = Entry(self.motor1_timer_frame)
        self.motor1_timer_sec_label = Label(self.motor1_timer_frame, text='sec', background='#b8dffe', font=('Arial', 10))
        self.motor1_timer_status = BooleanVar()
        self.motor1_timer_checkbox = Checkbutton(self.motor1_timer_frame, background='#b8dffe',
                                                 variable=self.motor1_timer_status, onvalue=True, offvalue=False)

        self.motor2_label = Label(self.container, text='Motor 2', background='#b8dffe', font=('Arial', 10))
        self.motor2_left_button = Button(self.container, text='Left', command=self.motor2_rotate_left)
        self.motor2_right_button = Button(self.container, text='Right', command=self.motor2_rotate_right)
        self.motor2_stop_button = Button(self.container, text='Stop', command=self.motor2_rotate_stop)
        self.motor2_buttons = [self.motor2_left_button, self.motor2_right_button, self.motor2_stop_button]
        self.motor2_pwm_scale = Scale(self.container, from_=0, to=50, orient=HORIZONTAL, length=100, width=10,
                                      label="PWM")

        self.motor2_timer_frame = tk.Frame(self.container, bg='#b8dffe')
        self.motor2_timer_label = Label(self.motor2_timer_frame, text='Motor#2 Time-limited motion', background='#b8dffe', font=('Arial', 10))
        self.motor2_timer_entry = Entry(self.motor2_timer_frame)
        self.motor2_timer_sec_label = Label(self.motor2_timer_frame, text='sec', background='#b8dffe', font=('Arial', 10))
        self.motor2_timer_status = BooleanVar()
        self.motor2_timer_checkbox = Checkbutton(self.motor2_timer_frame, background='#b8dffe',
                                                 variable=self.motor2_timer_status, onvalue=True, offvalue=False)

        self.motor3_label = Label(self.container, text='Motor 3', background='#b8dffe', font=('Arial', 10))
        self.motor3_left_button = Button(self.container, text='Left', command=self.motor3_rotate_left)
        self.motor3_right_button = Button(self.container, text='Right', command=self.motor3_rotate_right)
        self.motor3_stop_button = Button(self.container, text='Stop', command=self.motor3_rotate_stop)
        self.motor3_buttons = [self.motor3_left_button, self.motor3_right_button, self.motor3_stop_button]
        self.motor3_pwm_scale = Scale(self.container, from_=0, to=50, orient=HORIZONTAL, length=100, width=10,
                                      label="PWM")

        self.motor3_timer_frame = tk.Frame(self.container, bg='#b8dffe')
        self.motor3_timer_label = Label(self.motor3_timer_frame, text='Motor#3 Time-limited motion', background='#b8dffe', font=('Arial', 10))
        self.motor3_timer_entry = Entry(self.motor3_timer_frame)
        self.motor3_timer_sec_label = Label(self.motor3_timer_frame, text='sec', background='#b8dffe', font=('Arial', 10))
        self.motor3_timer_status = BooleanVar()
        self.motor3_timer_checkbox = Checkbutton(self.motor3_timer_frame, background='#b8dffe',
                                                 variable=self.motor3_timer_status, onvalue=True, offvalue=False)

        self.motor4_label = Label(self.container, text='Motor 4', background='#b8dffe', font=('Arial', 10))
        self.motor4_left_button = Button(self.container, text='Left', command=self.motor4_rotate_left)
        self.motor4_right_button = Button(self.container, text='Right', command=self.motor4_rotate_right)
        self.motor4_stop_button = Button(self.container, text='Stop', command=self.motor4_rotate_stop)
        self.motor4_buttons = [self.motor4_left_button, self.motor4_right_button, self.motor4_stop_button]
        self.motor4_pwm_scale = Scale(self.container, from_=0, to=50, orient=HORIZONTAL, length=100, width=10,
                                      label="PWM")

        self.motor4_timer_frame = tk.Frame(self.container, bg='#b8dffe')
        self.motor4_timer_label = Label(self.motor4_timer_frame, text='Motor#4 Time-limited motion', background='#b8dffe', font=('Arial', 10))
        self.motor4_timer_entry = Entry(self.motor4_timer_frame)
        self.motor4_timer_sec_label = Label(self.motor4_timer_frame, text='sec', background='#b8dffe', font=('Arial', 10))
        self.motor4_timer_status = BooleanVar()
        self.motor4_timer_checkbox = Checkbutton(self.motor4_timer_frame, background='#b8dffe',
                                                 variable=self.motor4_timer_status, onvalue=True, offvalue=False)

        self.motor5_label = Label(self.container, text='Motor 5', background='#b8dffe', font=('Arial', 10))
        self.motor5_left_button = Button(self.container, text='Left', command=self.motor5_rotate_left)
        self.motor5_right_button = Button(self.container, text='Right', command=self.motor5_rotate_right)
        self.motor5_stop_button = Button(self.container, text='Stop', command=self.motor5_rotate_stop)
        self.motor5_buttons = [self.motor5_left_button, self.motor5_right_button, self.motor5_stop_button]
        self.motor5_pwm_scale = Scale(self.container, from_=0, to=50, orient=HORIZONTAL, length=100, width=10,
                                      label="PWM")

        self.motor5_timer_frame = tk.Frame(self.container, bg='#b8dffe')
        self.motor5_timer_label = Label(self.motor5_timer_frame, text='Motor#5 Time-limited motion', background='#b8dffe', font=('Arial', 10))
        self.motor5_timer_entry = Entry(self.motor5_timer_frame)
        self.motor5_timer_sec_label = Label(self.motor5_timer_frame, text='sec', background='#b8dffe', font=('Arial', 10))
        self.motor5_timer_status = BooleanVar()
        self.motor5_timer_checkbox = Checkbutton(self.motor5_timer_frame, background='#b8dffe',
                                                 variable=self.motor5_timer_status, onvalue=True, offvalue=False)

    def setup_layout(self):
        self.adc_checkbox.place(relx=0.01, rely=0.02, relheight=0.05, relwidth=0.1)
        self.power_switch_checkbox.place(relx=0.12, rely=0.02, relheight=0.05, relwidth=0.07)

        self.global_timer_frame.place(relx=0.2, rely=0.01, relheight=0.08, relwidth=0.22)
        self.global_timer_label.place(relx=0.05, rely=0.05, relheight=0.25, relwidth=0.9)
        self.global_timer_entry.place(relx=0.2, rely=0.5, relheight=0.35, relwidth=0.35)
        self.global_timer_sec_label.place(relx=0.6, rely=0.52, relheight=0.21, relwidth=0.15)
        self.global_timer_checkbox.place(relx=0.05, rely=0.5, relheight=0.3, relwidth=0.13)

        self.motor1_label.place(relx=0.01, rely=0.13, relheight=0.05)
        self.motor1_left_button.place(relx=0.08, rely=0.13, relheight=0.05, relwidth=0.08)
        self.motor1_right_button.place(relx=0.165, rely=0.13, relheight=0.05, relwidth=0.08)
        self.motor1_stop_button.place(relx=0.25, rely=0.13, relheight=0.05, relwidth=0.08)
        self.motor1_pwm_scale.place(relx=0.335, rely=0.11)
        self.motor1_timer_frame.place(relx=0.48, rely=0.115, relheight=0.08, relwidth=0.23)
        self.motor1_timer_label.place(relx=0.05, rely=0.05, relheight=0.25, relwidth=0.9)
        self.motor1_timer_entry.place(relx=0.2, rely=0.5, relheight=0.35, relwidth=0.35)
        self.motor1_timer_sec_label.place(relx=0.6, rely=0.52, relheight=0.21, relwidth=0.15)
        self.motor1_timer_checkbox.place(relx=0.05, rely=0.5, relheight=0.3, relwidth=0.13)

        self.motor2_label.place(relx=0.01, rely=0.24, relheight=0.05)
        self.motor2_left_button.place(relx=0.08, rely=0.24, relheight=0.05, relwidth=0.08)
        self.motor2_right_button.place(relx=0.165, rely=0.24, relheight=0.05, relwidth=0.08)
        self.motor2_stop_button.place(relx=0.25, rely=0.24, relheight=0.05, relwidth=0.08)
        self.motor2_pwm_scale.place(relx=0.335, rely=0.22)
        self.motor2_timer_frame.place(relx=0.48, rely=0.225, relheight=0.08, relwidth=0.23)
        self.motor2_timer_label.place(relx=0.05, rely=0.05, relheight=0.25, relwidth=0.9)
        self.motor2_timer_entry.place(relx=0.2, rely=0.5, relheight=0.35, relwidth=0.35)
        self.motor2_timer_sec_label.place(relx=0.6, rely=0.52, relheight=0.21, relwidth=0.15)
        self.motor2_timer_checkbox.place(relx=0.05, rely=0.5, relheight=0.3, relwidth=0.13)

        self.motor3_label.place(relx=0.01, rely=0.35, relheight=0.05)
        self.motor3_left_button.place(relx=0.08, rely=0.35, relheight=0.05, relwidth=0.08)
        self.motor3_right_button.place(relx=0.165, rely=0.35, relheight=0.05, relwidth=0.08)
        self.motor3_stop_button.place(relx=0.25, rely=0.35, relheight=0.05, relwidth=0.08)
        self.motor3_pwm_scale.place(relx=0.335, rely=0.33)
        self.motor3_timer_frame.place(relx=0.48, rely=0.335, relheight=0.08, relwidth=0.23)
        self.motor3_timer_label.place(relx=0.05, rely=0.05, relheight=0.25, relwidth=0.9)
        self.motor3_timer_entry.place(relx=0.2, rely=0.5, relheight=0.35, relwidth=0.35)
        self.motor3_timer_sec_label.place(relx=0.6, rely=0.52, relheight=0.21, relwidth=0.15)
        self.motor3_timer_checkbox.place(relx=0.05, rely=0.5, relheight=0.3, relwidth=0.13)

        self.motor4_label.place(relx=0.01, rely=0.46, relheight=0.05)
        self.motor4_left_button.place(relx=0.08, rely=0.46, relheight=0.05, relwidth=0.08)
        self.motor4_right_button.place(relx=0.165, rely=0.46, relheight=0.05, relwidth=0.08)
        self.motor4_stop_button.place(relx=0.25, rely=0.46, relheight=0.05, relwidth=0.08)
        self.motor4_pwm_scale.place(relx=0.335, rely=0.44)
        self.motor4_timer_frame.place(relx=0.48, rely=0.445, relheight=0.08, relwidth=0.23)
        self.motor4_timer_label.place(relx=0.05, rely=0.05, relheight=0.25, relwidth=0.9)
        self.motor4_timer_entry.place(relx=0.2, rely=0.5, relheight=0.35, relwidth=0.35)
        self.motor4_timer_sec_label.place(relx=0.6, rely=0.52, relheight=0.21, relwidth=0.15)
        self.motor4_timer_checkbox.place(relx=0.05, rely=0.5, relheight=0.3, relwidth=0.13)

        self.motor5_label.place(relx=0.01, rely=0.57, relheight=0.05)
        self.motor5_left_button.place(relx=0.08, rely=0.57, relheight=0.05, relwidth=0.08)
        self.motor5_right_button.place(relx=0.165, rely=0.57, relheight=0.05, relwidth=0.08)
        self.motor5_stop_button.place(relx=0.25, rely=0.57, relheight=0.05, relwidth=0.08)
        self.motor5_pwm_scale.place(relx=0.335, rely=0.55)
        self.motor5_timer_frame.place(relx=0.48, rely=0.555, relheight=0.08, relwidth=0.23)
        self.motor5_timer_label.place(relx=0.05, rely=0.05, relheight=0.25, relwidth=0.9)
        self.motor5_timer_entry.place(relx=0.2, rely=0.5, relheight=0.35, relwidth=0.35)
        self.motor5_timer_sec_label.place(relx=0.6, rely=0.52, relheight=0.21, relwidth=0.15)
        self.motor5_timer_checkbox.place(relx=0.05, rely=0.5, relheight=0.3, relwidth=0.13)

    def switch_button_color(self, button, color='#19e676'):
        if button['bg'] == 'SystemButtonFace':
            button.config(bg=color)
        else:
            button.config(bg='SystemButtonFace')

    def configure_relatives_buttons(self, group_buttons, pressed_button):
        self.switch_button_color(group_buttons[pressed_button])
        current_button_group_copy = group_buttons.copy()
        del current_button_group_copy[pressed_button]
        for i in range(0, len(current_button_group_copy)):
            self.switch_button_color(current_button_group_copy[i], color='SystemButtonFace')

    def adc_change(self):
        pub.sendMessage("Adc_change")

    def power_switch(self):
        pub.sendMessage("Power_switch")

    def motor1_rotate_left(self):
        pub.sendMessage("Motor1_rotate_left")
        self.configure_relatives_buttons(self.motor1_buttons, 0)

    def motor1_rotate_right(self):
        pub.sendMessage("Motor1_rotate_right")
        self.configure_relatives_buttons(self.motor1_buttons, 1)

    def motor1_rotate_stop(self):
        pub.sendMessage("Motor1_rotate_stop")
        self.configure_relatives_buttons(self.motor1_buttons, 2)

    def motor1_pwm_scale_change(self, arg2):
        pub.sendMessage("Motor1_pwm_scale_change")

    def motor2_rotate_left(self):
        pub.sendMessage("Motor2_rotate_left")
        self.configure_relatives_buttons(self.motor2_buttons, 0)

    def motor2_rotate_right(self):
        pub.sendMessage("Motor2_rotate_right")
        self.configure_relatives_buttons(self.motor2_buttons, 1)

    def motor2_rotate_stop(self):
        pub.sendMessage("Motor2_rotate_stop")
        self.configure_relatives_buttons(self.motor2_buttons, 2)

    def motor2_pwm_scale_change(self, arg2):
        pub.sendMessage("Motor2_pwm_scale_change")

    def motor3_rotate_left(self):
        pub.sendMessage("Motor3_rotate_left")
        self.configure_relatives_buttons(self.motor3_buttons, 0)

    def motor3_rotate_right(self):
        pub.sendMessage("Motor3_rotate_right")
        self.configure_relatives_buttons(self.motor3_buttons, 1)

    def motor3_rotate_stop(self):
        pub.sendMessage("Motor3_rotate_stop")
        self.configure_relatives_buttons(self.motor3_buttons, 2)

    def motor3_pwm_scale_change(self, arg2):
        pub.sendMessage("Motor3_pwm_scale_change")

    def motor4_rotate_left(self):
        pub.sendMessage("Motor4_rotate_left")
        self.configure_relatives_buttons(self.motor4_buttons, 0)

    def motor4_rotate_right(self):
        pub.sendMessage("Motor4_rotate_right")
        self.configure_relatives_buttons(self.motor4_buttons, 1)

    def motor4_rotate_stop(self):
        pub.sendMessage("Motor4_rotate_stop")
        self.configure_relatives_buttons(self.motor4_buttons, 2)

    def motor4_pwm_scale_change(self, arg2):
        pub.sendMessage("Motor4_pwm_scale_change")

    def motor5_rotate_left(self):
        pub.sendMessage("Motor5_rotate_left")
        self.configure_relatives_buttons(self.motor5_buttons, 0)

    def motor5_rotate_right(self):
        pub.sendMessage("Motor5_rotate_right")
        self.configure_relatives_buttons(self.motor5_buttons, 1)

    def motor5_rotate_stop(self):
        pub.sendMessage("Motor5_rotate_stop")
        self.configure_relatives_buttons(self.motor5_buttons, 2)

    def motor5_pwm_scale_change(self, arg2):
        pub.sendMessage("Motor5_pwm_scale_change")


if __name__ == '__main__':
    root = Tk()
    root['bg'] = '#0585e8'
    root.title('Motor Client')
    root.geometry('800x600')
    photo = PhotoImage(file="../Images/cyber_hand.png")
    root.iconphoto(False, photo)
    root.resizable(width=False, height=True)

    view = View(root)
    view.setup()

    root.mainloop()
