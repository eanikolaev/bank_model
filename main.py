from application import Application
from queue import Queue
from bankmodel import BankModel
from windows import MainWindow
from Tkinter import *
from random import randint


def updateTime():
    global time_alarm, stat, skipTime, waitLabel, ticks, queueLens, skipMins, skipHours, closed, closedOnEnter, skipAllFlag, progressLabel
    time_alarm = mw.labels['time'].after(tickStep, updateTime)
    mw.bm.nextStep()
    if not closed:
        ticks += 1
        calcQueueStat()
        calcClerkStat()
        if arrivalTime and arrivalTime <= mw.bm.time:
            nextApplication()
        processQueue()

    processSchedule()

    if mw.bm.finished():
        finish()
        return

    if newDayTime and newDayTime <= mw.bm.time:
        everyDay()
 
    if skipTime:
        if mw.bm.time >= (skipTime + skipMins + skipHours*60):
            mw.canvas.delete(waitLabel)
            skipTime = None
            closed = False
            closedOnEnter = False
        else:
            return

    if not skipAllFlag:
        mw.drawQueue()
        mw.drawClerks()
        mw.labels['time']['text'] = "%s:%s" % mw.bm.getCurrentTime()
        updateDay()
        updateSpeed()
        updateStat()


def processSchedule():
    global closed, closedOnEnter
    currentDay = mw.bm.getDayOfWeek()
    schedule = mw.bm.schedule[currentDay]
    next_schedule = mw.bm.schedule[(currentDay+1) % 7]
    currentHours, currentMinutes = map(int, mw.bm.getCurrentTime())
    if not schedule['work']:
        closed = True
        skip(60 - currentMinutes, 24 - currentHours - 1)

    workStartHours  = int(schedule['workRange'][0])
    workFinishHours = int(schedule['workRange'][1])

    if schedule['dinner']:
      for i in range(len(mw.bm.clerks)):
        if (mw.bm.clerks[i].dinnerStart <= currentHours*60+currentMinutes <= mw.bm.clerks[i].dinnerStart+mw.bm.dinnerLen):
            mw.bm.clerks[i].status = 'dinner'
        elif mw.bm.clerks[i].application:
            mw.bm.clerks[i].status = 'busy'
        else:
            mw.bm.clerks[i].status = 'free'

    if (currentHours < workStartHours):
        closed = True
        skip(60-currentMinutes, workStartHours-currentHours-1)
    elif (mw.bm.closeBeforeTime != -1 and 
          currentHours == workFinishHours - 1 and
          (60-currentMinutes)<=mw.bm.closeBeforeTime):
        closedOnEnter = True
    elif (currentHours >= workFinishHours):
        closed = True
        allAway()
        skip((24-currentHours)*60)


def allAway():
    global nextApp, stat
    stat['Clients']['missed'][0] += len(mw.bm.queue.apps)
    mw.bm.queue = Queue()
    Application.num = 0
    nextApp = None
    for i in range(len(mw.bm.clerks)):
        if mw.bm.clerks[i].application:
            stat['Clients']['served'][0] += 1
            stat['Others']['bank profit'][0] += mw.bm.clerks[i].application.cost
       
        mw.bm.clerks[i].application = None
        mw.bm.clerks[i].status = 'free'


def updateDay():
    mw.labels['day']['text'] = mw.bm.getNameDayOfWeek()
    

def updateSpeed():
    global tickStep    
    speed = mw.slider.get()    
    tickStep = int(defaultTickStep / float(speed))


def updateStat():
    mw.labels['stat'].configure(text=getReadableStat(stat))


def nextApplication():
    global arrivalTime, nextApp, stat, appsCount, closed, closedOnEnter
    
    if nextApp and not closed:
        if len(mw.bm.queue.apps) < mw.bm.queue.maxLen and not closedOnEnter:
            if (len(mw.bm.queue.apps) > mw.bm.queue.threshold and not randint(0,3)):
                pass
            else:
                mw.bm.queue.push(nextApp)
                if not skipTime and not skipAllFlag:
                    mw.drawQueue()
        else:
            stat['Clients']['missed'][0] += 1

    duration = mw.bm.getNextAppProcessingTime()
    cost = mw.bm.getNextAppCost()
    arrivalTime = mw.bm.time + mw.bm.getNextAppArrivalTime()
    nextApp = Application(cost=cost, duration=duration, arrivalTime=mw.bm.time)
    appsCount += 1



