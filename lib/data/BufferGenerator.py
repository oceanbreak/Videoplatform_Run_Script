from lib.data.SonarThread import SonarThread
from lib.data.ComPortData import ComPortData
import time
print("__generate_buffer__\n")

class BufferGenerator:
    def __init__(self, com_port, rate, messages):
        self._com_port = com_port
        self._rate = rate
        self._message = messages
        self._out_message = False
        self._cur_data = None
        try:
            self._data_line = ComPortData(com_port, rate, 5, messages) #CHANGE
        except:
            print("ERROR Sonardatabufer: Cannot generate buffer with %s message" % messages)

    def write_buffer_entry(self):
        if self._out_message:
            self._data_line.sendMessage(self._out_message)
            print('"%s" message sent to port %s' % (self._out_message, self._com_port))
            self._out_message = False
        try:
            self._data_line.pullData()
            cur_string = self._data_line.getOutputData()
            # print(self._data_line.time_out_timer)
        except IndexError:
            cur_string = False
        if cur_string:
            # print(time.asctime() + ':\t' + str(cur_string))
            self._cur_data = cur_string


    def repeat_writing_buffer(self):
        self.proc_buffer = SonarThread(self.write_buffer_entry)
        self.proc_buffer.start()

    def stop_writing_buffer(self):
        self.proc_buffer.stop()
        self._data_line.closePort()

    def getData(self):
        return self._cur_data

    def send_message(self, out_message):
        self._out_message = out_message

if __name__ == '__main__':
    proc1 = BufferGenerator('COM12', 9600, ['GGA', 'DBT'])
    proc1.repeat_writing_buffer()
    for  i in range(10):
        # print(proc1.getData())
        # print(proc1.getData() is None)
        time.sleep(1)
    proc1.stop_writing_buffer()