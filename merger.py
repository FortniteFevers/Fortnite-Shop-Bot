import requests
from PIL import Image, ImageFont, ImageDraw
import PIL
from datetime import datetime
import os
from math import ceil, sqrt
from typing import Union
import glob

# Credits to https://github.com/MyNameIsDark01 for the original Merger code.
# This merger is under rights, you may not take this code and use it in your own project without proper credits to Fevers and Dark.

def merger(ogitems, currentdate, datas: Union[list, None] = None):
    save_as = f'shop {currentdate}.jpg'

    # If no data is passed, retrieve from cache folders
    if not datas:
        if ogitems == False:
            datas = [Image.open(i) for i in glob.glob('cache/*.png')]
        else:
            datas = [Image.open(i) for i in glob.glob('ogcache/*.png')]

    list_ = []
    if ogitems == False:
        list_.extend(f'cache/{file}' for file in os.listdir('cache') if not file.startswith('tempzzz'))
    else:
        list_.extend(f'ogcache/{file}' for file in os.listdir('ogcache'))

    # Number of items and grid size calculation
    num = len(list_)
    rowslen = ceil(sqrt(num))
    columnslen = ceil(num / rowslen)  # Ensure enough rows for all items

    mode = "RGB"
    px = 512

    # Final image size
    width = rowslen * px
    height = columnslen * px
    image = Image.new(mode, (width, height), (0, 0, 0))  # Fill with black to avoid blank gaps

    # Sort files to ensure consistent order
    datas = [Image.open(i) for i in sorted(list_)]

    # Paste each image onto the grid
    for i, card in enumerate(datas):
        x = (i % rowslen) * px
        y = (i // rowslen) * px
        image.paste(card, (x, y))

    # Save main shop image
    image.save(f"{save_as}" if ogitems == False else "OGitems.jpg")

    #==== GENERATES TITLE ====#

    if ogitems == False:
        img = Image.new("RGB", (width, height + 322), 0x000000)  # Add space for the title
        shopimage = Image.open(f"{save_as}")
        img.paste(shopimage, (0, 322))
        
        # Add title and date
        font_title = ImageFont.truetype('BurbankBigRegular-BlackItalic.otf', 150)
        font_date = ImageFont.truetype('BurbankBigRegular-BlackItalic.otf', 50)
        draw = ImageDraw.Draw(img)
        draw.text((width / 2, 190), 'FORTNITE ITEM SHOP', font=font_title, fill='white', anchor='ms')  # Title
        draw.text((width / 2, 240), currentdate, font=font_date, fill='white', anchor='ms')  # Date

        # Save final image
        img.save(f'{save_as}')
        img.save('shop.jpg')

    return image
