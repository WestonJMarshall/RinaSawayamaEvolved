# DiscordBot.py
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

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents().all()
client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='!',intents=intents)

q = Queue(maxsize = 16)
voice_channel = None

@bot.command(name='cringe')
async def cringe(ctx):
    response = '<:suffer:885330089523437638>'
    await ctx.send(response)

@bot.command(name='skip')
async def skip(ctx):
    await stop(ctx)
    await asyncio.sleep(1000)
    Check_Queue()


@bot.command(name='play', help='To play song')
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
    Remove()
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

def Remove():
    for file in glob.glob('*.m4a'):
        os.remove(file)
    for file in glob.glob('*.mp3'):
        os.remove(file)
    for file in glob.glob('*.webm'):
        os.remove(file)


@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client   

    if voice_client.is_playing():
        voice_client.stop()

    await voice_client.disconnect()
    await asyncio.sleep(1000)
    
    Remove()

@play.before_invoke
async def ensure_voice(ctx):
    if ctx.voice_client is None:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("You are not connected to a voice channel.")
            raise commands.CommandError("Author not connected to a voice channel.")
    elif ctx.voice_client.is_playing():
        ctx.voice_client.stop()


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



bot.run(TOKEN)