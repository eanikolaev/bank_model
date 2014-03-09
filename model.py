class Model(object):
    def __init__(self, step=10, range=30, startDay=0, startTime=9*60):
        self.step      = step
        self.range     = range
        self.day       = startDay
        self.startTime = startTime
        self.time      = self.startTime


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

