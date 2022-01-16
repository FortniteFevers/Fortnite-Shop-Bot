import requests
from PIL import Image, ImageFont, ImageDraw
from datetime import date
from datetime import datetime
import os
import time
import shutil
import tweepy

#===============#
loadFont = 'BurbankBigRegular-BlackItalic.otf'
showItems = False
botDelay = 5

twitAPIKey = ''
twitAPISecretKey = ''
twitAccessToken = ''
twitAccessTokenSecret = '' 

updateMode = False
#===============#

auth = tweepy.OAuthHandler(twitAPIKey, twitAPISecretKey)
auth.set_access_token(twitAccessToken, twitAccessTokenSecret)
api = tweepy.API(auth)

def compress():
    import math
    foo = Image.open("shop.jpg")
    x, y = foo.size
    x2, y2 = math.floor(x/2), math.floor(y/2)
    foo = foo.resize((x2,y2),Image.ANTIALIAS)
    foo.save("shop.jpg",quality=65)
    print('Compressed image!')

def genshop():

    try:
        shutil.rmtree('cache')
        os.makedirs('cache')
    except:
        os.makedirs('cache')

    start = time.time()

    response = requests.get('https://fortnite-api.com/v2/shop/br/combined')

    data = response.json()['data']

    currentdate = response.json()['data']['date']
    currentdate = currentdate[:10]

    # --- FEATURED GEN --- #
    print('\nGenerating Featured Section...')
    featured = data['featured']
    count = 0
    for i in featured['entries']:

        if i['newDisplayAssetPath'] != None:
            url = i['newDisplayAsset']['materialInstances'][0]['images']['Background']
        else:
            url = i['items'][0]['images']['icon']

        name = i['items'][0]['id']
        last_seen = i['items'][0]['shopHistory']
        try:
            last_seen = last_seen[-2][:10]
        except:
            last_seen = 'NEW!'
        price = i['finalPrice']

        if i['bundle'] != None:
            url = i['bundle']['image']
            name = f"zzz{i['bundle']['name']}"
        
        if last_seen != 'NEW!':
            dateloop = datetime.strptime(last_seen, "%Y-%m-%d")
            current = datetime.strptime(currentdate, "%Y-%m-%d")
            diff = str(current.date() - dateloop.date())
            diff = diff.replace('days, 0:00:00', '')
            if diff == '0:00:00':
                diff = '1'
        else:
            diff = 'NEW!'


        open(f'cache/{name}.png', 'wb').write(requests.get(url).content)
        background = Image.open(f'cache/{name}.png').resize((512, 512), Image.ANTIALIAS)
        background.save(f'cache/{name}.png')

        img=Image.new("RGB",(512,512))
        img.paste(background)

        # OTHER ITEMS GEN
        try:
            if i['items'][1]:
                url = i['items'][1]['images']['icon']
                open(f'cache/temp{name}.png', 'wb').write(requests.get(url).content)
                background = Image.open(f'cache/temp{name}.png').resize((80, 80), Image.ANTIALIAS)
                background.save(f'cache/temp{name}.png')
            
                background = Image.open(f'cache/temp{name}.png')
                img.paste(background, (0, 0), background)

                os.remove(f'cache/temp{name}.png')
            if i['items'][2]:
                url = i['items'][2]['images']['icon']
                open(f'cache/temp{name}.png', 'wb').write(requests.get(url).content)
                background = Image.open(f'cache/temp{name}.png').resize((80, 80), Image.ANTIALIAS)
                background.save(f'cache/temp{name}.png')
            
                background = Image.open(f'cache/temp{name}.png')
                img.paste(background, (0, 100), background)

                os.remove(f'cache/temp{name}.png')

            if i['items'][3]:
                url = i['items'][3]['images']['icon']
                open(f'cache/temp{name}.png', 'wb').write(requests.get(url).content)
                background = Image.open(f'cache/temp{name}.png').resize((80, 80), Image.ANTIALIAS)
                background.save(f'cache/temp{name}.png')
            
                background = Image.open(f'cache/temp{name}.png')
                img.paste(background, (0, 200), background)

                os.remove(f'cache/temp{name}.png')
        except:
            pass



        overlay = Image.open('overlay.png').convert('RGBA')
        img.paste(overlay, (0,0), overlay)

        img.save(f'cache/{name}.png')

        background = Image.open(f'cache/{name}.png')

        itemname = i['items'][0]['name']
        if i['bundle'] != None:
            itemname = f"{i['bundle']['name']}"
        
        font=ImageFont.truetype(loadFont,35)
        draw=ImageDraw.Draw(background)
        draw.text((256,420),itemname,font=font,fill='white', anchor='ms') # Writes name

        if 'NEW!' in diff:
            diff_text = 'NEW!'
        else:
            diff = diff.replace(' ', '')
            diff_text = f'LAST SEEN: {diff} days ago'

        if '0:00' in diff_text:
            diff_text = 'LAST SEEN: 1 day ago'

        font=ImageFont.truetype(loadFont,15)
        draw=ImageDraw.Draw(background)
        draw.text((256,450),diff_text,font=font,fill='white', anchor='ms') # Writes date last seen

        font=ImageFont.truetype(loadFont,40)
        draw=ImageDraw.Draw(background)
        draw.text((256,505),f'{price}',font=font,fill='white', anchor='ms') # Writes price

        background.save(f'cache/{name}.png')

        if showItems != False:
            print(f'Last Seen: {diff} days ago\n{name} - {price}\n')

        count += 1

    print(f'Done generating "{count}" items in the Featured section.')
    featrued_num = count
    print('')

    # --- DAILY GEN --- #
    print('Generating Daily Section...')
    daily = data['daily']
    count = 0
    for i in daily['entries']:

        if i['newDisplayAssetPath'] != None:
            url = i['newDisplayAsset']['materialInstances'][0]['images']['Background']
        else:
            url = i['items'][0]['images']['icon']


        name = i['items'][0]['id']
        last_seen = i['items'][0]['shopHistory']
        try:
            last_seen = last_seen[-2][:10]
        except:
            last_seen = 'NEW!'
        price = i['finalPrice']

        if i['bundle'] != None:
            url = i['bundle']['image']
            name = f"zzz{i['bundle']['name']}"
        
        if last_seen != 'NEW!':
            dateloop = datetime.strptime(last_seen, "%Y-%m-%d")
            current = datetime.strptime(currentdate, "%Y-%m-%d")
            diff = str(current.date() - dateloop.date())
            diff = diff.replace('days, 0:00:00', '')
            if diff == '0:00:00':
                diff = '1'
        else:
            diff = 'NEW!'


        open(f'cache/{name}.png', 'wb').write(requests.get(url).content)
        background = Image.open(f'cache/{name}.png').resize((512, 512), Image.ANTIALIAS)
        background.save(f'cache/{name}.png')

        img=Image.new("RGB",(512,512))
        img.paste(background)

        # OTHER ITEMS GEN
        try:
            if i['items'][1]:
                url = i['items'][1]['images']['icon']
                open(f'cache/temp{name}.png', 'wb').write(requests.get(url).content)
                background = Image.open(f'cache/temp{name}.png').resize((80, 80), Image.ANTIALIAS)
                background.save(f'cache/temp{name}.png')
            
                background = Image.open(f'cache/temp{name}.png')
                img.paste(background, (0, 0), background)

                os.remove(f'cache/temp{name}.png')
            if i['items'][2]:
                url = i['items'][2]['images']['icon']
                open(f'cache/temp{name}.png', 'wb').write(requests.get(url).content)
                background = Image.open(f'cache/temp{name}.png').resize((80, 80), Image.ANTIALIAS)
                background.save(f'cache/temp{name}.png')
            
                background = Image.open(f'cache/temp{name}.png')
                img.paste(background, (0, 100), background)

                os.remove(f'cache/temp{name}.png')

            if i['items'][3]:
                url = i['items'][3]['images']['icon']
                open(f'cache/temp{name}.png', 'wb').write(requests.get(url).content)
                background = Image.open(f'cache/temp{name}.png').resize((80, 80), Image.ANTIALIAS)
                background.save(f'cache/temp{name}.png')
            
                background = Image.open(f'cache/temp{name}.png')
                img.paste(background, (0, 200), background)

                os.remove(f'cache/temp{name}.png')
        except:
            pass

        overlay = Image.open('overlay.png').convert('RGBA')
        img.paste(overlay, (0,0), overlay)

        img.save(f'cache/{name}.png')

        background = Image.open(f'cache/{name}.png')


        itemname = i['items'][0]['name']
        if i['bundle'] != None:
            itemname = f"{i['bundle']['name']}"
        font=ImageFont.truetype(loadFont,35)
        draw=ImageDraw.Draw(background)
        draw.text((256,420),itemname,font=font,fill='white', anchor='ms') # Writes name

        if 'NEW!' in diff:
            diff_text = 'NEW!'
        else:
            diff = diff.replace(' ', '')
            diff_text = f'LAST SEEN: {diff} days ago'

        if '0:00' in diff_text:
            diff_text = 'LAST SEEN: 1 day ago'

        font=ImageFont.truetype(loadFont,15)
        draw=ImageDraw.Draw(background)
        draw.text((256,450),diff_text,font=font,fill='white', anchor='ms') # Writes date last seen

        font=ImageFont.truetype(loadFont,40)
        draw=ImageDraw.Draw(background)
        draw.text((256,505),f'{price}',font=font,fill='white', anchor='ms') # Writes price

        background.save(f'cache/{name}.png')

        if showItems != False:
            print(f'Last Seen: {diff} days ago\n{name} - {price}\n')

        count += 1


    print(f'Done generating "{count}" items in the Daily section.')
    daily_num = count
    
    #########################

    totalnum = daily_num + featrued_num
    print(f'\nGenerated {totalnum} items from the {currentdate} Item Shop.')

    print('\nMerging images...')
    from merger import merger
    merger(currentdate)

    end = time.time()

    print(f"IMAGE GENERATING COMPLETE - Generated image in {round(end - start, 2)} seconds!")

    img=Image.open(f'shop.jpg')
    img.show()
    #try:
    #    api.update_with_media(f'shop.jpg', f'#Fortnite Item Shop update for {currentdate}!\n\nConsider using code "Fevers" to support me! #EpicPartner')
    #except:
    #    compress()
    #    api.update_with_media(f'shop.jpg', f'#Fortnite Item Shop update for {currentdate}!\n\nConsider using code "Fevers" to support me! #EpicPartner')
    #time.sleep(10)
    

