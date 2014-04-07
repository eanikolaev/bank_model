class Clerk(object):
    def __init__(self, num, dinnerStart, level=0, status='free'):
        self.level = level             # уровень клерка
        self.num = num                 # номер клерка
        self.dinnerStart = dinnerStart # время начала обеда клерка
        self.status = status           # статус клерка
        self.salary = self.getSalary() # генерация зарплаты клерка
        self.application = None


    def getSalary(self):
        return 2000 + 200*self.level
