from lib.data.ComPortData import ComPortData
from lib.data.BufferGenerator import BufferGenerator, BufferConcatinator, BufferCollection
import time
from lib.data.DataStructure import CoordinatesData, DepthData, data_keywords
from lib.data.NmeaParser import NmeaParser
from lib.UI.Settings import Settings
from lib.data.DataCollection import DataCollection



global_settings = Settings()
global_settings.readSettings()

buffer = BufferCollection(global_settings)

buffer_rocess = buffer.InnitiateBuffers()
collection = DataCollection()

try:

    while True:

        output = buffer.getRawData()
        # print(output)
        
        collection.readDataFromBuffer(output)

        print(collection.toDisplayText())

        time.sleep(0.5)

finally:
    buffer.stopWritingBuffers()

