from Tkinter import *
import tkMessageBox
import time

class MainWindow(object):
    def __init__(self, bankmodel):
        self.root = Tk()
        self.root.wm_title("Bank modeling")
        w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry("%dx%d+0+0" % (w, h))
        self.bm = bankmodel

        self.drawButtons() 
        self.drawLabels()
        self.drawCanvas()
        self.drawSlider()
        self.clients = []
        self.clerks = []
        self.readOnly = False


    def updateAll(self):
        self.labels['time']['text'] = "%s:%s" % self.bm.getCurrentTime()
        self.labels['day']['text'] = self.bm.getNameDayOfWeek()
        self.drawQueue()
        self.drawClerks()


    def drawButtons(self):
        self.buttons = {
            'start': Button(self.root, text = 'Start'),
            'pause': Button(self.root, text = 'Pause', state=DISABLED),
            'stop': Button(self.root, text = 'Stop', state=DISABLED),
            'parameters': Button(self.root, text='Parameters', command=self.popupParameters),
            'exit': Button(self.root, text = 'Exit', command=self.root.destroy),
            'skipday': Button(self.root, text = 'Skip day'),
            'schedule': Button(self.root, text = 'Schedule', command=self.popupSchedule)
        }

        self.buttons['schedule'].grid(row=1, column=1)
	self.buttons['parameters'].grid(row=1, column=2)
        self.buttons['exit'].grid(row=1, column=3)
        self.buttons['skipday'].grid(row=3, column=4)
        self.buttons['start'].grid(row=3, column=6)
        self.buttons['pause'].grid(row=3, column=7)
        self.buttons['stop'].grid(row=3, column=8)


    def drawLabels(self):
        self.labels = {
            'time': Label(self.root, text='21:00', font='Arial 24 bold'),
            'day': Label(self.root, text='monday', font='Arial 24 bold', width=12),
            'stat': Label(self.root, text='', width=30, font='Arial 16 bold')
        }

        self.labels['time'].grid(row=1, column=5, columnspan=1)
        self.labels['day'].grid(row=1, column=4, columnspan=1)
        self.labels['stat'].grid(row=2, column=1, columnspan=3)
 

    def drawCanvas(self):
        self.canvas = Canvas(self.root, width=1000, height=700)
        self.canvas.grid(row=2, column=4, columnspan=5)
        self.canvas.create_rectangle(0, 0, 999, 699, fill="lemon chiffon")


    def drawSlider(self):
        self.slider = Scale(self.root, orient=HORIZONTAL, from_=0.1, to=10, resolution=0.1, label='Change speed', length=350, tickinterval=0)
        self.slider.set(1)
        self.slider.grid(row=3, column=5)


    def drawClerks(self):
        self.clearClerks()
        clerkCount = self.bm.clerkCount
        step = int(self.canvas.cget('width')) / clerkCount
        pos = step/2
        for i in range(clerkCount):
            self.drawClerk(self.bm.clerks[i], pos)
            pos += step            


    def drawClerk(self, clerk, pos, up=20, down=45):
        self.clerks.append(self.canvas.create_text(pos, up-10, text='Clerk ' + str(clerk.num)))
        if clerk.status == 'busy':
            self.clerks.append(self.canvas.create_rectangle(pos-20, up, pos+20, down, fill="red"))
        elif clerk.status == 'free':
	    self.clerks.append(self.canvas.create_rectangle(pos-20, up, pos+20, down, fill="lime green"))
        elif clerk.status == 'dinner':
	    self.clerks.append(self.canvas.create_rectangle(pos-20, up, pos+20, down, fill="yellow"))
        else:
	    self.clerks.append(self.canvas.create_rectangle(pos-20, up, pos+20, down, fill="steel blue"))
        
        if clerk.application:
            for c in self.drawClient(clerk.application.num, pos, down+25, 20, 20):
                self.clerks.append(c)


    def drawQueue(self, startx=50):
        self.clearQueue()
        y = 500
        x = startx
        for a in self.bm.queue.apps:
            self.pushToQueue(self.drawClient(a.num, x, y, 20, 20))
            x += 50


    def drawClient(self, i, x, y, sizex, sizey):
        res = []
        res.append(self.canvas.create_rectangle(x, y, x+sizex, y+sizey, fill='tomato'))
        res.append(self.canvas.create_text(x, y+sizey+10, text=str(i)))
        return res


    def pushToQueue(self, clients):
        for c in clients:
             self.clients.append(c)


    def clearQueue(self):
        for c in self.clients:
            self.canvas.delete(c)
        self.clients = []


    def clearClerks(self):
        for c in self.clerks:
            self.canvas.delete(c)
        self.clerks = []



    def popupParameters(self):
        self.pw = ParametersWindow(self.root, self.bm, self)
        self.root.wait_window(self.pw.top)


    def popupSchedule(self):
        self.sw = ScheduleWindow(self.root, self.bm, self)
        self.root.wait_window(self.sw.top)


