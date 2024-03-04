import os, requests, re, discord

from bs4 import BeautifulSoup
from discord import Intents
from dotenv import load_dotenv

## load the discord token from the .env file (acts like a key)
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client(intents=Intents.default())
overview = requests.get('https://tracker.gg/valorant/profile/riot/Swoof%23NBA/overview')

if overview.status_code == 200:

    ## parsing html
    soup = BeautifulSoup(overview.text, "html.parser")
    stats = soup.body.get_text().strip()

    ## scraping valorant data
    views = re.search(r'Claim Profile\d+,\d+', stats).group(0).replace('Claim Profile', '')
    
    rankrr_match = re.search(r'Current Rating([^\d]+)(\d+)', stats)
    if rankrr_match:
        rank = rankrr_match.group(1).strip() + " " + rankrr_match.group(2)[:1]
        rr = rankrr_match.group(2)[1:4]
    else:
        rank = "unknown D:"
        rr = "unknown too D:"

    games_match = re.search(r'(\d+)\s+Matches', stats)
    if games_match:
        games = int(games_match.group(1))
    else:
        games = "an unknown amount of "   
    
    time = re.search(r'\d+', re.search(r'\d+h Playtime', stats).group(0)).group(0)

    ## summary message ready for discord
    msg = "Swoof has spent this act playing " + str(games) + " games and is currently hardstuck " + rank + " " + rr + "RR.\nThis is a total of " + time + " hours or " + str(int(round(int(time)/24, 0))) + " days and his profile has been viewed " + views + " times."

## pinged message when joining the server (only for local testing)
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

## everytime a message is sent, check for possible replies
@client.event
async def on_message(message):
    ## if lina is typed anytime, let them know thats alec's mum!
    if 'lina' in message.content.lower():
        await message.channel.send(f'Thats my mum!')
    ## if the bot is mentioned by anyone in the server, send the summary message
    elif client.user in message.mentions:
        await message.channel.send(msg)

client.run(TOKEN)
