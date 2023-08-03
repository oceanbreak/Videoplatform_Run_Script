from lib.data.ComPortData import ComPortData
from lib.data.BufferGenerator import BufferGenerator
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

    proc1 = BufferGenerator('COM13', 9600, ['DBS', 'GGA', "DBT"])
    # proc2 = BufferGenerator('COM13', 9600, ['GGA'])
    # proc3 = BufferGenerator('COM13', 9600, ['DBT'])
    parser = NmeaParser()

    proc1.repeat_writing_buffer()
    # proc2.repeat_writing_buffer()
    # proc3.repeat_writing_buffer()

    for i in range(30):
        ret = proc1.getData()
        
        # b= proc2.getData()
        # c= proc3.getData()

        if ret is not None:
            
            a, b, c = proc1.getData()

            if a is not None:
                depth = parser.parseDBS(a)
                print(depth)

            if b is not None:
                coord = parser.parseGGA(b)
                print(coord)
                print(coord.deg_min())

            if c is not None:
                altimeter = parser.parseDBT(c)
                print(altimeter)

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
finally:
    proc1.stop_writing_buffer()
    # proc2.stop_writing_buffer()
    # proc3.stop_writing_buffer()

