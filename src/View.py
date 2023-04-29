import tkinter as tk
import cv2 as cv
from pubsub import pub
from tkinter import *
from PIL import ImageTk, Image
from MotorsFrame import MotorsFrame


class View:
    def __init__(self, parent):
        self.container = parent
        self.upper_motors_frame = MotorsFrame(self.container, 'Upper')
        self.lower_motors_frame = MotorsFrame(self.container, 'Lower')

        pub.subscribe(self.adc_figure_update, 'Adc figure updated')


    def setup(self):
        self.create_widgets()
        self.setup_layout()
        self.init_camera_first_frame()

    def create_widgets(self):
        self.figure_frame = tk.Frame(self.container, bg='#09AD4B')
        self.figure_label = Label(self.figure_frame)
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
                                                 command=self.global_timer_switch, variable=self.global_timer_status,
                                                 onvalue=True, offvalue=False)

    def setup_layout(self):
        self.figure_frame.place(relx=0.4, rely=0.07, height=480, width=640)
        self.figure_label.pack(anchor="nw")
        self.adc_checkbox.place(relx=0.005, rely=0.01, relheight=0.04, relwidth=0.047)
        self.power_switch_checkbox.place(relx=0.055, rely=0.01, relheight=0.04, relwidth=0.04)

        self.global_timer_frame.place(relx=0.1, rely=0.005, relheight=0.06, relwidth=0.11)
        self.global_timer_label.place(relx=0.05, rely=0.05, relheight=0.25, relwidth=0.9)
        self.global_timer_entry.place(relx=0.2, rely=0.5, relheight=0.35, relwidth=0.35)
        self.global_timer_sec_label.place(relx=0.6, rely=0.52, relheight=0.21, relwidth=0.15)
        self.global_timer_checkbox.place(relx=0.05, rely=0.5, relheight=0.3, relwidth=0.13)

        self.upper_motors_frame.main_frame.place(relx=0.005, rely=0.07, relheight=0.4, relwidth=0.36)
        self.upper_motors_frame.setup_layout()

        self.lower_motors_frame.main_frame.place(relx=0.005, rely=0.48, relheight=0.4, relwidth=0.36)
        self.lower_motors_frame.setup_layout()

    def rescale_frame(self, img, scale=0.3):
        width = int(img.shape[1] * scale)
        height = int(img.shape[0] * scale)
        dimensions = (width, height)
        return cv.resize(img, dimensions, interpolation=cv.INTER_AREA)

    def fit_image_into_label(self, image, rescale_flag=False, given_scale=0.5):
        if rescale_flag:
            img = self.rescale_frame(image, scale=given_scale)
        else:
            img = image
        cvimage = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        img = Image.fromarray(cvimage)
        imgtk = ImageTk.PhotoImage(image=img)
        self.figure_label.imgtk = imgtk
        self.figure_label.configure(image=imgtk)

    def init_camera_first_frame(self):
        initial_image = cv.imread('../Images/No_graph.png')
        self.fit_image_into_label(initial_image)

    def adc_figure_update(self):
        figure = cv.imread('../Images/AdcFigure.png')
        self.fit_image_into_label(figure)

    def adc_change(self):
        pub.sendMessage("Adc_switch")

    def global_timer_switch(self):
        data = self.global_timer_entry.get()
        timer_status = self.global_timer_status.get()
        if timer_status:
            if data == '':
                print('View.py - Global_timer_entry - "Setting with NO time"')
            else:
                pub.sendMessage("Global_timer_switch")
        else:
            pub.sendMessage("Global_timer_switch")

    def power_switch(self):
        pub.sendMessage("Power_switch")


if __name__ == '__main__':
    root = Tk()
    root['bg'] = '#0585e8'
    root.title('Motor Client')
    root.geometry('1600x900')
    photo = PhotoImage(file="../Images/cyber_hand.png")
    root.iconphoto(False, photo)
    root.resizable(width=False, height=False)

    view = View(root)
    view.setup()

    root.mainloop()
