import discord, random, re
#from discord import Message
import datetime
import time
import discord.ext.commands
from discord.ext import commands
from discord.ext.commands import Bot

        
class msglogging(commands.Cog, name="messagelogging"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        ctn = message.clean_content
        athr = message.author
        chnnl = message.channel
        gld = message.guild
        t = time.localtime()
        tod = time.strftime("%H:%M:%S", t)
        f = open("log.txt", "a")
        f.write(f"{ctn}: sent by: {athr} at {tod} in {chnnl} https://discord.com/channels/{gld.id}/{chnnl.id}/{message.id} ")


def setup(bot):
    bot.add_cog(msglogging(bot))
