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
    parser = NmeaParser()

    proc1.repeat_writing_buffer()
    proc2.repeat_writing_buffer()

    for i in range(30):
        a = proc1.getData()
        b= proc2.getData()
        if b is not None:
            if b[0] is not None:
                coord = parser.parseGGA(b[0])
                print()
                print(coord.degrees())
                print(coord.deg_min())
                print()
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

