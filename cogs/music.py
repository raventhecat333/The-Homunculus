import asyncio

import discord
import youtube_dl

from discord.ext import commands, tasks
from discord.ext.commands import Bot

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

#%(extractor)s-%(id)s-
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return ctx.author.voice_client.move_to()


        await ctx.author.voice.channel.connect()
        channel = ctx.author.voice_channel
        await ctx.send(f"joined {channel}")
        return
        
    #@slash.slash()
    #async def join(self, ctx):
    #    """Joins a voice channel"""

    #    if ctx.voice_client is not None:
    #        return ctx.author.voice_client.move_to()


    #    await ctx.author.voice.channel.connect()
    #    channel = ctx.author.voice_channel
    #    await ctx.send(f"joined {channel}")
    #    return

    @commands.command()
    async def move(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel regardless of the channel you are in"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def play(self, ctx, *, query):
        """Plays a file from the local filesystem (this command is broken, idfk why but it is sorry lol"""

        #source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        #ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)

        #await ctx.send(f'Now playing: {query}')
        await ctx.send("command doesnt work for some reason sorry")

    @commands.command()
    async def yt(self, ctx, *, url):
        """Plays from a url (almost anything youtube_dl supports)"""
        playing = ctx.voice_client.is_playing()
        if playing is True:
            return await ctx.send("a song is currently playing please wait")
        else:
            async with ctx.typing():
                player = await YTDLSource.from_url(url, loop=self.bot.loop)
                ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
        await ctx.send(f'Now playing: {player.title}')
   

    
    
    
    @commands.command()
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""
        playing = ctx.voice_client.is_playing()
        if playing is True:
            await ctx.send("a song is currently playing please wait")
            return
        else:
            async with ctx.typing():
               player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
               ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {player.title}')

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")
        await ctx.invoke(volumechecker)
        
        
    @commands.command(invoke_without_command=True)
    async def volumechecker(self, ctx): 
        """runs after volume to check"""
        
        
        limit = 2
        volume = ctx.voice_client.source.volume
        if volume > limit:
           ctx.voice_client.source.volume = 1
           return await ctx.send(f"error reseting volume to {limit}%")

    @commands.command()
    async def pause(self, ctx):
        """pauses music"""
        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        await ctx.send(":pause_button: Paused!")
        await ctx.voice_client.pause()
    
    @commands.command()
    async def nowplaying(self, ctx):
        """
        returns name of current song
        """
        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")
        await ctx.send(f'{player.title}')

              
    @commands.command()
    async def resume(self, ctx):
        """
        resumes playback
        """
        await ctx.send(":play_button: Resuming!")
        await ctx.voice_client.resume()

    @commands.command(name="disconnect", aliases=["dc", "leave", "stop", "fuckoff"])
    async def disconnect(self, ctx):
        """Stops and disconnects the bot from voice"""
        await ctx.voice_client.disconnect()
        await ctx.send(":wave: Disconnected!")


    @play.before_invoke
    @yt.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                   description='Relatively simple music player')

def setup(bot):
        bot.add_cog(music(bot))
