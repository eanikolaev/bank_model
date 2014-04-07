# -*- coding: utf-8 -*- 
class Model(object):
    # шаг моделирования в минутах
    step = 1

    # период моделирования в днях
    range = 30

    # начальный день недели
    startDay = 0

    # час начала моделирования
    startTime = 9

    # текущее время в минутах
    time = startTime*60

    def nextStep(self):
        self.time += self.step


    def getDaysElapsed(self):
        return (self.getHoursElapsed() / 24)


    def getMinutesElapsed(self):
        return (self.time)


    def getHoursElapsed(self):
        return (self.getMinutesElapsed() / 60)


    def getCurrentTime(self):
        me = self.getMinutesElapsed() % 60
        if me < 10:
            me = '0' + str(me)
        else:
            me = str(me)

        return str(self.getHoursElapsed() % 24), me


    def getDayOfWeek(self):
        return (self.startDay + self.getDaysElapsed()) % 7


    def getNameDayOfWeek(self):
        return self.getDayName(self.getDayOfWeek())


    def getDaysBeforeFinish(self):
        return (self.range - self.getDaysElapsed() - self.startDay)


    def finished(self):
        return (self.getDaysElapsed() - self.startDay >= self.range)


    def getDayNum(self, name):
        return {
            'monday': 0,
            'tuesday': 1,
            'wednesday': 2,
            'thursday': 3,
            'friday': 4,
            'saturday': 5,
            'sunday': 6
        } [name.lower()]


    def getDayName(self, num):
        return {
            0: 'monday',
            1: 'tuesday',
            2: 'wednesday',
            3: 'thursday',
            4: 'friday',
            5: 'saturday',
            6: 'sunday'
        } [num]
