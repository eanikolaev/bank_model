from model import Model
from clerk import Clerk


class BankModel(Model):
    def __init__(self,
                 arrivalRange=(0,10),
                 processingRange=(2,30),
                 clerkCount=7,
                 schedule=None,
                 closeBeforeTime=-1
    ):
        if schedule == None:
            self.schedule = self.getDefaultSchedule()

        


    def getDefaultSchedule(self):
        s = dict( [ (i, self.getDefaultWorkDay()) for i in range(5) ] )
        s[5] = self.getDefaultShortDay()
        s[6] = self.getDefaultFreeDay()
        return s
          

    def getDefaultWorkDay(self):
        return { 'workRange': (9, 18), 'dinnerRange': (12, 15), 'work': True, 'dinner': True }


    def getDefaultShortDay(self):
        return { 'workRange': (9, 15), 'work': True, 'dinner': False }


    def getDefaultFreeDay(self):
        return { 'work': False }

