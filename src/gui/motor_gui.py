from tkinter import *


def left_rotate():
    print('Rotate left')


def right_rotate():
    print('Rotate right')


root = Tk()

root['bg'] = '#ffffff'
root.title('Motor Client')
root.geometry('480x320')
photo = PhotoImage(file="../../Images/cyber_hand.png")
root.iconphoto(False, photo)
root.resizable(width=False, height=True)

left_rotate_button = Button(root, text='Rotate left', command=left_rotate)
left_rotate_button.place(relx=0.05, rely=0.15, relheight=0.1)

right_rotate_button = Button(root, text='Rotate right', command=right_rotate)
right_rotate_button.place(relx=0.2, rely=0.15, relheight=0.1)


root.mainloop()
