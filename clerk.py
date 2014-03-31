class Clerk(object):
    def __init__(self, num, dinnerStart, level=0, status='free'):
        self.level = level
        self.num = num
        self.dinnerStart = dinnerStart
        self.status = status
        self.salary = self.getSalary()
        self.application = None


    def getSalary(self):
        return 2000 + 200*self.level
