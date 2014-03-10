from bankmodel import BankModel
from interface import MainWindow


if __name__ == '__main__':
    bm = BankModel()
    mw = MainWindow(bm)
    mw.root.mainloop()

