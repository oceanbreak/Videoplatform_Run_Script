import numpy as np
import os
from matplotlib import pyplot as plt
from lib.folder_struct.SrtFromLog import LogReader, LogData
from lib.data.DataStructure import CoordinatesData
from lib.UI.Settings import Settings
from lib.data.DataCollection import DataCollection
from tkinter import filedialog
from scipy.signal import savgol_filter

def moving_average(data, window):
    data = np.array(data)

    if window % 2 !=1:
        print('Window size must be odd')
        raise ValueError
    range_window = (-window//2+1, window//2+1)

    out_data = []
    for i, val in enumerate(data):
        temp_arr = []
        if i < window // 2:
            for j in range(*range_window):
                if i+j >= 0:
                    temp_arr.append(data[i+j])

        elif i > data.shape[0] - window/2:
            
            for j in range(*range_window):
                try:
                    temp_arr.append(data[i+j])
                except IndexError:
                    pass
        else:
            for j in range(*range_window):
                temp_arr.append(data[i+j])
#         print(f'{i}: {temp_arr}')
        temp_arr = np.array(temp_arr)
        out_data.append(np.mean(temp_arr[temp_arr != None]))
    return out_data


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

    @staticmethod
    def floatVal(value):
        try:
            val = float(value)
        except ValueError:
            val = None
        return val

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
        reader = LogReader(log_file_path=self.log_file ,data_collection=self.data_collection)
        reader.readLogFile(self.log_file)
        self.log_data = reader.getLogData()

    def formAxes(self):
        # Form coordinates in DD.DDDDD format
        self.lat_arr = []
        self.lon_arr = []
        self.depth_arr = []
        self.temp_arr = []
        self.tr_length_arr = []
        self.tr_time_arr = []
        self.altimeter_arr = []

        for line in self.log_data.values():
            coords = (CoordinatesData(line.nav_lat.value, line.nav_lon.value))
            y, x = coords.degrees()
            self.lat_arr.append(y)
            self.lon_arr.append(x)
            
            self.depth_arr.append(self.floatVal(line.depth.value))
            self.tr_length_arr.append(self.floatVal(line.track_length.value))
            # self.tr_time_arr.append(float(line.track_time.value))
            self.temp_arr.append(self.floatVal(line.temp.value))

    def plotCoordinates(self):
        fig, ax = plt.subplots(figsize=(5,10))
        ax.plot(self.lon_arr,self.lat_arr)
        ax.set_xticklabels(ax.get_xticks(), rotation = 45)
        ax.xaxis.set_major_formatter(self.major_formatter_lon)
        ax.yaxis.set_major_formatter(self.major_formatter_lat)
        ax.grid()
        # ax.set_title('Трек')
        ax.set_xlabel('Долгота')
        ax.set_ylabel('Широта')

        out_file_name = f'{self.log_name}_{self.NAVI_BASE_NAME}.png'
        plt.savefig(os.path.join(self.log_path, self.GRAPHS_SUBFOLDER, out_file_name), dpi=300)
        plt.show()

    def plotTemperatureRange(self):
        fig, ax = plt.subplots(figsize=(12,5))
        temp_filtered = moving_average(self.temp_arr, 13)
        # temp_filtered = self.temp_arr
        ax.plot(self.tr_length_arr, temp_filtered)

        ax.grid()
        # ax.set_title('Температура')
        ax.set_xlabel('Длина трека, м')
        ax.set_ylabel('Температура, С')

        out_file_name = f'{self.log_name}_{self.TEMP_RANGE_NAME}.png'
        plt.savefig(os.path.join(self.log_path, self.GRAPHS_SUBFOLDER, out_file_name), dpi=300)
        plt.show()


    def plotDepthRange(self):
        fig, ax = plt.subplots(figsize=(12,5))
        depth_filtered = savgol_filter(self.depth_arr, 23, 2)
        # temp_filtered = self.temp_arr
        ax.plot(self.tr_length_arr, depth_filtered)

        ax.grid()
        ax.set_xlabel('Длина трека, м')
        ax.set_ylabel('Глубина, м')
        ax.invert_yaxis()

        out_file_name = f'{self.log_name}_{self.DEPTH_RANGE_NAME}.png'
        plt.savefig(os.path.join(self.log_path, self.GRAPHS_SUBFOLDER, out_file_name), dpi=300)
        plt.show()

    def plotTempDepth(self):
        fig, ax = plt.subplots(figsize=(4,12))
        temp_filtered = moving_average(self.temp_arr, 13)
        # temp_filtered = self.temp_arr
        ax.invert_yaxis()
        ax.set_xlabel('Температура, С')
        ax.set_ylabel('Глубина, м')
        ax.plot(temp_filtered, self.depth_arr)

        ax.grid()

        out_file_name = f'{self.log_name}_{self.TEMP_DEPTH_BASE_NAME}.png'
        plt.savefig(os.path.join(self.log_path, self.GRAPHS_SUBFOLDER, out_file_name), dpi=300)
        plt.show()      

    def run(self):
        ret = self.askFiles()
        if ret:
            self.readLogFile()
            self.formAxes()
            self.plotCoordinates()
            self.plotTemperatureRange()
            self.plotDepthRange()
            self.plotTempDepth()
      
    
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
    graphs.run()

    # for line in graphs.log_data.values():
    #     print(line.nav_lat.value, line.nav_lon.value)