class ParametersWindow(object):
    def __init__(self, root, bm, mw):
        self.top = Toplevel(root)
        self.labels = {}
        self.entries = {}
        self.buttons = {}
        self.bm = bm
        self.mw = mw
       
        self.parameters = [
            ['Set modeling range (in days)', [ ['range', 'range', None] ], 2],
            ['Set modeling step (in minutes)', [ ['step', 'step', None] ], 2],
            ['Set start day of week', [ ['startDay', 'startDay', None] ], 2],
            ['Set start time (in hours)' , [ ['startTime', 'startTime', None] ], 2],
            ['Set the number of clerks' , [['clerkCount', 'clerkCount', None] ], 2],
            ['Set boundaries of time between 2 applications (in minutes)', [ ['arrivalLeft', 'arrivalRange', '0'] , 
                                                                             ['arrivalRight', 'arrivalRange', '1'] ], 2],
            ['Set boundaries of application processing time (in minutes)', [ ['processingLeft', 'processingRange', '0'],
                                                                             ['processingRight','processingRange', '1'] ], 2],
            ['Set boundaries of dinner time (in hours)' , [['dinnerStart', 'dinnerRange', '0'], 
                                                           ['dinnerFinish', 'dinnerRange','1'] ], 2],
            ['Set time when bank should be closed to enter\n(in minutes before official close time)' , [['beforeTime', 'closeBeforeTime', None] ], 3],
            ['Set boundaries of application cost' , [['costMin', 'costRange', '0'],
                                                                               ['costMax', 'costRange', '1']
                                                                              ], 2],
            ['Set max length of queue' , [['maxLen', 'maxLen', 'queue'] ], 2],
            ['Set threshold of queue' , [['threshold', 'threshold', 'queue'] ], 2],
        ]

        self.drawParameters()        


    def drawParameter(self, name, row, var=""):
        self.labels[name] = Label(self.top, text=name, font='Arial 10 bold')
        self.labels[name].grid(row=row, column=1)

        self.entries[name] = Entry(self.top)
        self.entries[name].grid(row=row, column=2)

        self.entries[name].delete(0, END)
        self.entries[name].insert(0, str(var))


    def drawParameters(self):
        i = 0
        for label, params, height in self.parameters:
            self.drawLabel(label, i, height=height)

            i += 1
            for name, var, rest in params:
                val = None
                if rest:
                    if rest == 'queue':
                        val = getattr(self.bm.queue, var)
                    else:
                        val = getattr(self.bm, var)[int(rest)]
                else:
                    val = getattr(self.bm, var)

                self.drawParameter(name, i, val)
                i += 1
        self.drawOkCancel(i)


    def saveParameters(self):
        for label, params, height in self.parameters:
            for name, var, rest in params:
                if rest:
                    if rest == 'queue':
                        setattr(self.bm.queue, var, int(self.entries[name].get()))
                    else:
                        getattr(self.bm, var)[int(rest)] = int(self.entries[name].get())
                else:
                    setattr(self.bm, var, int(self.entries[name].get()))
        self.bm.time = self.bm.startTime*60


    def drawLabel(self, name, row, height=2):
        Label(self.top, text=name, height=height).grid(row=row, column=1, columnspan=2)


    def drawOkCancel(self, row):
        self.buttons['ok'] = Button(self.top, text='Ok',command=self.saveAndExit)        
        self.buttons['ok'].grid(row=row, column=1)

        self.buttons['cancel'] = Button(self.top, text='Cancel',command=self.cancel)
        self.buttons['cancel'].grid(row=row, column=2)

        if self.mw.readOnly:
            self.buttons['ok'].configure(state=DISABLED)

    
    def cancel(self):
        self.top.destroy()


    def saveAndExit(self):        
        try:
            self.saveParameters()
            self.mw.updateAll()
            self.top.destroy()            

        except ValueError:
            tkMessageBox.showwarning("Error", "Invalid parameters!", parent=self.top)


