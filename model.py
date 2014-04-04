class Model(object):
    step = 1
    range = 30
    startDay = 0
    startTime = 9
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
