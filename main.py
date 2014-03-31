from application import Application
from bankmodel import BankModel
from windows import MainWindow
from Tkinter import *


def updateTime():
    global time_alarm, stat, skipTime, waitLabel
    time_alarm = mw.labels['time'].after(tickStep, updateTime)
    mw.bm.nextStep()
    if arrivalTime and arrivalTime <= mw.bm.time:
        nextApplication()

    if mw.bm.finished():
        finish()
        return
    
    for i in range(len(mw.bm.clerks)):
        if mw.bm.clerks[i].status == 'free' and mw.bm.queue.apps:                
            mw.bm.clerks[i].application = mw.bm.queue.pop()
            mw.bm.clerks[i].status = 'busy' 
            mw.bm.clerks[i].appTime = mw.bm.time

        elif mw.bm.clerks[i].status == 'busy':
            if mw.bm.time >= mw.bm.clerks[i].appTime + mw.bm.clerks[i].application.duration:
                stat['Clients']['served'][0] += 1
                mw.bm.clerks[i].status = 'free'
                mw.bm.clerks[i].application = None
                mw.bm.clerks[i].appTime = 0
 
    if skipTime:
        if mw.bm.time >= (skipTime + 24*60):
            mw.canvas.delete(waitLabel)
            skipTime = None
        else:
            return

    mw.drawQueue()
    mw.drawClerks()
    mw.labels['time']['text'] = "%s:%s" % mw.bm.getCurrentTime()
    updateDay()
    updateSpeed()
    updateStat()
       

def updateDay():
    mw.labels['day']['text'] = mw.bm.getNameDayOfWeek()
    

def updateSpeed():
    global tickStep    
    speed = mw.slider.get()    
    tickStep = int(defaultTickStep / float(speed))


def updateStat():
    mw.labels['stat'].configure(text=getReadableStat(stat))


def nextApplication():
    global arrivalTime, nextApp, stat
    
    if nextApp:
        if len(mw.bm.queue.apps) < mw.bm.queue.maxLen:            
            mw.bm.queue.push(nextApp)
            if not skipTime:
                mw.drawQueue()
        else:
            stat['Clients']['missed'][0] += 1

    duration = mw.bm.getNextAppProcessingTime()
    cost = mw.bm.getNextAppCost()
    arrivalTime = mw.bm.time + mw.bm.getNextAppArrivalTime()
    nextApp = Application(cost=cost, duration=duration)


def getReadableStat(stat):
    s = 'Statistics:\n\n'
    for key in sorted(stat):
        s += key + '\n'
        for p in sorted(stat[key]):
            s += p + ': ' + str(stat[key][p][0]) + '\n'
        s += '\n'

    return s


def init():
    mw.labels['time'].after_idle(updateTime)


def stop():
    mw.labels['time'].after_cancel(time_alarm)


def finish():
    stop()
    mw.buttons['stop'].configure(state=DISABLED)
    mw.buttons['start'].configure(state=NORMAL)
    mw.buttons['pause'].configure(text='Pause')
    mw.buttons['pause'].configure(state=DISABLED)
    mw.readOnly = False
    

def start():
    global tickStep, time_alarm, arrivalTime, nextApp, skipTime, waitLabel
    tickStep = defaultTickStep
    time_alarm = None
    arrivalTime = nextApp = None
    skipTime = None
    if waitLabel:
        mw.canvas.delete(waitLabel)
    waitLabel = None

    init()
    initStat()
    mw.bm.time = mw.bm.startTime*60
    mw.buttons['pause'].configure(state=NORMAL)
    mw.buttons['pause'].configure(text='Pause')
    mw.buttons['start'].configure(state=DISABLED)
    mw.buttons['stop'].configure(state=NORMAL)
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


def skipDay():
    global skipTime, tickStep, waitLabel
    waitLabel = mw.canvas.create_text(450, 300, text='Please, wait...', font='Arial 30 bold')
    skipTime = mw.bm.time
    tickStep = 0


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
    mw.labels['day']['text'] = mw.bm.getNameDayOfWeek()
    mw.labels['time']['text'] = "%s:%s" % mw.bm.getCurrentTime()
    mw.labels['stat'].after_idle(updateStat)
    mw.drawClerks()

    mw.root.mainloop()

