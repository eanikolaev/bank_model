# -*- coding: utf-8 -*- 
from random import randint
class Application(object):
    num = 0 # начало нумерации заявок
    def __init__(self, duration, arrivalTime, costRange=(3000, 50000), cost=None):
        # установление стоимости заявки
        if cost == None:
            self.cost = int(self.getRandomCost(costRange))
        else:
            self.cost = cost

        Application.num += 1           
        self.num = Application.num     # установление номера заявки
        self.duration = duration       # установление продолжительности заявки
        self.arrivalTime = arrivalTime # установление времени поступления заявки


    def getRandomCost(self, (l,r) ):
        return randint(l, r)


    def setClerk(self, c):
        self.clerk = c


