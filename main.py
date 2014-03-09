from bankmodel import BankModel
from interface import drawAll


if __name__ == '__main__':
    bm = BankModel()
    (root, buttons, labels, canvas, slider) = drawAll()
    root.mainloop()

