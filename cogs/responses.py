import json
import os
import sys

from discord.ext import commands

# Only if you want to use variables that are in the config.json file.
if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)


# Here we name the cog and create a new class for the cog.
class responses(commands.Cog, name="responses"):
    def __init__(self, bot):
        self.bot = bot

    # why did i make this?
    @commands.command(name="")
    async def adventurer(self, ctx, *, args):
        """
        i used to be a {thing} like you till a took an arrow to the knee
        """
        # Do your stuff here
        thing = args
        await ctx.send(f"i used to be a/an {thing} like you till a took a arrow to the knee")
        
# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(responses(bot))
