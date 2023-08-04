from lib.data.ComPortData import ComPortData
import time

navi = ComPortData('COM13', 9600, 5, ['GGA', 'MTW'], ['NAVI', 'TEMP'])

try:
    while(True):
        navi.pullData()
        ret = [ str(a) for a in navi.getOutputData()]
        print(ret)
        # time.sleep(0.1)

finally:
    navi.closePort()
