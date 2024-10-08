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
showItems = True # # Lets you know every time the program generates a cosmetic (used for debugging)
botDelay = 5

ToggleTweet = False # True means the program uses your Twitter API keys. False means it does not.
twitAPIKey = ''
twitAPISecretKey = ''
twitAccessToken = ''
twitAccessTokenSecret = '' 

# CHANGE UPDATE MODE TO FALSE IF "ToggleTweet" IS FALSE!!!
updateMode = False # False means it instantly tweets it, True means it keeps refreshing until shop updates

showData = True # Only used when ToggleTweet is "True", posts a tweet with extra shop information

CreatorCode = 'Fevers'

OGitemsbot = True
opitemdate = 180 # Threshold for classifying "Rare" items

archiveShop = True # If True, the program saves a copy of the Item Shop with the corresponding date
#===============#

if ToggleTweet == True:
    print("\n! ! ! TWEETING IS ON ! ! !\n")
    # V1 Tweepy
    auth = tweepy.OAuthHandler(twitAPIKey, twitAPISecretKey)
    auth.set_access_token(twitAccessToken, twitAccessTokenSecret)
    api = tweepy.API(auth, wait_on_rate_limit=True)


    # V2 Tweepy
    client = tweepy.Client(
        access_token=twitAccessToken,
        access_token_secret=twitAccessTokenSecret,
        consumer_key=twitAPIKey,
        consumer_secret=twitAPISecretKey,
        wait_on_rate_limit=True
        )

def compress():
    import math
    foo = Image.open("shop.jpg")
    x, y = foo.size
    x2, y2 = math.floor(x/2), math.floor(y/2)
    foo = foo.resize((x2,y2))
    foo.save("shop.jpg",quality=65)
    print('Compressed image!')

def genshop():

    print("Generating the Fortnite Item Shop.")

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
    if featured != None:
        for i in featured['entries']:

            if i['newDisplayAssetPath'] != None:
                if i['newDisplayAsset'] != None:
                    if i['newDisplayAsset']['materialInstances'] != []:
                        try:
                            url = i['newDisplayAsset']['materialInstances'][0]['images']['Background']
                        except:
                            url = i['newDisplayAsset']['materialInstances'][0]['images']['OfferImage']
                    else:
                        try:
                            url = i['newDisplayAsset']['renderImages'][0]['image']
                        except:
                            url = i['newDisplayAsset']['renderImages'][1]['image']
            else:
                url = i['items'][0]['images']['icon']

            name = i['items'][0]['id']
            last_seen = i['items'][0]['shopHistory']
            try:
                last_seen = last_seen[-2][:10]
            except:
                last_seen = 'NEW!'
            price = i['finalPrice']

            try: # Since fortnite removed bundles on some items for some reason
                if i['bundle'] != None:
                    url = i['bundle']['image']
                    filename = f"zzz{i['bundle']['name']}"
                    name = i['bundle']['name']
            except:
                filename = i['items'][0]['id'] # why not
                pass
            
            #if showItems != False:
            #    print("Loading... ")
            
            if last_seen != 'NEW!':
                dateloop = datetime.strptime(last_seen, "%Y-%m-%d")
                current = datetime.strptime(currentdate, "%Y-%m-%d")
                diff = str(current.date() - dateloop.date())
                #print("Diff 1:", diff)
                diff = diff.replace('days, 0:00:00', '')
                if diff == '0:00:00':
                    diff = '1'
            else:
                diff = 'NEW!'
            #print("Diff2:",diff)


            open(f'cache/{filename}.png', 'wb').write(requests.get(url).content)
            background = Image.open(f'cache/{filename}.png').resize((512, 512))
            background.save(f'cache/{filename}.png')

            img=Image.new("RGB",(512,512))
            img.paste(background)

            # OTHER ITEMS GEN
            try:
                if i['bundle'] == None:
                    if i['items'][1]:
                        url = i['items'][1]['images']['icon']
                        open(f'cache/temp{filename}.png', 'wb').write(requests.get(url).content)
                        background = Image.open(f'cache/temp{filename}.png').resize((80, 80))
                        background.save(f'cache/temp{filename}.png')
                    
                        background = Image.open(f'cache/temp{filename}.png')
                        img.paste(background, (0, 0), background)

                        os.remove(f'cache/temp{filename}.png')
                    if i['items'][2]:
                        url = i['items'][2]['images']['icon']
                        open(f'cache/temp{filename}.png', 'wb').write(requests.get(url).content)
                        background = Image.open(f'cache/temp{filename}.png').resize((80, 80))
                        background.save(f'cache/temp{filename}.png')
                    
                        background = Image.open(f'cache/temp{filename}.png')
                        img.paste(background, (0, 100), background)

                        os.remove(f'cache/temp{filename}.png')

                    if i['items'][3]:
                        url = i['items'][3]['images']['icon']
                        open(f'cache/temp{filename}.png', 'wb').write(requests.get(url).content)
                        background = Image.open(f'cache/temp{filename}.png').resize((80, 80))
                        background.save(f'cache/temp{filename}.png')
                    
                        background = Image.open(f'cache/temp{filename}.png')
                        img.paste(background, (0, 200), background)

                        os.remove(f'cache/temp{filename}.png')
            except:
                pass



            overlay = Image.open('overlay.png').convert('RGBA')
            img.paste(overlay, (0,0), overlay)

            img.save(f'cache/{filename}.png')

            background = Image.open(f'cache/{filename}.png')

            itemname = i['items'][0]['name']

            try: # Since fortnite removed bundles on some items for some reason again
                if i['bundle'] != None:
                    itemname = i['bundle']['name']
            except:
                itemname = i['items'][0]['name']
                pass

            if showItems != False:
                print("Loading... ", itemname)

            try: # Once again since fortnite is dumb
                if i['bundle'] != None:
                    itemname = f"{i['bundle']['name']}"
            except:
                pass
            
            font=ImageFont.truetype(loadFont,35)
            draw=ImageDraw.Draw(background)
            draw.text((256,420),itemname,font=font,fill='white', anchor='ms') # Writes name

            if 'NEW!' in diff:
                diff_text = 'NEW!'
            else:
                #diff = diff.replace(' ', '') ??????? WHY DID I INCLUDE THIS HELLO??????
                diff_text = f'LAST SEEN: {diff} days ago'

            if '0:00' in diff_text:
                diff_text = 'LAST SEEN: 1 day ago'

            font=ImageFont.truetype(loadFont,15)
            draw=ImageDraw.Draw(background)
            draw.text((256,450),diff_text,font=font,fill='white', anchor='ms') # Writes date last seen

            font=ImageFont.truetype(loadFont,40)
            draw=ImageDraw.Draw(background)
            draw.text((256,505),f'{price}',font=font,fill='white', anchor='ms') # Writes price

            background.save(f'cache/{filename}.png')

            if showItems != False:
                print(f'{diff_text}\n{name} - {price}\n')
                # Example: Last seen: 1 day ago then the name, price, etc. you get the rest.

            count += 1

    print(f'Done generating "{count}" items in the Featured section.')
    featrued_num = count
    print('')
    
    #########################

    totalnum = featrued_num
    print(f'\nGenerated {totalnum} items from the {currentdate} Item Shop.')

    print('\nMerging images...')
    from merger import merger
    merger(ogitems=False)

    end = time.time()

    print(f"IMAGE GENERATING COMPLETE - Generated image in {round(end - start, 2)} seconds!")

    img=Image.open(f'shop.jpg')
    img.show()

    s = response.json()['data']

    list = []

    if s['featured'] != None:
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
    
    if list != []:
        list.sort(reverse = True)
        maxitem = list[0]

        list.sort()
        minitem = list[0]

        average = sum(list) / len(list)
        average = round(average, 0)
    else:
        totalnum = "N/A"
        maxitem = "N/A"
        minitem = "N/A"
        average = "N/A"

    if showData == True:
        text = f'#Fortnite Item Shop update for {currentdate}!\n\nConsider using code "{CreatorCode}" to support me! #EpicPartner\n\nTotal Items: {totalnum}\nMax Last Seen: {maxitem} days\nMin Last Seen: {minitem} days\nAverage of Last Seen items: {average} days'
    else:
        text = f'#Fortnite Item Shop update for {currentdate}!\n\nConsider using code "{CreatorCode}" to support me! #EpicPartner'
    print(text)
    
    if ToggleTweet == True:
        try:
            try:
                media_id = api.media_upload(filename="shop.jpg").media_id
                shoptweet = client.create_tweet(text=text, media_ids=[media_id])
            except Exception as e:
                print(e)
        except:
            compress()
            try:
                media_id = api.media_upload(filename="shop.jpg").media_id
                shoptweet = client.create_tweet(text=text, media_ids=[media_id])
            except Exception as e:
                print(e)

        print('Tweeted!')
        print(f"Tweet ID: {shoptweet.data['id']}")

    list.clear()
    if OGitemsbot is True:
        print("Running OG Items bot")
        if ToggleTweet is True:
            ogitems(tweetID=shoptweet.data['id'])
        else:
            ogitems(tweetID=None)
    time.sleep(10)
    