class ScheduleWindow(object):
    def __init__(self, root, bm, mw):
        self.top = Toplevel(root)
        self.mw = mw
        self.drawSchedule(bm)


    def drawSchedule(self, bm):
        Label(self.top, text='Day', font='Arial 10 bold').grid(row=1, column=1)
        Label(self.top, text='work', font='Arial 10 bold').grid(row=1, column=2)
        Label(self.top, text='start', font='Arial 10 bold').grid(row=1, column=3)
        Label(self.top, text='finish', font='Arial 10 bold').grid(row=1, column=4)
        Label(self.top, text='dinner', font='Arial 10 bold').grid(row=1, column=5)
        self.bm = bm
        self.entries = {}
        self.buttons = {}
        self.checkbuttons = {}

        for i in range(7):
            Label(self.top, text=bm.getDayName(i), font='Arial 10 bold').grid(row=(i+2), column=1)
            self.drawCheckbutton('work', i+2, 2, i, bm.schedule[i]['work'])
            self.drawEntry('start', i+2, 3, i, bm.schedule[i]['workRange'][0])
            self.drawEntry('finish', i+2, 4, i, bm.schedule[i]['workRange'][1])
            self.drawCheckbutton('dinner', i+2, 5, i, bm.schedule[i]['dinner'])

        self.drawOkCancel(i+3)

 
    def drawEntry(self, name, row, column, i, var=""):
        self.entries[name+str(i)] = Entry(self.top)
        self.entries[name+str(i)].grid(row=row, column=column)

        self.entries[name+str(i)].delete(0, END)
        self.entries[name+str(i)].insert(0, str(var))


    def drawCheckbutton(self, name, row, column, i, val=0):
        self.checkbuttons[name+str(i)] = IntVar()
        cb = Checkbutton(self.top, text='', variable=self.checkbuttons[name+str(i)])
        if val: cb.select()
        cb.grid(row=row, column=column)
        

    def drawOkCancel(self, row):
        self.buttons['ok'] = Button(self.top, text='Ok',command=self.saveAndExit)
        self.buttons['ok'].grid(row=row, column=1, columnspan=2)

        self.buttons['cancel'] = Button(self.top, text='Cancel',command=self.cancel)
        self.buttons['cancel'].grid(row=row, column=3, columnspan=2)

        if self.mw.readOnly:
            self.buttons['ok'].configure(state=DISABLED)


    def validate(self):
        for i in range(7):
            if self.checkbuttons['work'+str(i)].get():
                l = int(self.entries['start'+str(i)].get())
                r = int(self.entries['finish'+str(i)].get())
                if l > r or l < 0 or r > 24:
                   return False   
        return True


    def saveParameters(self):
        for i in range(7):
            self.bm.schedule[i]['work'] = self.checkbuttons['work'+str(i)].get()
            if self.bm.schedule[i]['work']:
                self.bm.schedule[i]['dinner'] = self.checkbuttons['dinner'+str(i)].get()
                self.bm.schedule[i]['workRange'] = (int(self.entries['start'+str(i)].get()), int(self.entries['finish'+str(i)].get()))


    def saveAndExit(self):        
        try:
            if self.validate():
                self.saveParameters()                
                self.top.destroy()
            else:
                raise ValueError

        except ValueError:
            tkMessageBox.showwarning("Error", "Invalid parameters!", parent=self.top)


    def cancel(self):
        self.top.destroy()


