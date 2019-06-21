import sonarcom, time, sonar_threading
print("__generate_buffer__\n")

class GenerateBuffer:
    def __init__(self, com_port, rate, message):
        self._com_port = com_port
        self._rate = rate
        self._message = message
        self._cur_data = None
        try:
            self._data_line = sonarcom.ComPortData(com_port, rate, 10, message) #CHANGE
        except:
            print("ERROR Sonardatabufer: Cannot generate buffer with %s message" % message)

    def write_buffer_entry(self):
        try:
           cur_string = self._data_line.getOutputData()
        except AttributeError:
            cur_string = False
        if cur_string:
            print(time.asctime() + ':\t' + str(cur_string))
            self._cur_data = cur_string

    def repeat_writing_buffer(self):
        self.proc_buffer = sonar_threading.SonarThread(self.write_buffer_entry)
        self.proc_buffer.start()

    def stop_writing_buffer(self):
        self.proc_buffer.stop()

    def getData(self):
        return self._cur_data

if __name__ == '__main__':
    proc1 = GenerateBuffer('COM3', 4800, 'GPGGA')
    proc1.repeat_writing_buffer()
    for  i in range(10):
        print(proc1.getData())
        time.sleep(1)
    proc1.stop_writing_buffer()