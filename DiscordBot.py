# DiscordBot.py

#region Imports
from RinasAssistant import *
#endregion

#region Startup & Globals
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
atexit.register(HelperFunctions.exit_handler)

intents = discord.Intents().all()
client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='!', intents=intents)

q = Queue(maxsize = 32)
voice_channel = None
#endregion


#region Response Commands
@bot.command(name='cringe')
async def cringe(ctx):
    response = '<:suffer:885330089523437638>'
    await ctx.send(response)

@bot.command(name='spongebob')
async def spongebob(ctx, *, text):
    response = ""
    isLower = not text[0].islower()
    for c in text:
        num = random.random()
        if num >= 0.9:                          #10% chance to have two lower/upper characters in a row
            if isLower:
                response += c.lower()
            else:
                response += c.upper()
        elif isLower:                           #if the last char was lower, it swaps to upper
            response += c.upper()
            isLower = False
        else:                                   #if the last char was upper, it swaps to lower
            response += c.lower()
            isLower = True
    await ctx.send(response)

@bot.command(name='nani') #THIS CODE IS REALLY WRONG BUT ITS FUNNY
async def nani(ctx):
    api_url = "https://ranmoji.herokuapp.com/emojis/api/v.1.0/"
    response = requests.get(api_url)

    emojiHTMLEntity = json.loads(response.text)['emoji']

    emojiHTMLEntityHex = emojiHTMLEntity[3:len(emojiHTMLEntity) - 1].lower() + "0"
    emojiBytes = codecs.decode(emojiHTMLEntityHex, "hex")
    emojiUTF16 = emojiBytes.decode("utf-16", "ignore")

    await ctx.send(emojiUTF16)

@bot.command(name='current-emotion')
async def emotion(ctx):
    """
    Overview: Take an html hex code for an emoji from an api endpoint,
    convert it to utf-16, and then send it to be displayed as an emote in Discord
    
    The endpoint that is currently being used is https://ranmoji.herokuapp.com/emojis/api/v.1.0/
    This endpoint returns an emoji in a way that an HTML web page would read and then render them.
    Every emoji has a codepoint. A codepoint is just the utf-8 code for a character within the utf-8 character set
    However, if we want to take an emoji's data and then have it be rendered, we need to know what
    data format our destination uses to render emojis. HTML uses 'HTML hex' written in this format &#xnnnnn;. (n = number or letter, the n's will be the codepoint)
    For Discord, we need to add a utf-8 character to a utf-8 string. That character is derived from the base 10 version
    of the hexidecimal code point because there is no easy hexidecimal data type here in Python. So we
    convert our base 16 hex code into a base 10 decimal code and then the chr() command converts that into a 
    single utf-8 character for us instead of it being like a 6 digit integer. 

    ALSO we access our API endpoint using a GET request, and we use the requests library to help with that.
    GET returns JSON data which we parse for the 'emoji' field, whose value is the HTML hex data.
    Finally we need to strip off the HTML stuff on what we get, so we take off the &,#, and ;, and add a 0 to the front, 
    and then we have the hexidecimal code we can convert
    """
    api_url = "https://ranmoji.herokuapp.com/emojis/api/v.1.0/"
    response = requests.get(api_url)

    emojiHTMLEntity = json.loads(response.text)['emoji']
    emojiHTMLEntityHex = '0' + emojiHTMLEntity[2:len(emojiHTMLEntity) - 1].lower()

    emoji = ""
    try:
        emoji = chr(int(emojiHTMLEntityHex,16))
    except:
        emoji = "Whoops I'm an idiot!"

    await ctx.send(emoji)

@bot.command(name='random-character')
async def randomChar(ctx):
    #Generates a random 4 digit hex code that will map to some symbol in the utf-8 character set
    numCharMap = {1 : 'A', 2 : 'B', 3 : 'C', 4 : 'D', 5 : 'E', 6 : 'F'}
    charVals = ["0","0","0","0"]

    for c in charVals:
        if(random.randint(0,1) == 1):
            c = str(random.randint(0,9))
        else:
            c = numCharMap[random.randint(1,6)]
    
    emojiHTMLEntityHex = "0x" + charVals[0] + charVals[1] + charVals[2] + charVals[3]
    emoji = chr(int(emojiHTMLEntityHex,16))

    await ctx.send(emoji)

#endregion


#region Music Commands
@bot.command(name='skip')
async def skip(ctx):
    await pause(ctx)
    await asyncio.sleep(1)
    check_queue("Skipped")

@bot.command(name='queue')
async def queue(ctx):
    s = 'Queued Items: \n'
    i = 0
    for qi in q.queue:
        i += 1
        s += '[' + str(i) + ']' + ' ' + qi.title + '\n'
    await ctx.send(s)

@bot.command(name='download', help='Plays a song with a predownload from YouTube')
async def download(ctx,url):
    server = ctx.message.guild
    global voice_channel
    voice_channel = server.voice_client

    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=bot.loop)
        if not player == None:
            q.put(player)
            if(q.qsize() == 1 and not(voice_channel.is_playing())):
                voice_channel.play(source=q.get(), after=lambda x: check_queue(x))
            await ctx.send('**Added Audio:** {}'.format(player.title))

@bot.command(name='play', help='Streams a song directly from YouTube')
async def play(ctx, *, url):
    server = ctx.message.guild
    global voice_channel
    voice_channel = server.voice_client

    async with ctx.typing():
        player = await YTDLSource.from_url(ctx, url, loop=bot.loop, stream=True)
        if not player == None:
            q.put(player)
            if(q.qsize() == 1 and not(voice_channel.is_playing())):
                voice_channel.play(source=q.get(), after=lambda x: check_queue(x))
            await ctx.send('**Added Audio:** {}'.format(player.title))

@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        voice_client.pause()
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
        voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")

@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
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
    await asyncio.sleep(1)
    
@play.before_invoke
@download.before_invoke
async def ensure_voice(ctx):
    if (ctx.voice_client is None) or (ctx.voice_client.channel is not ctx.author.voice.channel):
        if ctx.author.voice:
            if ctx.voice_client is not None:
                await ctx.voice_client.disconnect()
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("You are not connected to a voice channel.")
            raise commands.CommandError("Author not connected to a voice channel.")
#endregion


#region Helper Functions
def check_queue(x):
    print(x)
    if(q.qsize() > 0):
        voice_channel.play(source=q.get(), after=lambda x: check_queue(x))    
#endregion


#region Youtube-DL Functionality
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': 'TempDownloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'quiet': True,
    'no_warnings': True,
    'source_address': '0.0.0.0',
    'cachedir': False
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
    async def from_url(cls, ctx, url, *, loop=None, stream=False):
        #youtube-dl --rm-cache-dir
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            data = data['entries'] #THIS IS FOR PLAYLISTS, JUST LOOPS THE PLAY FUNCTION
            if len(data) < 20:
                for d in data:
                    await play(ctx,url=d['url'])
            else:
                await ctx.send("Cannot load a playlist with more than 20 songs")
        else:
            filename = data['url'] if stream else ytdl.prepare_filename(data)
            ret = cls(discord.FFmpegPCMAudio(filename), data=data)
            if ret.title == 'videoplayback':
                await asyncio.sleep(0.5) # FOR NAMING PLAYLIST SONGS
                ret.title = 'Playlist Song #' + str(q.qsize())
            return ret
#endregion

bot.run(TOKEN)

