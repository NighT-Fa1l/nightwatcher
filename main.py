import discord
from discord.ext import commands
import os
import asyncio

import webserver

webserver.keep_alive()


intents = discord.Intents.all()
intents.members = True
intents.messages = True  # Enable message intents

bot = commands.Bot(command_prefix='!', intents=intents)

async def load_extensions():
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'commands.{filename[:-3]}')
                print(f'Loaded {filename}')
            except Exception as e:
                print(f'Failed to load {filename}: {e}')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_connect():
    await load_extensions()
bot.run(os.getenv("DISCORD_TOKEN"))


