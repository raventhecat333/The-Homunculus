import json
import os
import platform
import random
import sys

import aiohttp
import discord

from discord.ext import commands        

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)


class reply(commands.Cog, name="reply"):
    def __init__(self, bot):
        self.bot = bot
        
async def on_message(self, *, ctx):
        # we do not want the bot to reply to itself
        if message.content('hello'):
            await ctx.author.reply.send('Hello!', mention_author=False)

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                   description='Relatively simple music player')

def setup(bot):
        bot.add_cog(reply(bot))
