from model import Model
from clerk import Clerk
from queue import Queue
from numpy.random import uniform
from application import Application


class BankModel(Model):
    def __init__(self,
                 arrivalRange=[0,5],
                 processingRange=[0,25],
                 clerkCount=5,
                 schedule=None,
                 dinnerRange=[12,15],
                 dinnerLen=30,
                 costRange=[5, 3000],
                 closeBeforeTime=20
    ):
        self.dinnerRange = dinnerRange
        self.dinnerLen = dinnerLen
        self.arrivalRange = arrivalRange
        self.processingRange = processingRange
        self.clerkCount = clerkCount
        self.closeBeforeTime = closeBeforeTime
        self.costRange = costRange
        self.queue = Queue()

        if schedule == None:
            self.schedule = self.getDefaultSchedule()
        
        startDinnerTime = self.dinnerRange[0] * 60
        finishDinnerTime = (self.dinnerRange[1] * 60) - self.dinnerLen
        dinnerStep = (finishDinnerTime - startDinnerTime) / self.clerkCount
        dinnerTime = startDinnerTime
        clerks = []
        for i in range(self.clerkCount):            
            c = Clerk(i+1, dinnerTime)            
            clerks.append(c)
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
        return { 'work': False, 'workRange': (9, 18), 'dinner': True}


    def getNextAppArrivalTime(self):
        day = self.getDayOfWeek() + 1
        hour = int(self.getCurrentTime()[0])
        end = int(self.schedule[day]['workRange'][1])
        k = 5 / (9 *(hour/float(end) + day/18.0))
        l = self.arrivalRange[0]
        r = int(k*self.arrivalRange[1])
        if r < l: r = l+1
        return uniform(l, r)


    def getNextAppCost(self):
        return int(uniform(self.costRange[0], self.costRange[1]))


    def getNextAppProcessingTime(self):
        return uniform(self.processingRange[0], self.processingRange[1])


    def allAway(self):
        for c in self.clerks:
           c.application = None
           c.status = 'free'
        self.queue.apps = []


    def clear(self):
        Application.num = 0 
        self.queue = Queue()
        for c in self.clerks:
            c.application = None
            c.status = 'free'
