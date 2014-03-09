from model import Model
from clerk import Clerk
from queue import Queue


class BankModel(Model):
    def __init__(self,
                 arrivalRange=(0,10),
                 processingRange=(2,30),
                 clerkCount=7,
                 schedule=None,
                 dinnerRange=(12,15),
                 dinnerLen=30,
                 closeBeforeTime=-1
    ):
        self.dinnerRange = dinnerRange
        self.dinnerLen = dinnerLen
        self.arrivalRange = arrivalRange
        self.processingRange = processingRange
        self.clerkCount = clerkCount
        self.closeBeforeTime = closeBeforeTime

        if schedule == None:
            self.schedule = self.getDefaultSchedule()
        
        startDinnerTime = self.dinnerRange[0] * 60
        finishDinnerTime = (self.dinnerRange[1] * 60) - self.dinnerLen
        dinnerStep = (finishDinnerTime - startDinnerTime) / self.clerkCount
        dinnerTime = startDinnerTime
        clerks = ()
        for i in range(self.clerkCount):            
            c = Clerk(i, dinnerTime)            
            clerks += (c, )
            dinnerTime += dinnerStep

        self.clerks = clerks

    def getDefaultSchedule(self):
        s = dict( [ (i, self.getDefaultWorkDay()) for i in range(5) ] )
        s[5] = self.getDefaultShortDay()
        s[6] = self.getDefaultFreeDay()
        return s
          

    def getDefaultWorkDay(self):
        return { 'workRange': (9, 18), 'work': True, 'dinner': True }


    def getDefaultShortDay(self):
        return { 'workRange': (9, 15), 'work': True, 'dinner': False }


    def getDefaultFreeDay(self):
        return { 'work': False }

