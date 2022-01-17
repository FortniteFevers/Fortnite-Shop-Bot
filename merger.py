from PIL import Image, ImageFont, ImageDraw
import PIL
import requests
import glob
from math import ceil, sqrt
from typing import Union
import os

# Credits to https://github.com/MyNameIsDark01 for the original Merger code.
# This merger is under rights, you may not take this code and use it in your own project without proper credits to Fevers and Dark.

def merger(currentdate, datas: Union[list, None] = None, save_as: str = f'shop.jpg'):
    if not datas:
        datas = [Image.open(i) for i in glob.glob('cache/*.png')]

    list_ = []
    num = 0
    for file in os.listdir('cache'):
        num += 1
        list_.append(f'cache/{file}')

    row_n = num
        
    rowslen = ceil(sqrt(row_n))
    columnslen = round(sqrt(row_n))

    mode = "RGB"
    px = 512

    rows = rowslen * px
    columns = columnslen * px
    image = Image.new(mode, (rows, columns))

    i = 0

    datas = [Image.open(i) for i in sorted(list_)]

    for card in datas:
        image.paste(
            card,
            ((0 + ((i % rowslen) * card.width)),
                (0 + ((i // rowslen) * card.height)))
        )

        i += 1

    image.save(f"{save_as}")

    img = PIL.Image.open(f"{save_as}")
    width, height = img.size

    img=Image.new("RGB",(width,height+322))

    shopimage = Image.open(f"{save_as}")
    img.paste(shopimage, (0, 322))
    
    font=ImageFont.truetype('BurbankBigRegular-BlackItalic.otf',150)
    draw=ImageDraw.Draw(img)
    draw.text((width/2,150),'FORTNITE ITEM SHOP',font=font,fill='white', anchor='ms') # Writes name

    font=ImageFont.truetype('BurbankBigRegular-BlackItalic.otf',50)
    draw.text((width/2,200),currentdate,font=font,fill='white', anchor='ms') # Writes name

    img.save(f'{save_as}')

    return image
