"""
This module takes an image and adds data to it.
Designed to add data on underwater camera snapshots
"""

import PIL
from PIL import ImageFont, Image, ImageDraw

def addCaption(img_file, text_to_draw):
    """
    :param img_file:
    :param text_to_draw:
    :return: screenshot with data text on it
    """

    font = ImageFont.truetype('resources/F25_Bank_Printer.ttf', 25)
    img_file = img_file
    text_to_draw = text_to_draw

    img = Image.open(img_file)
    draw = ImageDraw.Draw(img)
    draw.text((10,10), text_to_draw, (255, 255, 255), font = font)
    draw = ImageDraw.Draw(img)


    img.save(img_file)