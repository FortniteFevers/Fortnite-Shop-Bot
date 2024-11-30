# Configuration for Fortnite-Shop-Bot
# Created by Fevers

loadFont = 'BurbankBigRegular-BlackItalic.otf'  # File location the bot uses
debugItems = False  # Lets you know every time the program generates a cosmetic (used for debugging)
botDelay = 5  # Seconds the bot takes to update in updateMode

sideItemLoader = False # Toggles generating side items in the shop! Works with bundles and singular items. (Note: This increases loading time significantly)
showProgressBar = True  # Set to False to disable the progress bar

ToggleTweet = False  # True means the program uses your Twitter API keys. False means it does not.

twitAPIKey = ''  # DO NOT SHOW THIS KEY TO ANYONE
twitAPISecretKey = ''  # DO NOT SHOW THIS KEY TO ANYONE
twitAccessToken = ''  # DO NOT SHOW THIS KEY TO ANYONE
twitAccessTokenSecret = ''  # DO NOT SHOW THIS KEY TO ANYONE

# CHANGE UPDATE MODE TO FALSE IF "ToggleTweet" IS FALSE!!!
updateMode = False  # False means it instantly tweets it, True means it keeps refreshing until shop updates

showData = True  # Only used when ToggleTweet is "True", posts a tweet with extra shop information

CreatorCode = 'Fevers'  # Used for posting on Twitter :)

OGitemsbot = True
opitemdate = 180  # Threshold for classifying "Rare" items

archiveShop = True  # If True, the program saves a copy of the Item Shop with the corresponding date
