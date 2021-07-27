import asyncio
import json
import os
import random
import sys 

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import BucketType

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)


class Fun(commands.Cog, name="fun"):
    def __init__(self, bot):
        self.bot = bot

#class EmojiNotFound(commands.CommandError):
#    pass

    """
    Why 1 and 86400?
    -> Because the user should be able to use the command *once* every *86400* seconds
    
    Why BucketType.user?
    -> Because the cool down only affects the current user, if you want other types of cool downs, here are they:
    - BucketType.default for a global basis.
    - BucketType.user for a per-user basis.
    - BucketType.server for a per-server basis.
    - BucketType.channel for a per-channel basis.
    """

    @commands.command(name="dailyfact")
    @commands.cooldown(1, 86400, BucketType.user)
    async def dailyfact(self, context):
        """
        Get a daily fact, command can only be ran once every day per user.
        """
        # This will prevent your bot from stopping everything when doing a web request - see: https://discordpy.readthedocs.io/en/stable/faq.html#how-do-i-make-a-web-request
        async with aiohttp.ClientSession() as session:
            async with session.get("https://uselessfacts.jsph.pl/random.json?language=en") as request:
                if request.status == 200:
                    data = await request.json()
                    embed = discord.Embed(description=data["text"], color=0xD75BF4)
                    await context.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B
                    )
                    await context.send(embed=embed)
                    # We need to reset the cool down since the user didn't got his daily fact.
                    self.dailyfact.reset_cooldown(context)
    
    @commands.command()
    async def emoji(self, ctx, *, emote: discord.Emoji):
        """
        gives url to emote
        """
        ID = int(f'{emote.id}')
        Name = str(f'{emote.name}')
        server = str(f'{emote.guild}')
        if discord.ext.commands.errors.EmojiNotFound is True:
                    embed = discord.Embed(
                        title="Error!",
                        description="This emoji isnt useable by the bot, this may be fixed later",
                        color=0xE02B2B
                    )
                    await ctx.send(embed=embed)
        #ID = int(f'{emote.id}')
        elif emote.animated is True:
            ext = 'gif'
        else:
            ext = 'png'
            #ID = int(f'{emote.id}')
            #Name = str(f'{emote.name}')
            #server = str(f'{emote.guild}')
            #await ctx.send(f'https://cdn.discordapp.com/emojis/{ID}.png')
            #await ctx.send(f'{Name}')
            #await ctx.send(f'{server}')
        embed = discord.Embed(
            description="",
            color=0x42F56C
        )
        embed.set_author(
            name=f"{ctx.message.author}, Has requested information about this Emoji"
        )
        embed.set_image(url=f'https://cdn.discordapp.com/emojis/{ID}.{ext}')
        embed.add_field(
            name="Name:",
            value=f"{emote.name}",
            inline=True
        )
        embed.add_field(
            name="Emote ID:",
            value=f"{emote.id}",
            inline=True
        )
        embed.add_field(
            name="This Emoji is from:",
            value=f"{emote.guild}",
            inline=False
        )
        embed.set_footer(
            text=f"Requested by {ctx.message.author}"
        )
        await ctx.send(embed=embed)

    
    @commands.command(name="ask")
    async def ask(self, ctx, *, question):
        """
        yes no maybe
        """
        #picks random yes no or maybe
        #question = args 
        answers = ['Yes', 'No', 'Maybe', 'Yesn\'t']
        embed = discord.Embed(
            title="**My Answer:**",
            description=f"{answers[random.randint(0, len(answers))]}",
            color=0x42F56C
        )
        embed.set_footer(
            text=f"The question was: '{question}' "
        )
        await ctx.send(embed=embed) 
    
    
    #@commands.command()
    #async def avatar(self, ctx, *, pfp: discord.Member.avatar_url)
    
    
    @commands.command()
    async def img(self, ctx, args):
       imagename = args
       print(imagename)
       if imagename == 'waffle':
              embed = discord.Embed(
                  title="waffle",
                  description="",
                  color=0x42F56C
              )
              embed.set_image(url='https://preview.redd.it/m1poqb5acne51.png?auto=webp&s=90ad9df0965d0d5e5eaf67162827d1035542a37e')
       await ctx.send(embed=embed)

    
    @commands.command(name="rps")
    async def rock_paper_scissors(self, context):
        choices = {
            0: "rock",
            1: "paper",
            2: "scissors"
        }
        reactions = {
            "🪨": 0,
            "🧻": 1,
            "✂": 2
        }
        embed = discord.Embed(title="Please choose", color=0xF59E42)
        embed.set_author(name=context.author.display_name, icon_url=context.author.avatar_url)
        choose_message = await context.send(embed=embed)
        for emoji in reactions:
            await choose_message.add_reaction(emoji)

        def check(reaction, user):
            return user == context.message.author and str(reaction) in reactions

        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=10, check=check)

            user_choice_emote = reaction.emoji
            user_choice_index = reactions[user_choice_emote]

            bot_choice_emote = random.choice(list(reactions.keys()))
            bot_choice_index = reactions[bot_choice_emote]

            result_embed = discord.Embed(color=0x42F56C)
            result_embed.set_author(name=context.author.display_name, icon_url=context.author.avatar_url)
            await choose_message.clear_reactions()

            if user_choice_index == bot_choice_index:
                result_embed.description = f"**That's a draw!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = 0xF59E42
            elif user_choice_index == 0 and bot_choice_index == 2:
                result_embed.description = f"**You won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = 0x42F56C
            elif user_choice_index == 1 and bot_choice_index == 0:
                result_embed.description = f"**You won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = 0x42F56C
            elif user_choice_index == 2 and bot_choice_index == 1:
                result_embed.description = f"**You won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = 0x42F56C
            else:
                result_embed.description = f"**I won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = 0xE02B2B
                await choose_message.add_reaction("🇱")
            await choose_message.edit(embed=result_embed)
        except asyncio.exceptions.TimeoutError:
            await choose_message.clear_reactions()
            timeout_embed = discord.Embed(title="Too late", color=0xE02B2B)
            timeout_embed.set_author(name=context.author.display_name, icon_url=context.author.avatar_url)
            await choose_message.edit(embed=timeout_embed)


def setup(bot):
    bot.add_cog(Fun(bot))
