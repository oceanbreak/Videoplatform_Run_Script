from lib.data.ComPortData import ComPortData
from lib.data.BufferGenerator import BufferGenerator, BufferConcatinator
import time
from lib.data.DataStructure import CoordinatesData, DepthData
from lib.data.NmeaParser import NmeaParser
from lib.folder_struct.Settings import Settings


global_settings = Settings()

global_settings.navi_port.set_port(13)
global_settings.navi_port.set_rate(9600)
global_settings.navi_port.set_message('GGA')

global_settings.depth_port.set_port(13)



try:
    a = DepthData(17.642)
    print(a)

    proc1 = BufferGenerator('COM13', 9600, ['GGA'], ['NAVI'])
    proc2 = BufferGenerator('COM4', 9600, ['DBS'], ['DEPTH'])
    proc3 = BufferGenerator('COM10', 57600, ['DBT'], ['ALT'])
    parser = NmeaParser()

    proc1.repeat_writing_buffer()
    proc2.repeat_writing_buffer()
    proc3.repeat_writing_buffer()

    for i in range(30):
        b1 = proc1.getData()
        b2 = proc2.getData()
        b3 = proc3.getData()


        bc = BufferConcatinator(b1, b2, b3)
        buffer_list = bc.concatinate()
        print(buffer_list)
        
        # b= proc2.getData()
        # c= proc3.getData()

        # if ret is not None:
            
        #     a, b, c = proc1.getData()

        #     if a is not None:
        #         depth = parser.parseDBS(a.string)
        #         print(a.keyword, depth)

        #     if b is not None:
        #         coord = parser.parseGGA(b.string)
        #         print(b.keyword, coord)
        #         print(coord.deg_min())

        #     if c is not None:
        #         altimeter = parser.parseDBT(c.string)
        #         print(c.keyword, altimeter)


        time.sleep(1)

    # for  i in range(10):
    #     # print(proc1.getData())
    #     # print(proc1.getData() is None)
    #     time.sleep(1)
finally:
    proc1.stop_writing_buffer()
    # proc2.stop_writing_buffer()
    # proc3.stop_writing_buffer()

