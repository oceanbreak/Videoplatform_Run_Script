from lib.ComPortData import ComPortData
from lib.BufferGenerator import BufferGenerator
import time

if __name__ == '__main__':
    proc1 = BufferGenerator('COM4', 9600, ['DBS'])
    proc1.repeat_writing_buffer()
    for  i in range(10):
        # print(proc1.getData())
        # print(proc1.getData() is None)
        time.sleep(1)
    proc1.stop_writing_buffer()

