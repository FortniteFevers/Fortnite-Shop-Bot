from PIL import Image
import PIL
import requests
import glob
from math import ceil, sqrt
from typing import Union

response = requests.get('https://fortnite-api.com/v2/shop/br/combined')

currentdate = response.json()['data']['date']
currentdate = currentdate[:10]
# Credits to https://github.com/MyNameIsDark01 for the original Merger code.
# This merger is under rights, you may not take this code and use it in your own project without proper credits to Fevers and Dark.

def merger(datas: Union[list, None] = None, save_as: str = f'shop.jpg'):
    if not datas:
        datas = [Image.open(i) for i in glob.glob('cache/*.png')]

    row_n = len(datas)
        
    rowslen = ceil(sqrt(row_n))
    columnslen = round(sqrt(row_n))

    mode = "RGB"
    px = 512

    rows = rowslen * px
    columns = columnslen * px
    image = Image.new(mode, (rows, columns))

    i = 0

    for card in datas:
        image.paste(
            card,
            ((0 + ((i % rowslen) * card.width)),
                (0 + ((i // rowslen) * card.height)))
        )

        i += 1

    image.save(f"{save_as}")

    return image
