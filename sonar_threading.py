""" Custom threading module for user defined functions """

import threading

class SonarThread(threading.Thread):
    """
    The class takes user defined function as an argument and creates thread that executes it repeatedly after .start()
    while stop() method is not applied.
    """
    def __init__(self, custom_func):
        super(SonarThread, self).__init__()
        self._stop = threading.Event()
        self.customFunc = custom_func

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        while not self.stopped():
            self.customFunc()

if __name__ == '__main__':

    import random, time

    def userFunc():
        print("I'm usrer func and generating %i number" % random.randint(1,10))

    proc1 = SonarThread(userFunc)
    proc1.start()
    time.sleep(10)
    proc1.stop()
    print('Program Sropped')