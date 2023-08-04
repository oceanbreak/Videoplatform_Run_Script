from lib.data.SonarThread import SonarThread
from lib.data.ComPortData import ComPortData
from lib.data.DataStructure import ComPortString
import time
print("__generate_buffer__\n")


class BufferGenerator:
    def __init__(self, com_port, rate, messages, data_keywords, printout=False):
        self.__printout = printout
        self.data_keyword = data_keywords
        self._com_port = com_port
        self._rate = rate
        self._messages = messages
        self._out_message = False
        self._cur_data = None
        try:
            self._data_line = ComPortData(com_port, rate, 5, messages, data_keywords) #CHANGE
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
            if self.__printout:
                print(time.asctime() + ':\t' + str([str(cs) for cs in cur_string]))
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


class BufferConcatinator:

    def __init__(self, *args, **kwargs):
        self.__buffer_objects = []
        for bobj_list in args:
            # Test here if buffer returns None
            if bobj_list is  not None:
                for bobj in bobj_list:
                    self.__buffer_objects.append(bobj)

    def concatinate(self):
        ret = {}
        for bobj in self.__buffer_objects:
            ret[bobj.keyword] = bobj.string
        return ret


if __name__ == '__main__':
    proc1 = BufferGenerator('COM12', 9600, ['GGA', 'DBT'])
    proc1.repeat_writing_buffer()
    for  i in range(10):
        # print(proc1.getData())
        # print(proc1.getData() is None)
        time.sleep(1)
    proc1.stop_writing_buffer()