from bankmodel import BankModel
from windows import MainWindow


if __name__ == '__main__':
    bm = BankModel()
    mw = MainWindow(bm)
    mw.root.mainloop()

