import requests
from PIL import Image, ImageFont, ImageDraw
import PIL
from datetime import datetime
import os
from math import ceil, sqrt
from typing import Union
import glob
response = requests.get('https://fortnite-api.com/v2/shop/br/combined')

currentdate = response.json()['data']['date']
currentdate = currentdate[:10]
# Credits to https://github.com/MyNameIsDark01 for the original Merger code.
# This merger is under rights, you may not take this code and use it in your own project without proper credits to Fevers and Dark.

def merger(ogitems, datas: Union[list, None] = None, save_as: str = f'shop {currentdate}.jpg'):
    print(ogitems)
    response = requests.get('https://fortnite-api.com/v2/shop/br/combined')
    currentdate = response.json()['data']['date']
    currentdate = currentdate[:10]
    if not datas:
        if ogitems == False:
            datas = [Image.open(i) for i in glob.glob('cache/*.png')]
        else:
            datas = [Image.open(i) for i in glob.glob('ogcache/*.png')]

    list_ = []
    num = 0
    if ogitems == False:
        for file in os.listdir('cache'):
            num += 1
            
            if file.startswith('tempzzz'):
                pass
            else:
                list_.append(f'cache/{file}')
    else:
        for file in os.listdir('ogcache'):
            num += 1   
            list_.append(f'ogcache/{file}')

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

    if ogitems == False:
        image.save(f"{save_as}")
    else:
        image.save(f"OGitems.jpg")

    #==== GENERATES TITLE ====#

    if ogitems == False:
        img = PIL.Image.open(f"{save_as}")
        width, height = img.size

        img=Image.new("RGB",(width,height+322), 0x000000)

        shopimage = Image.open(f"{save_as}")
        img.paste(shopimage, (0, 322))
        
        font=ImageFont.truetype('BurbankBigRegular-BlackItalic.otf',150)
        draw=ImageDraw.Draw(img)
        draw.text((width/2,190),'FORTNITE ITEM SHOP',font=font,fill='white', anchor='ms') # Writes name

        font=ImageFont.truetype('BurbankBigRegular-BlackItalic.otf',50)
        draw.text((width/2,240),currentdate,font=font,fill='white', anchor='ms') # Writes name

        img.save(f'{save_as}')
        img.save('shop.jpg')

        return image
