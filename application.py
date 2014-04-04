from random import randint
class Application(object):
    num = 0
    def __init__(self, duration, arrivalTime, costRange=(3000, 50000), cost=None):
        if cost == None:
            self.cost = int(self.getRandomCost(costRange))
        else:
            self.cost = cost

        Application.num += 1
        self.num = Application.num
        self.duration = duration
        self.arrivalTime = arrivalTime


    def getRandomCost(self, (l,r) ):
        return randint(l, r)


    def setClerk(self, c):
        self.clerk = c


