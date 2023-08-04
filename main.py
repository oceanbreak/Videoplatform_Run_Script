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
    proc3 = BufferGenerator('COM10', 57600, ['DBT', 'MTW'], ['ALT', 'TEMP'])
    proc4 = BufferGenerator('COM3', 9600, ['\x68\x04\x00\x04\x08'], ['INCLIN'])
    parser = NmeaParser()

    proc1.repeat_writing_buffer()
    proc2.repeat_writing_buffer()
    proc3.repeat_writing_buffer()
    proc4.repeat_writing_buffer(IO_mode=True)

    while(True):
        b1 = proc1.getData()
        b2 = proc2.getData()
        b3 = proc3.getData()
        b4 = proc4.getData()


        bc = BufferConcatinator(b1, b2, b3, b4)
        buffer_list = bc.concatinate()
        print(buffer_list)
        

        time.sleep(1.0)

    # for  i in range(10):
    #     # print(proc1.getData())
    #     # print(proc1.getData() is None)
    #     time.sleep(1)
finally:
    proc1.stop_writing_buffer()
    proc2.stop_writing_buffer()
    proc3.stop_writing_buffer()
    proc4.stop_writing_buffer()

