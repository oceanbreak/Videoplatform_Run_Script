"""
This module takes an image and adds data to it.
Designed to add data on underwater camera snapshots
"""

import PIL
from PIL import ImageFont, Image, ImageDraw
import os

class ImageCaption:

    def __init__(self, img_file, data_collection):
        self.img_file = img_file
        path, file = os.path.split(self.img_file)
        self.path = path
        self.file = file
        self.data_text = data_collection.toDisplayText()
        self.font = ImageFont.truetype('resources/F25_Bank_Printer.ttf', 25)

    def addCaption(self):
        """
        :param img_file:
        :param text_to_draw:
        :return: screenshot with data text on it
        """

        img_file = self.img_file
        text_to_draw = self.data_text

        img = Image.open(img_file)
        draw = ImageDraw.Draw(img)
        draw.text((10,10), text_to_draw, (255, 255, 255), font = self.font)
        draw = ImageDraw.Draw(img)

        img.save(img_file)


    def addSnapLogLine(self):
        with open(self.path + '/SNAP_LOG.txt', 'a') as snapshot_log:
            snapshot_log.write(self.file + '\n')
            snapshot_log.write(self.data_text + '\n\n')
