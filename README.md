# Fortnite-Shop-Bot
A bot to automatically post the Fortnite Item Shop to a Twitter / X. All assets belong to Epic Games.

## Features
- Fetches Item Shop data from [Fortnite API](https://fortnite-api.com/).
- Creates a visual representation of the shop items using **Pillow**.
- Compresses and archives images for future use.
- Posts updates to Twitter / X using **Tweepy**.
- Detects rare items based on last seen dates.
- Fully customizable via the `config.py` file, allowing you to edit API keys, bot delay, debug settings, Support-A-Creator code, and more.

--------------
> [!WARNING]  
> This branch is in **beta** and will have issues while running.

# How to Run

1. Make sure you have [Python 3.x](https://www.python.org/downloads/) installed on your computer.
2. Install all the required modules used in this program. Scroll below for the list.
3. Sign up for the [Twitter/X API program](https://developer.x.com/en/docs/platform-overview) and fill in your API keys within the `config.py` file.
4. If you want, you can edit other variables in `config.py`, such as the Support-A-Creator code, whether to print item data in the terminal, bot delay, etc.
5. Just run the `bot.py` file, and you're good to go!

# How to use Tweepy to post to Twitter / X
> [!NOTE]  
> If you **do not want** to use the Twitter / X capabilities of the program, change "ToggleTweet" to "False" & "UpdateMode" to "False" in `config.py`
*  In the User authentication settings of your application on the Developer Portal, make sure to edit your settings to what I have below:
*  Change your App permissions from *"Read"* to **"Read and write and Direct message"** (keep Request email from users off)
*  Change Type of App from *"Native App"* to **"Web App, Automated App or Bot"**
*  Under App info, change your "Callback URI / Redirect URL" to "https://localhost"
*  Under App info, change your "Website URL" to "https://localhost.com"

--------------

## Requirements
- Python 3.x
- Required libraries: `requests`, `Pillow`, `tweepy`, `shutil`, `datetime`, `os`, `time`

Install dependencies with:
```bash
pip install requests Pillow tweepy
```
--------------

# Example Image:
![Item Shop](https://pbs.twimg.com/media/GE-gTvBXUAAJnuJ?format=jpg&name=4096x4096)
