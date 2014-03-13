from bankmodel import BankModel
from windows import MainWindow
from Tkinter import *


def updateTime():
    global time_alarm
    time_alarm = mw.labels['time'].after(tickStep, updateTime)
    mw.labels['time']['text'] = "%s:%s" % mw.bm.getCurrentTime()
    mw.bm.nextStep()


def updateDay():
    global day_alarm
    day_alarm = mw.labels['day'].after(tickStep, updateDay)
    mw.labels['day']['text'] = mw.bm.getNameDayOfWeek()
    

def updateSpeed():
    global tickStep, speed_alarm    
    speed_alarm = mw.slider.after(tickStep, updateSpeed)
    speed = mw.slider.get()    
    tickStep = int(defaultTickStep / float(speed))


def start():
    mw.labels['time'].after_idle(updateTime)
    mw.labels['day'].after_idle(updateDay)
    mw.slider.after_idle(updateSpeed)
    mw.buttons['pause'].configure(state=NORMAL)
    mw.buttons['start'].configure(state=DISABLED)


def pause():
    global time_alarm, day_alarm, speed_alarm 
    mw.labels['time'].after_cancel(time_alarm)
    mw.labels['day'].after_cancel(day_alarm)
    mw.slider.after_cancel(speed_alarm)
    mw.buttons['pause'].configure(state=DISABLED)
    mw.buttons['start'].configure(state=NORMAL)
 

def skipDay():
    if mw.buttons['start'].cget('state') == DISABLED:
        mw.bm.time += 24*60


if __name__ == '__main__':    
    bm = BankModel()
    mw = MainWindow(bm)
    stat = {    
        'servedClients': (0, 'count of served clients'),
        'missedClients': (0, 'count of missed clients'),
        'maxQueueLen': (0, 'maximum length of queue'),
        'avgQueueLen': (0, 'average length of queue'),
        'minQueueLen': (0, 'minimum length of queue'),
        'avgTimeInQueue': (0, 'average time which client spends in queue'),
        'clerkWorkload': (0, 'average workload of clerks'),
        'profit': (0, 'bank accumulated profit')        
    }
    
    defaultTickStep = 500
    tickStep = defaultTickStep
    time_alarm = day_alarm = speed_alarm = None

    mw.buttons['start'].configure(command=start)
    mw.buttons['pause'].configure(command=pause)
    mw.buttons['skipday'].configure(command=skipDay)
    mw.labels['day']['text'] = mw.bm.getNameDayOfWeek()
    mw.labels['time']['text'] = "%s:%s" % mw.bm.getCurrentTime()
    mw.drawClerks()

    mw.root.mainloop()

