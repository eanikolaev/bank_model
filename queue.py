class Queue(object):
    def __init__(self, maxLen=15, threshold=7):
        self.apps = []             # список заявок
        self.maxLen = maxLen       # максимальная длина очереди
        self.threshold = threshold # порог очереди (клиенты начинают уходить)


    def push(self, x):
        self.apps.append(x)


    def pop(self):
        if self.apps:
            el = self.apps[0]
            self.apps = self.apps[1:]
            return el
        else:
            return None
