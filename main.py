from lib.data.ComPortData import ComPortData
from lib.data.BufferGenerator import BufferGenerator
import time
from lib.data.DataStructure import CoordinatesData, DepthData
from lib.data.NmeaParser import NmeaParser


a = DepthData(17.642)
print(a)


if __name__ == '__main__':
    proc1 = BufferGenerator('COM4', 9600, ['DBS'])
    proc2 = BufferGenerator('COM13', 9600, ['GGA', 'RMC'])
    proc3 = BufferGenerator('COM10', 57600, ['DBT'])
    parser = NmeaParser()

    proc1.repeat_writing_buffer()
    proc2.repeat_writing_buffer()
    proc3.repeat_writing_buffer()

    for i in range(30):
        a = proc1.getData()
        b= proc2.getData()
        c= proc3.getData()

        if a is not None:
            depth = parser.parseDBS(a[0])
            print(depth)

        if b is not None:
            coord = parser.parseGGA(b[0])
            print(coord)
            print(coord.deg_min())

        if c is not None:
            altimeter = parser.parseDBT(c[0])
            print(altimeter)

        print('Waiting for data')
        # try:
        #     coord = NmeaParser.parseGGA(a[0])
        #     print(coord)
        # except (TypeError, AttributeError):
        #     pass
        time.sleep(1)

    # for  i in range(10):
    #     # print(proc1.getData())
    #     # print(proc1.getData() is None)
    #     time.sleep(1)
    proc1.stop_writing_buffer()
    proc2.stop_writing_buffer()
    proc3.stop_writing_buffer()

