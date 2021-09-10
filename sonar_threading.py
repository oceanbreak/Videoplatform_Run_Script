""" Custom threading module for user defined functions """

import threading

class SonarThread(threading.Thread):
    """
    The class takes user defined function as an argument and creates thread that executes it repeatedly after .start()
    while stop() method is not applied.
    """
    def __init__(self, custom_func, parameters=[]):
        super(SonarThread, self).__init__()
        self._stop = threading.Event()
        self.customFunc = custom_func
        self.parameters = parameters

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        while not self.stopped():
            self.customFunc(*self.parameters)

if __name__ == '__main__':

    import random, time

    def userFunc(x):
        print("I'm usrer func and generating %i number and word %s" % (random.randint(1,10), x))

    proc1 = SonarThread(userFunc, ['tesetword'])
    proc1.start()
    time.sleep(10)
    proc1.stop()
    print('Program Sropped')