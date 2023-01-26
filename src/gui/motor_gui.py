from tkinter import *
import src.comports as comport


def left_rotate():
    print('Rotate left')


def right_rotate():
    print('Rotate right')


def get_bytestring():
    bytestring = str(bytestring_entry.get())
    warning_label = Label(root, text='8 bits!', background='#f65e05', font=('Arial', 10))
    if len(bytestring) == 8:
        for i in range(0, 8):
            if bytestring[i] in '01':
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
            comport.main(bytestring)
    else:
        warning_label.place(relx=0.81, rely=0.01, relheight=0.056, relwidth=0.15)


root = Tk()

root['bg'] = '#0585e8'
root.title('Motor Client')
root.geometry('480x320')
photo = PhotoImage(file="../../Images/cyber_hand.png")
root.iconphoto(False, photo)
root.resizable(width=False, height=True)

# left_rotate_button = Button(root, text='Rotate left', command=left_rotate)
# left_rotate_button.place(relx=0.05, rely=0.15, relheight=0.1)
#
# right_rotate_button = Button(root, text='Rotate right', command=right_rotate)
# right_rotate_button.place(relx=0.2, rely=0.15, relheight=0.1)

bytestring_label = Label(root, text='Enter byte string e.g. "00110110" (7 <= 0)', background='#b8dffe', font=('Arial', 10))
bytestring_label.place(relx=0.01, rely=0.01, relheight=0.05)

bytestring_entry = Entry()
bytestring_entry.place(relx=0.54, rely=0.01, relheight=0.05, relwidth=0.15)

bytestring_button = Button(root, text='Send', command=get_bytestring)
bytestring_button.place(relx=0.7, rely=0.01, relheight=0.056, relwidth=0.1)

root.mainloop()
