#import datetime
import json
import os
import sys
import time
#from datetime import time
import discord
from discord.ext import commands

from helpers import json_manager

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)


class owner(commands.Cog, name="owner"):
    def __init__(self, bot):
        self.bot = bot
        
        
        

   
    @commands.command()
    async def shutdown(self, context):
        """
        Make the bot shutdown
        """
        if context.message.author.id in config["owners"]:
            embed = discord.Embed(
                description="Shutting down. Bye! :wave:",
                color=0x42F56C
            )
            await context.send(embed=embed)
            #await context.message.delete()
            await self.bot.close()
        else:
            embed = discord.Embed(
                title="Error!",
                description="You don't have the permission to use this command.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
    
    

    
    
    @commands.command(name="whois")
    async def whois(self, ctx, *, member: discord.Member):
        """
        self explanatory
        """
        if ctx.message.author.id in config["owners"]:
                roles = [x.name for x in member.roles]
                role_length = len(roles)
                if role_length > 50:
                        roles = roles[:50]
                        roles.append(f">>>> Displaying[50/{len(roles)}] Roles")
                roles = ", ".join(roles)   
                ID = member.id
                name = member.name
                embed = discord.Embed(
                    description=f"Info about {name}",
                    color=0x42F56C   
                )
                embed.set_image(url=f"{member.avatar_url}")
                embed.add_field(
                name="Server Nickname:",
                value=f"{member.nick}",
                inline=True
                )
                embed.add_field(
                name="Roles:",
                value=f"{roles}",
                inline=True
                )
                embed.add_field(
                name="Joined at:",
                value=f"{member.joined_at}",
                inline=True
                )
                embed.add_field(
                name="Created at:",
                value=f"{member.created_at}",
                inline=True
                )
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Error!",
                description="You don't have the permission to use this command.",
                color=0xE02B2B
            )
            await ctx.send(embed=embed)
         
                
               
            
    
            
    @commands.command(name="say", aliases=["echo", "repeat"])
    async def say(self, context, *, args):
        """
        The bot will say anything you want.
        """
        if context.message.author.id in config["owners"]:
            await context.message.delete()
            await context.send(args)
        else:
            embed = discord.Embed(
                title="Error!",
                description="You don't have the permission to use this command.",
                color=0xE02B2B
            )
            await context.send(embed=embed)

    @commands.command(name="embed")
    async def embed(self, context, *, args):
        """
        The bot will say anything you want, but within embeds.
        """
        if context.message.author.id in config["owners"]:
            embed = discord.Embed(
                description=args,
                color=0x42F56C
            )
            await context.message.delete()
            await context.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Error!",
                description="You don't have the permission to use this command.",
                color=0xE02B2B
            )
            await context.send(embed=embed)

    @commands.group(name="blacklist")
    async def blacklist(self, context):
        """
        Lets you add or remove a user from not being able to use the bot.
        """
        if context.invoked_subcommand is None:
            with open("blacklist.json") as file:
                blacklist = json.load(file)
            embed = discord.Embed(
                title=f"There are currently {len(blacklist['ids'])} blacklisted IDs",
                description=f"{', '.join(str(id) for id in blacklist['ids'])}",
                color=0x0000FF
            )
            await context.send(embed=embed)
            
    @commands.command
    @blacklist.command(name="add")
    async def blacklist_add(self, ctx, *, member: discord.Member.id):
        """
        Lets you add a user from not being able to use the bot.
        """
        if context.message.author.id in config["owners"]:
            userID = member.id
            try:
                with open("blacklist.json") as file:
                    blacklist = json.load(file)
                if (userID in blacklist['ids']):
                    embed = discord.Embed(
                        title="Error!",
                        description=f"**{member.name}** is already in the blacklist.",
                        color=0xE02B2B
                    )
                    await context.send(embed=embed)
                    return
                json_manager.add_user_to_blacklist(userID)
                embed = discord.Embed(
                    title="User Blacklisted",
                    description=f"**{member.name}** has been successfully added to the blacklist",
                    color=0x42F56C
                )
                with open("blacklist.json") as file:
                    blacklist = json.load(file)
                embed.set_footer(
                    text=f"There are now {len(blacklist['ids'])} users in the blacklist"
                )
                await context.send(embed=embed)
            except:
                embed = discord.Embed(
                    title="Error!",
                    description=f"An unknown error occurred when trying to add **{member.name}** to the blacklist.",
                    color=0xE02B2B
                )
                await context.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Error!",
                description="You don't have the permission to use this command.",
                color=0xE02B2B
            )
            await context.send(embed=embed)

    @blacklist.command(name="remove")
    async def blacklist_remove(self, context, member: discord.Member = None):
        """
        Lets you remove a user from not being able to use the bot.
        """
        if context.message.author.id in config["owners"]:
            userID = member.id
            try:
                json_manager.remove_user_from_blacklist(userID)
                embed = discord.Embed(
                    title="User removed from blacklist",
                    description=f"**{member.name}** has been successfully removed from the blacklist",
                    color=0x42F56C
                )
                with open("blacklist.json") as file:
                    blacklist = json.load(file)
                embed.set_footer(
                    text=f"There are now {len(blacklist['ids'])} users in the blacklist"
                )
                await context.send(embed=embed)
            except:
                embed = discord.Embed(
                    title="Error!",
                    description=f"**{member.name}** is not in the blacklist.",
                    color=0xE02B2B
                )
                await context.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Error!",
                description="You don't have the permission to use this command.",
                color=0xE02B2B
            )
            await context.send(embed=embed)


def setup(bot):
    bot.add_cog(owner(bot))
