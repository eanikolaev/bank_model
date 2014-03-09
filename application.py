from random import randint
class Application(object):
    def __init__(self, duration, costRange=(3000, 50000), cost=None):
        if cost == None:
            self.cost = self.getRandomCost(costRange)

        self.duration = duration


    def getRandomCost(self, (l,r) ):
        return randint(l, r)


    def setClerk(self, c):
        self.clerk = c