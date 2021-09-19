# DiscordBot.py

#region Imports
from pathlib import Path
import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os.path
from os import path
import youtube_dl
import asyncio
import glob
from queue import Queue
#endregion


#region Startup & Globals
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents().all()
client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='!',intents=intents)

q = Queue(maxsize = 16)
voice_channel = None
#endregion


#region Response Commands
@bot.command(name='cringe')
async def cringe(ctx):
    response = '<:suffer:885330089523437638>'
    await ctx.send(response)

@bot.command(name='deleteF')
async def deleteF(ctx):
    response = 'Deleting'
    await ctx.send(response)
    Remove("DownloadsABC123/")
#endregion


#region Music Commands
@bot.command(name='skip')
async def skip(ctx):
    await stop(ctx)
    await asyncio.sleep(1000)
    Check_Queue()


@bot.command(name='play', help='Plays a song with a predownload from YouTube')
async def play(ctx,url):
    server = ctx.message.guild
    global voice_channel
    voice_channel = server.voice_client

    async with ctx.typing():
        filename = await YTDLSource.from_url(url, loop=bot.loop)
        q.put(filename)
        if(q.qsize() == 1 and not(voice_channel.is_playing())):
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=q.get()), after=lambda x: Check_Queue())
    await ctx.send('**Added Audio:** {}'.format(filename))

#@bot.command(name='stream', help='Streams a song directly from YouTube')
#async def stream(ctx, *, url):

    #async with ctx.typing():
        #player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)
        #ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

    #await ctx.send(f'Now playing: {player.title}')

def Check_Queue():

    #ctx.send("hit!")
    if(q.qsize() > 0):
        #server = ctx.message.guild
        #voice_channel = server.voice_client
        voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=q.get()), after=lambda x: Check_Queue())

@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")
    
@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play_song command")

@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")

@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    Remove("DownloadsABC123/")
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client   

    if voice_client.is_playing():
        voice_client.stop()

    await voice_client.disconnect()
    await asyncio.sleep(1000)
    
    Remove("DownloadsABC123/")

@play.before_invoke
async def ensure_voice(ctx):
    if (ctx.voice_client is None) or (ctx.voice_client.channel is not ctx.author.voice.channel):
        if ctx.author.voice:
            if ctx.voice_client is not None:
                await ctx.voice_client.disconnect()
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("You are not connected to a voice channel.")
            raise commands.CommandError("Author not connected to a voice channel.")
    elif ctx.voice_client.is_playing():
        ctx.voice_client.stop()
#endregion

#region Helper Functions
def Remove(path):
    #Check if folder path exists, create one if it doesn't
    root = Path().absolute()
    print(root)
    full = root.joinpath(path)
    print(full)
    if not(os.path.exists(full) and os.path.isdir(full)):
        print('No Downloads Folder')
        os.makedirs(full)
    #Delete all files in the path
    files = os.listdir(full)
    for file in files:
        fileFull = full.joinpath(file)
        print(fileFull)
        os.remove(fileFull)
    print('Complete')
#endregion


#region Youtube-DL Functionality
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'continue_dl': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192', }],
    'restrictfilenames': True,
    'noplaylist': True,
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
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        if(path.exists(data['title']) or path.exists(data['title'] + '.mp3')):
            filename = data['title']
        else:
            filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename.split('.')[0] + ".mp3"
#endregion


bot.run(TOKEN)