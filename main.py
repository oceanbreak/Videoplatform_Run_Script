from lib.data.ComPortData import ComPortData
from lib.data.BufferGenerator import BufferGenerator
import time
from lib.data.DataStructure import CoordinatesData, DepthData


a = DepthData(17.642)
print(a)


if __name__ == '__main__':
    proc1 = BufferGenerator('COM4', 9600, ['DBS'])
    proc2 = BufferGenerator('COM13', 9600, ['GGA', 'RMC'])

    proc1.repeat_writing_buffer()
    proc2.repeat_writing_buffer()

    for i in range(30):
        a = proc1.getData()
        b= proc2.getData()
        try:
            print(f'GPS: {b[0].split(",")[1:6]}')
            print(f'Depth: {a[0].split(",")[3:5]}')
        except TypeError:
            pass
        time.sleep(1)

    # for  i in range(10):
    #     # print(proc1.getData())
    #     # print(proc1.getData() is None)
    #     time.sleep(1)
    proc1.stop_writing_buffer()
    proc2.stop_writing_buffer()

