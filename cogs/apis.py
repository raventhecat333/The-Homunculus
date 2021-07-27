import json
import os
import platform
import random
import sys
import time

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import Bot


class apis(commands.Cog, name="apis"):
    def __init__(self, bot):
        self.bot = bot
        



    @commands.command()
    async def quote(self, ctx):
        url = "https://animechan.vercel.app/api/random"
        async with aiohttp.ClientSession() as session:
            raw_response = await session.get(url)
            response = await raw_response.json()
            embed = discord.Embed(
                title=":information_source: Random Anime Quote", 
                color=0x42F56C
            )
            embed.add_field(
                name="Anime:",
                value=f'{response["anime"]}',
                inline=False
            )
            embed.add_field(
                name="Character:",
                value=f'{response["character"]}',
                inline=False
            )
            embed.add_field(
                name="Quote:",
                value=f'{response["quote"]}',
                inline=False
            )
            embed.set_footer(
                text=f"Requested by {ctx.message.author}"
            )
            await ctx.send(embed=embed)   

    @commands.command(name="bitcoin")
    async def bitcoin(self, context):
        """
        Get the current price of bitcoin.
        """
        url = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
        # Async HTTP request
        async with aiohttp.ClientSession() as session:
            raw_response = await session.get(url)
            response = await raw_response.text()
            response = json.loads(response)
            embed = discord.Embed(
                title=":information_source: Info",
                description=f"Bitcoin price is: ${response['bpi']['USD']['rate']}",
                color=0x42F56C
            )
            await context.send(embed=embed)

        
        





def setup(bot):
    bot.add_cog(apis(bot))
