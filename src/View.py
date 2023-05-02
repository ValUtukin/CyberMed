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

    def setup_layout(self):
        self.figure_frame.place(relx=0.4, rely=0.01, height=480, width=640)
        self.figure_label.pack(anchor="nw")

        self.upper_motors_frame.main_frame.place(relx=0.005, rely=0.01, height=340, width=600)
        self.upper_motors_frame.setup_layout()

        self.lower_motors_frame.main_frame.place(relx=0.005, rely=0.4, height=340, width=600)
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
