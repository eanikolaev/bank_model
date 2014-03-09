class Queue(object):
    def __init__(self, maxLen=15, threshold=7):
        self.apps = []
        self.maxLen = maxLen
        self.threshold = threshold


    def push(self, x):
        self.apps.append(x)


    def pop(self):
        return self.apps.pop()