def everyDay():
    global newDayTime, stat
    currentDay = mw.bm.getDayOfWeek()
    schedule = mw.bm.schedule[currentDay]
    if schedule['work']:
        for c in mw.bm.clerks:
            if c.status != 'away':
                stat['Others']['bank profit'][0] -= c.salary

    for k in range(mw.bm.clerkCount):
        if mw.bm.clerks[k].status == 'away':
            mw.bm.clerks[k].status = 'free'

    if not randint(0,6):
        k = randint(0, mw.bm.clerkCount-1)
        mw.bm.clerks[k].status = 'away'

    newDayTime += 24*60


def getReadableStat(stat):
    s = 'Statistics:\n\n'
    for key in sorted(stat):
        s += key + '\n'
        for p in sorted(stat[key]):
            value = str(stat[key][p][0])
            if p == 'clerk workload':
                value += '%'
            s += p + ': ' + value + '\n'
        s += '\n'

    return s


def init():
    mw.labels['time'].after_idle(updateTime)


def stop():
    mw.labels['time'].after_cancel(time_alarm)


def finish():
    global waitLabel, progressLabel
    allAway()
    mw.updateAll()
    updateStat()
    stop()    
    mw.drawInformation()
    mw.buttons['stop'].configure(state=DISABLED)
    mw.buttons['start'].configure(state=NORMAL)
    mw.buttons['pause'].configure(text='Pause')
    mw.buttons['pause'].configure(state=DISABLED)
    mw.buttons['skipday'].configure(state=DISABLED)
    mw.buttons['skiphour'].configure(state=DISABLED)
    mw.buttons['skipall'].configure(state=DISABLED)
    mw.readOnly = False
    skipAllFlag = False
    if waitLabel:
        mw.canvas.delete(waitLabel)

    progressLabel = waitLabel = None
    

def processQueue():
    global allTimeAtQueue
    for i in range(len(mw.bm.clerks)):
        if mw.bm.clerks[i].status == 'free' and mw.bm.queue.apps:                
            mw.bm.clerks[i].application = mw.bm.queue.pop()
            mw.bm.clerks[i].application.duration *= ((mw.bm.clerkCount+10) / float(mw.bm.clerks[i].level+1+10))
            mw.bm.clerks[i].status = 'busy' 
            mw.bm.clerks[i].appTime = mw.bm.time
            allTimeAtQueue += (mw.bm.time - mw.bm.clerks[i].application.arrivalTime)
            stat['Others']['average time in queue'][0] = allTimeAtQueue / appsCount
            mw.drawInformation(mw.bm.clerks[i].application.num, mw.bm.clerks[i].num)

        elif mw.bm.clerks[i].application:
            if mw.bm.time >= mw.bm.clerks[i].appTime + mw.bm.clerks[i].application.duration:
                stat['Clients']['served'][0] += 1
                stat['Others']['bank profit'][0] += mw.bm.clerks[i].application.cost
                if mw.bm.clerks[i].status == 'busy':
                    mw.bm.clerks[i].status = 'free'
                mw.bm.clerks[i].application = None
                mw.bm.clerks[i].appTime = 0


def calcQueueStat():
    global queueLens
    curQueueLen = len(mw.bm.queue.apps)
    if curQueueLen < stat['Queue length']['minimum'][0]:
        stat['Queue length']['minimum'][0] = curQueueLen
    elif curQueueLen > stat['Queue length']['maximum'][0]:
        stat['Queue length']['maximum'][0] = curQueueLen

    queueLens += curQueueLen
    stat['Queue length']['average'][0] = queueLens / ticks


def calcClerkStat():
    global clerkAtWorkCount, clerkAllCount
    clerkAllCount += len(mw.bm.clerks)
    for c in mw.bm.clerks:
        if c.status == 'busy':
            clerkAtWorkCount += 1

    stat['Others']['clerk workload'][0] = clerkAtWorkCount*100/clerkAllCount
     

