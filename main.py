from lib.data.ComPortData import ComPortData
from lib.data.BufferGenerator import BufferGenerator, BufferConcatinator, BufferCollection
import time
from lib.data.DataStructure import CoordinatesData, DepthData, data_keywords
from lib.data.NmeaParser import NmeaParser
from lib.folder_struct.Settings import Settings



global_settings = Settings()
global_settings.readSettings()

buffer = BufferCollection(global_settings)

buffer_rocess = buffer.InnitiateBuffers()


try:

    while True:

        # buffer_output = []
        # for buffer_proc in buffer_rocess:
        #     buffer_output.append(buffer_proc.getData())

        # concatinator = BufferConcatinator(*buffer_output)
        # output = concatinator.concatinate()
        output = buffer.getRawData()
        print(output)
        time.sleep(0.1)

finally:
    buffer.stopWritingBuffers()

# try:
#     proc1 = BufferGenerator('COM13', 9600, ['GGA'], ['NAVI'])
#     proc2 = BufferGenerator('COM4', 9600, ['DBS'], ['DEPTH'])
#     proc3 = BufferGenerator('COM10', 57600, ['DBT', 'MTW'], ['ALT', 'TEMP'])
#     proc4 = BufferGenerator('COM3', 9600, ['\x68\x04\x00\x04\x08'], ['INCLIN'], IO=True)
#     parser = NmeaParser()

#     proc1.repeat_writing_buffer()
#     proc2.repeat_writing_buffer()
#     proc3.repeat_writing_buffer()
#     proc4.repeat_writing_buffer()

#     while(True):
#         b1 = proc1.getData()
#         b2 = proc2.getData()
#         b3 = proc3.getData()
#         b4 = proc4.getData()


#         bc = BufferConcatinator(b1, b2, b3, b4)
#         buffer_list = bc.concatinate()
#         print(buffer_list)
        

#         time.sleep(1.0)

#     # for  i in range(10):
#     #     # print(proc1.getData())
#     #     # print(proc1.getData() is None)
#     #     time.sleep(1)
# finally:
#     proc1.stop_writing_buffer()
#     proc2.stop_writing_buffer()
#     proc3.stop_writing_buffer()
#     proc4.stop_writing_buffer()

