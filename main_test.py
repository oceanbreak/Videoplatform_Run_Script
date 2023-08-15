from lib.folder_struct.ScanDirectory import ScanDirectory
import time

dir_scan = ScanDirectory('D:/')

for i in range(100):
    print(i)
    dir_scan.getAddedItem()
    time.sleep(1)