def start():
    global tickStep, time_alarm, arrivalTime, nextApp, skipTime, waitLabel, \
           ticks, queueLens, appsCount, allTimeAtQueue, newDayTime, \
           clerkAtWorkCount, clerkAllCount, closed, closedOnEnter, skipAllFlag, \
           progressLabel
    
    tickStep = defaultTickStep
    time_alarm = None
    arrivalTime = nextApp = None
    skipTime = None
    skipAllFlag = False
    skipMins = skipHours = 0
    ticks = 0
    appsCount = 0
    queueLens = 0
    closed = closedOnEnter = False
    clerkAtWorkCount = clerkAllCount = 0
    allTimeAtQueue = 0
    if waitLabel:
        mw.canvas.delete(waitLabel)
    waitLabel = None
    progressLabel = None

    init()
    initStat()
    mw.bm.time = mw.bm.startTime*60
    newDayTime = mw.bm.time + 24*60
    mw.buttons['pause'].configure(state=NORMAL)
    mw.buttons['pause'].configure(text='Pause')
    mw.buttons['start'].configure(state=DISABLED)
    mw.buttons['stop'].configure(state=NORMAL)
    mw.buttons['skipday'].configure(state=NORMAL)
    mw.buttons['skiphour'].configure(state=NORMAL)
    mw.buttons['skipall'].configure(state=NORMAL)
    mw.bm.clear()
    mw.updateAll()
    mw.readOnly = True
    nextApplication()
    

def pause():
    global time_alarm, day_alarm, speed_alarm 
    if mw.buttons['pause'].cget('text') == 'Pause':
        mw.buttons['pause'].configure(text='Continue')
        stop()

    else:
        mw.buttons['pause'].configure(text='Pause')
        init()
        
 
def initStat():
    global stat
    for s in stat:
        for ss in stat[s]:
            stat[s][ss][0] = 0


def skip(mins, hours=0):
    global skipTime, tickStep, waitLabel, skipMins, skipHours
    if skipTime: return
    if waitLabel: mw.canvas.delete(waitLabel)
    if not skipAllFlag:
        waitLabel = mw.canvas.create_text(450, 300, text='Please, wait...', font='Arial 30 bold')
    skipTime = mw.bm.time
    skipMins = mins
    skipHours = hours
    tickStep = 0


def skipDay():
    allAway()
    skip(0, 24-int(mw.bm.getCurrentTime()[0]))


def skipHour():
    allAway()
    skip(0, 1)


def skipAll():
    global skipAllFlag, tickStep, waitLabel
    allAway()
    skipAllFlag = True
    tickStep = 0
    waitLabel = mw.canvas.create_text(450, 300, text='Please, wait...', font='Arial 30 bold')


if __name__ == '__main__':    
    bm = BankModel()
    mw = MainWindow(bm)
    stat = {    
        'Clients': {
            'served': [0, 'count of served clients'],
            'missed': [0, 'count of missed clients'],
         },
        'Queue length': {
            'maximum': [0, 'maximum length of queue'],
            'average': [0, 'average length of queue'],
            'minimum': [0, 'minimum length of queue'],
         },
         'Others': {
            'average time in queue': [0, 'average time which client spends in queue'],
            'clerk workload': [0, 'average workload of clerks'],
            'bank profit': [0, 'bank accumulated profit']        
         }
    }
    waitLabel = None
    defaultTickStep = 500

    mw.buttons['start'].configure(command=start)
    mw.buttons['pause'].configure(command=pause)
    mw.buttons['stop'].configure(command=finish)
    mw.buttons['skipday'].configure(command=skipDay)
    mw.buttons['skiphour'].configure(command=skipHour)
    mw.buttons['skipall'].configure(command=skipAll)
    mw.labels['day']['text'] = mw.bm.getNameDayOfWeek()
    mw.labels['time']['text'] = "%s:%s" % mw.bm.getCurrentTime()
    mw.labels['stat'].after_idle(updateStat)
    mw.drawClerks()
    mw.drawInformation()

    mw.root.mainloop()


