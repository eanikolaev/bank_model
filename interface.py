from Tkinter import *


def openParameters():
    pass

def drawAll():
    root = Tk()
    root.wm_title("Bank modeling")
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("%dx%d+0+0" % (w, h))

    buttons = {
        'start': Button(root, text = 'Start').grid(row=3, column=5),
        'pause': Button(root, text = 'Pause', state=DISABLED).grid(row=3, column=6),
        'parameters': Button(root, text='Parameters', command=openParameters).grid(row=1, column=1),
        'exit': Button(root, text = 'Exit', command=root.destroy).grid(row=1, column=2),
        'skipday': Button(root, text = 'Skip day').grid(row=3, column=3)
    }

    labels = {
        'time': Label(root, text='21:00', font='Arial 24 bold').grid(row=1, column=3, columnspan=4),
        'stat': Label(root, text='Statistics:\n\nparameter1\nparameter2', width=40).grid(row=2, column=1, columnspan=2)
    }
    
    canvas = Canvas(root, width=1000, height=700)
    canvas.grid(row=2, column=3, columnspan=4)
    canvas.create_rectangle(0,0,999,699, fill="blue")

    slider = Scale(root, orient=HORIZONTAL, from_=0, to=30, resolution=0.2, label='Change speed', length=400, tickinterval=10)
    slider.set(1)
    slider.grid(row=3, column=4)

    return (root, buttons, labels, canvas, slider)

