import discord
import logging
import datetime
import time
from datetime import date
from discord.ext import commands, tasks
from discord.ext.commands import Bot
date = date.today()
time = time.localtime()
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename=f'logs/discord.{date}.{time}.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
class logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
def setup(bot):
    bot.add_cog(logging(bot))
