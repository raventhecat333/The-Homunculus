import json
import os
import sys
import random
import aiohttp

import discord
from discord.ext import commands

# Only if you want to use variables that are in the config.json file.
if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)


# Here we name the cog and create a new class for the cog.
class testing(commands.Cog, name="testing"):
    def __init__(self, bot):
        self.bot = bot


  

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    @commands.command(name="poke")
    async def poke(self, ctx, *, args):
        """
        This is a testing command that does nothing.
        """
        # Do your stuff here
        userid = args
        await ctx.send(f"<@{userid}>")
        
    @commands.command(name="rpoke")
    async def poke(self, ctx, *, args):
        """
        This is a testing command that does nothing.
        """
        # Do your stuff here
        userid = args
        await ctx.send(f"<@&{userid}>")


        
# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(testing(bot))
