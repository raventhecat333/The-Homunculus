import json
import os
import platform
import random
import sys

import aiohttp
import discord
from discord import Webhook, AsyncWebhookAdapter

from discord.ext import commands

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

class webhook(commands.Cog, name="webhook"):
    def __init__(self, bot):
        self.bot = bot

@commands.command(name="foo")
async def foo(self, ctx):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url('https://discord.com/api/webhooks/855092235464605716/2Xna5suaREjOp2C15zdIa8N_nyEQ7WC2ILrvjixSu7gDijK42tdIuAxNYPxsH9N_h0Zi', adapter=AsyncWebhookAdapter(session))
        await webhook.send('Hello World', username='Foo')

        
                           
def setup(bot):
        bot.add_cog(webhook(bot))
