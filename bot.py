import os

import discord
from discord.ext import commands
import aiohttp
import schedule
import time
from constants import URL, ANNOUNCE_CHN_ID  # Import the URL list from constants.py
from utils import fetch_notifications  # Import your fetch_notifications function

TOKEN = open('data/TOKEN.txt', 'r').readline().strip()

intents = discord.Intents.default()  # even default is more than we actually need
intents.members = True  # For AoC
bot = commands.Bot(command_prefix=";", intents=intents, owner_ids=[626478697003614219, 626853992051507231, 623559936470941727, 267257940740800512])
bot.remove_command('help')


async def create_aiohttp_session():
    bot.aiohttp_session = aiohttp.ClientSession(loop=bot.loop)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print('------')


for cog in os.listdir("./cogs"):
    if cog.endswith(".py") and not cog.startswith("_"):
        try:
            cog = f"cogs.{cog.replace('.py', '')}"
            bot.load_extension(cog)
        except Exception as e:
            print(f"{cog} can not be loaded:")
            raise e
bot.load_extension("jishaku")

bot.loop.run_until_complete(create_aiohttp_session())

# Schedule the announcement checking function
async def check_announcements():
    aiohttp_session = bot.aiohttp_session
    announcements = await fetch_notifications(aiohttp_session)
    
    # Process announcements here
    if announcements:
        for title, link in announcements:
            # Send notifications or perform other actions
            channel = bot.get_channel(ANNOUNCE_CHN_ID)
            if channel:
                await channel.send(f"New Announcement: {title}\n{link}")

# Schedule the function to run every 1 hour
schedule.every(1).hours.do(check_announcements)

# Run the scheduler loop
while True:
    schedule.run_pending()
    time.sleep(1)
    
# Run the bot
bot.run(TOKEN)