def main():
    apiurl = f'https://fortnite-api.com/v2/shop/br/combined'

    response = requests.get(apiurl)
    shopData = response.json()['data']['hash']
    currentdate = response.json()['data']['date']
    currentdate = currentdate[:10]

    count = 1

    while 1:
        
        response = requests.get(apiurl)
        if response:
            try:
                shopDataLoop = response.json()['data']['hash']
            except:
                return main()
            print("Checking for change in the Shop... ("+str(count)+")")
            count = count + 1
            
            if shopData != shopDataLoop: # Now run program as normal. Shop has changed.
                print('\nTHE SHOP HAS UPDATED!')
                time.sleep(10)
                try:
                    shutil.rmtree('cache')
                    os.makedirs('cache')
                except:
                    os.makedirs('cache')
                genshop()
                try:
                    api.update_with_media(f'shop.jpg', f'#Fortnite Item Shop update for {currentdate}!\n\nConsider using code "Fevers" to support me! #EpicPartner')
                except:
                    print('FILE SIZE TOO BIG. COMPRESSING IMAGE.')
                    compress()
                    
                    print('')
                    print('Attempting to tweet...')
                    api.update_with_media(f'shop.jpg', f'#Fortnite Item Shop update for {currentdate}!\n\nConsider using code "Fevers" to support me! #EpicPartner')
                    print('Tweeted!')

                print('')
                return main()
        
        else:
            print("FAILED TO GRAB SHOP DATA: URL DOWN")

        time.sleep(botDelay)

if updateMode == True:
    main()
else:
    genshop()
