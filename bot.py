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
showItems = False # Doesn't do anything. Just prints the items in the console while genrating.
botDelay = 15 # Time for the bot to check when the shop updates

# These are keys provided by the Twitter API. (API LINK: https://developer.twitter.com/en/portal/dashboard)
twitAPIKey = '' 
twitAPISecretKey = ''
twitAccessToken = ''
twitAccessTokenSecret = '' 

updateMode = True # If true, the system keeps refreshing until shop updates. If false, the system instnatly runs the shop generation.

showData = True # Shows shop data in your tweet, I reccomend to keep this on

CreatorCode = '' # Adds a creator code to your caption

OGitemsbot = True # Posts a seperate tweet after the Item Shop showcasing if there are any rare items that have returned to the shop
opitemdate = 150 # If items are over .... days, classify as a "rare" cosmetic
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
    if response:
        pass
    else:
        return genshop()

    try:
        data = response.json()['data']
    except:
        return genshop()

    currentdate = response.json()['data']['date']
    currentdate = currentdate[:10]

    # --- FEATURED GEN --- #
    print('\nGenerating Featured Section...')
    featured = data['featured']
    count = 0
    for i in featured['entries']:

        if i['newDisplayAssetPath'] != None:
            try:
                try:
                    url = i['newDisplayAsset']['materialInstances'][0]['images']['Background']
                except:
                    url = i['items'][0]['images']['icon']
            except:
                try:
                    url = i['newDisplayAsset']['materialInstances'][0]['images']['OfferImage']
                except:
                    url = i['items'][0]['images']['icon']
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
        if i['bundle'] == None:
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
    if daily != None:
        for i in daily['entries']:
    
            if i['newDisplayAssetPath'] != None:
                try:
                    try:
                        url = i['newDisplayAsset']['materialInstances'][0]['images']['Background']
                    except:
                        pass
                except:
                    url = i['newDisplayAsset']['materialInstances'][0]['images']['OfferImage']
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
            if i['bundle'] == None:
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
    else:
        print("Daily section does not exist.)

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

    s = response.json()['data']

    list = []

    for i in s['featured']['entries']:
        for i in i['items']:
            shophistory = i['shopHistory']
            try:
                lastseen = shophistory[-2]
            except:
                lastseen = currentdate
            lastseen = lastseen[:10]
            dateloop = datetime.strptime(lastseen, "%Y-%m-%d")
            current = datetime.strptime(currentdate, "%Y-%m-%d")
            diff = current.date() - dateloop.date()
            daysd=int(diff.days)
            list.append(daysd)

    for i in s['daily']['entries']:
        for i in i['items']:
            shophistory = i['shopHistory']
            try:
                lastseen = shophistory[-2]
            except:
                lastseen = currentdate
            lastseen = lastseen[:10]
            dateloop = datetime.strptime(lastseen, "%Y-%m-%d")
            current = datetime.strptime(currentdate, "%Y-%m-%d")
            diff = current.date() - dateloop.date()
            daysd=int(diff.days)
            list.append(daysd)

    featureditems = len(s['featured']['entries'])
    dailyitems = len(s['daily']['entries'])
    totalitems = featureditems+dailyitems

    list.sort(reverse = True)
    maxitem = list[0]

    list.sort()
    minitem = list[0]

    average = sum(list) / len(list)
    average = round(average, 0)

    if showData == True:
        text = f'#Fortnite Item Shop update for {currentdate}!\n\nConsider using code "{CreatorCode}" to support me! #EpicPartner\n\nTotal Items: {totalitems}\nMax Last Seen: {maxitem} days\nMin Last Seen: {minitem} days\nAverage of Last Seen items: {average} days'
    else:
        text = f'#Fortnite Item Shop update for {currentdate}!\n\nConsider using code "{CreatorCode}" to support me! #EpicPartner'

    try:
        api.update_with_media(f'shop.jpg', text)
    except:
        compress()
        api.update_with_media(f'shop.jpg', text)

    print('Tweeted!')

    list.clear()
    time.sleep(10)
    
def ogitems():
    ######################
    #opitemdate = 150
    ######################

    today = date.today()
    currentdate = today.strftime("%Y-%m-%d")
    response = requests.get('https://fortnite-api.com/v2/shop/br/combined')
    featured = response.json()['data']['featured']
    daily = response.json()['data']['daily']

    resultlist = []
    numberlist = []

    for i in featured['entries']:
        for i in i['items']:
            id = i['id']
            name = i['name']
            type = i['type']['displayValue']
            shophistory = i['shopHistory']
            try:
                lastseen = shophistory[-2]
            except:
                lastseen = currentdate
            lastseen = lastseen[:10]
            dateloop = datetime.strptime(lastseen, "%Y-%m-%d")
            current = datetime.strptime(currentdate, "%Y-%m-%d")
            diff = current.date() - dateloop.date()
            daysd=int(diff.days)
            if daysd >= opitemdate:
            
                resultlist.append(
                    {
                        "name": name,
                        "id": id,
                        "lastseen_days": f"{diff.days}",
                        "lastseen_date": lastseen,
                        "type": type
                    }
                )

                numberlist.append(diff.days)

    for i in daily['entries']:
        for i in i['items']:
            id = i['id']
            name = i['name']
            type = i['type']['displayValue']
            shophistory = i['shopHistory']
            try:
                lastseen = shophistory[-2]
            except:
                lastseen = currentdate
            lastseen = lastseen[:10]
            dateloop = datetime.strptime(lastseen, "%Y-%m-%d")
            current = datetime.strptime(currentdate, "%Y-%m-%d")
            diff = current.date() - dateloop.date()
            daysd=int(diff.days)
            if daysd >= opitemdate:
            
                resultlist.append(
                    {
                        "name": name,
                        "id": id,
                        "lastseen_days": f"{diff.days}",
                        "lastseen_date": lastseen,
                        "type": type
                    }
                )

                numberlist.append(diff.days)
    print(numberlist)
    if numberlist == []:
        print('There are no rare items tonight.')
        api.update_status(f"There are no rare items that have returned in the #Fortnite Item Shop of {currentdate}.")
        pass
    else:
        print('There are rare items tonight!')
        numberlist.sort()
        biggestnum = numberlist[-1]

        rarestitem = ''
        for i in resultlist:
            if i['lastseen_days'] == f'{biggestnum}':
                rarestitem += f"The rarest item is the {i['name']} {i['type']}, which hasn't been seen in {i['lastseen_days']} days!"

        tweetstring = "Rare items that have returned in tonight's #Fortnite Item Shop:\n\n"
        for i in resultlist:
            tweetstring += f"- {i['name']} ({i['lastseen_days']} days)\n"

        resultweet = f"{tweetstring}\n\n{rarestitem}"

        try:
            api.update_status(resultweet)
        except:
            api.update_status('There are rare items in the #Fortnite Item Shop tonight..\n\nHowever I am not able to post it as the tweet is too long. This means there are lots of rare cosmetics in the shop!')

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

                s = response.json()['data']
                featureditems = len(s['featured']['entries'])
                dailyitems = len(s['daily']['entries'])
                totalitems = featureditems+dailyitems

                print('\nTHE SHOP HAS UPDATED!')
                time.sleep(10)
                try:
                    shutil.rmtree('cache')
                    os.makedirs('cache')
                except:
                    os.makedirs('cache')
                genshop()

                if OGitemsbot is True:
                    ogitems()

                time.sleep(5)
                return main()
        
        else:
            print("FAILED TO GRAB SHOP DATA: URL DOWN")

        time.sleep(botDelay)

if updateMode == True:
    main()
else:
    genshop()
