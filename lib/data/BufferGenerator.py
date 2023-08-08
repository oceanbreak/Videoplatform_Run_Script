from lib.data.SonarThread import SonarThread
from lib.data.ComPortData import ComPortData
from lib.data.DataStructure import ComPortString, data_keywords
from lib.folder_struct.Settings import ComPortSettings
import time
print("__generate_buffer__\n")


class BufferGenerator:
    def __init__(self, com_port, rate, messages, data_keywords, printout=False, IO=False):
        self.__printout = printout
        self.data_keyword = data_keywords
        self._com_port = com_port
        self._rate = rate
        self._messages = messages
        self._out_message = False
        self._cur_data = None
        self.IO_mode = IO
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

    
    def write_buffer_IO_byte_mode(self, read_num=14):
        # Function to write and read from buffer in hex mode
        for message in self._messages:
            self._data_line.sendMessage(bytes(message, 'utf-8'))
            self._data_line.readHex(read_num)
            cur_string = self._data_line.getOutputData()
        if cur_string:
            self._cur_data = cur_string


    def repeat_writing_buffer(self):
        if not self.IO_mode:
            self.proc_buffer = SonarThread(self.write_buffer_entry)
        else:
            self.proc_buffer = SonarThread(self.write_buffer_IO_byte_mode)
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


class BufferCollection:

    def __init__(self, settings):

        self.ports = {settings.navi_port : settings.navi_port.port,
         settings.depth_port : settings.depth_port.port,
         settings.altimeter_port : settings.altimeter_port.port,
         settings.temp_port : settings.temp_port.port,
         settings.inclin_port : settings.inclin_port.port}
        
        self.rearanged_buffer_settings = None
        self.buffer_processes = None

        self.rearange()
        

    def rearange(self):
        buffers_settings_list = {}

        # Form dict of buffer settings, in case several messages coming from 1 port
        for item in self.ports:
            if self.ports[item] not in buffers_settings_list:
                if item.enable:
                    buffers_settings_list[self.ports[item]] = [item]
            else:
                if item.enable:
                    buffers_settings_list[self.ports[item]].append(item)

        self.rearanged_buffer_settings = buffers_settings_list
        return buffers_settings_list
    

    def InnitiateBuffers(self):
        # Start generating buffers
        buffer_dict = self.rearanged_buffer_settings
        self.buffer_processes = []
        for com_name in buffer_dict:
            cur_kw = []
            cur_msg = []
            port = buffer_dict[com_name][0].port
            rate = buffer_dict[com_name][0].rate
            for com_setting in buffer_dict[com_name]:
                cur_kw.append(com_setting.keyword)
                cur_msg.append(com_setting.message)

            if cur_kw[0] == data_keywords.INCLIN:
                # Special treatment for inclinometer
                self.buffer_processes.append(BufferGenerator(com_name, rate, ['\x68\x04\x00\x04\x08'], cur_kw, IO=True))
            else:
                self.buffer_processes.append(BufferGenerator(com_name, rate, cur_msg, cur_kw))

        for buffer_proc in self.buffer_processes:
            buffer_proc.repeat_writing_buffer()

        return self.buffer_processes


    def stopWritingBuffers(self):
        for buffer_proc in self.buffer_processes:
            buffer_proc.stop_writing_buffer()

    def getRawData(self):
        buffer_output = []
        for buffer_proc in self.buffer_processes:
            buffer_output.append(buffer_proc.getData())

        concatinator = BufferConcatinator(*buffer_output)
        return concatinator.concatinate()


if __name__ == '__main__':
    proc1 = BufferGenerator('COM12', 9600, ['GGA', 'DBT'])
    proc1.repeat_writing_buffer()
    for  i in range(10):
        # print(proc1.getData())
        # print(proc1.getData() is None)
        time.sleep(1)
    proc1.stop_writing_buffer()