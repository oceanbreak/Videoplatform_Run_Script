import numpy as np
import os
from matplotlib import pyplot as plt
from lib.folder_struct.SrtFromLog import LogReader, LogData
from lib.data.DataStructure import CoordinatesData
from lib.UI.Settings import Settings
from lib.data.DataCollection import DataCollection
from tkinter import filedialog




class Graphs:

    GRAPHS_SUBFOLDER = 'graphs'
    NAVI_BASE_NAME = 'track'
    TEMP_DEPTH_BASE_NAME = 'temp_depth'
    TEMP_RANGE_NAME = 'temp_range'
    DEPTH_RANGE_NAME = 'depth_range'
    ALTIMETER_RANGE_NAME = 'altimeter_range'

    def __init__(self, data_collection : DataCollection, settings : Settings):
        self.data_collection = data_collection
        self.settings = settings
        self.log_file = ''

    def askFiles(self):
        ret = filedialog.askopenfilename(initialdir=self.settings.default_folder)
        if ret != '':
            self.log_file = ret
            self.log_path, self.log_name = os.path.split(ret)
            self.log_name = '.'.join(self.log_name.split('.')[:-1])

            # Create output folder
            if self.GRAPHS_SUBFOLDER not in os.listdir(self.log_path):
                os.mkdir(os.path.join(self.log_path, self.GRAPHS_SUBFOLDER))
        return ret

    def readLogFile(self):
        reader = LogReader(log_file_path=self.log_file ,data_collection=data_collection)
        reader.readLogFile(self.log_file)
        self.log_data = reader.getLogData()

    def plotCoordinates(self):
        # Form coordinates in DD.DDDDD format
        # coords = [CoordinatesData(line.nav_lat.value, line.nav_lon.value) for line in self.log_data.values()]
        # print(coords)
        lat_arr = []
        lon_arr = []

        for line in self.log_data.values():
            coords = (CoordinatesData(line.nav_lat.value, line.nav_lon.value))
            y, x = coords.degrees()
            lat_arr.append(y)
            lon_arr.append(x)
        print(len(lat_arr), len(lon_arr))

        fig, ax = plt.subplots(figsize=(5,10))
        ax.plot(lon_arr,lat_arr)
        ax.set_xticklabels(ax.get_xticks(), rotation = 45)
        ax.xaxis.set_major_formatter(self.major_formatter_lon)
        ax.yaxis.set_major_formatter(self.major_formatter_lat)
        ax.grid()

        out_file_name = f'{self.log_name}_{self.NAVI_BASE_NAME}.png'
        plt.savefig(os.path.join(self.log_path, self.GRAPHS_SUBFOLDER, out_file_name), dpi=300)
        plt.show()

            # print(line.nav_lat.value, line.nav_lon.value)
            # print(CoordinatesData(line.nav_lat.value, line.nav_lon.value))
    
    # Def format of coord
    @staticmethod
    def major_formatter_lat(x, pos):
        letter = 'N' if x > 0 else 'S'
        val = np.abs(x)
        deg = int(np.floor(val))
        minut = (val - np.floor(val))* 60
        return f"{deg}\xb0 {minut:.3f}' {letter}"

    @staticmethod
    def major_formatter_lon(x, pos):
        letter = 'E' if x > 0 else 'W'
        val = np.abs(x)
        deg = int(np.floor(val))
        minut = (val - np.floor(val))* 60
        return f"{deg}\xb0 {minut:.3f}' {letter}"

    # def coord

if __name__ == '__main__':
    settings = Settings()
    data_collection = DataCollection(settings)
    
    graphs = Graphs(data_collection, settings)
    graphs.askFiles()
    graphs.readLogFile()
    
    graphs.plotCoordinates()

    # for line in graphs.log_data.values():
    #     print(line.nav_lat.value, line.nav_lon.value)