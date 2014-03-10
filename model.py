class Model(object):
    step = 10
    range = 30
    startDay = 0
    startTime = 9
    time = startTime


    def nextStep(self):
        self.time += self.step


    def getDaysElapsed(self):
        return (self.getHoursElapsed() / 24)


    def getMinutesElapsed(self):
        return (self.time - self.startTime)


    def getHoursElapsed(self):
        return (self.getMinutesElapsed() / 60)


    def getDayOfWeek(self):
        return (self.startDay + self.getDaysElapsed()) % 7


    def finished(self):
        return (self.getDaysElapsed() >= self.range)


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


    def getDayName(self):
        return {
            0: 'monday',
            1: 'tuesday',
            2: 'wednesday',
            3: 'thursday',
            4: 'friday',
            5: 'saturday',
            6: 'sunday'
        } [self.getDayOfWeek()]