def ogitems(tweetID):
    try:
        shutil.rmtree('ogcache')
        os.makedirs('ogcache')
    except:
        os.makedirs('ogcache')
    today = date.today()
    currentdate = today.strftime("%Y-%m-%d")
    response = requests.get('https://fortnite-api.com/v2/shop/br/combined')
    featured = response.json()['data']['featured']

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

    #print(numberlist) ([364, 364, 145, 132, 159, 298, 161])
    print('')
    if numberlist == []:
        print('There are no rare items tonight.')
        if ToggleTweet == True:
            client.create_tweet(text=f"There are no rare items (items that haven't been in the shop for {opitemdate} days) that have returned in the #Fortnite Item Shop of {currentdate}.", in_reply_to_tweet_id=tweetID)
        pass
    else:
        print('Rare cosmetics have been detected!')
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
        print(resultweet)

        for filename in os.listdir('cache'):
            for item in resultlist:
                if f"{item['id']}.png" == filename:
                    shutil.copy(f"cache/{filename}", f"ogcache/OG{filename}.png")
        from merger import merger
        merger(ogitems=True)
        print("Saved in this folder as 'OGitems'.\n")

        #   media_id = api.media_upload(filename="shop.jpg").media_id
        #   shoptweet = client.create_tweet(text=text, media_ids=[media_id])
        if ToggleTweet == True:
            media_id = api.media_upload(filename="OGitems.jpg").media_id
            client.create_tweet(text=f"There are {len(numberlist)} cosmetics that haven't been seen in {opitemdate} days!\n\n#Fortnite", media_ids=[media_id], in_reply_to_tweet_id=tweetID)
            print("Replied to original tweet with OG Item Bot.")
        else:
            pass


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

                time.sleep(5)
                return main()
        
        else:
            print("FAILED TO GRAB SHOP DATA: URL DOWN")

        time.sleep(botDelay)

if updateMode == True:
    main()
else:
    genshop()
