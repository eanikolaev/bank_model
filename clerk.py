class Clerk(object):
    def __init__(self, num, dinnerRange, level=0, status='free'):
        self.level = level
        self.num = num
        self.dinnerRange = dinnerRange
        self.status = status
        self.salary = self.getSalary()


    def getSalary(self):
        return 2000 + 200*self.level
