# DiscordBot.py

#region Imports
from random import randint
from RinasAssistant import *
#endregion

#region Startup & Globals
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SPOTIFY_ID = os.getenv('SPOTIFY_ID')
SPOTIFY_SECRET = os.getenv('SPOTIFY_SECRET')
atexit.register(HelperFunctions.exit_handler)

intents = discord.Intents().all()
client = discord.Client(intents=intents)
ffxivClient = pyxivapi.XIVAPIClient(api_key="baa9efb43d5940228cff609d8430cb7226461d8d92cf4a3dab95f3f7376f29ef")

bot = commands.Bot(command_prefix=['!','Rina-'], intents=intents)

q = Queue(maxsize = 32)
voice_channel = None
voiceCode = 'fr'
#endregion

MAX_PLAYLIST_SIZE = 20
nameQ = Queue(maxsize = MAX_PLAYLIST_SIZE)

ffmpeg_options = {
    'options': '-vn'
}

SPOTIFY_TOKEN = ''
SPOTIFY = ''

def spotify_token_retrieve():
    global SPOTIFY_TOKEN
    global SPOTIFY
    global SPOTIFY_ID
    global SPOTIFY_SECRET

    s = SPOTIFY_ID + ':' + SPOTIFY_SECRET
    s = s.encode('ascii')
    s = base64.b64encode(s)
    s = s.decode('ascii')
    rx = requests.post('https://accounts.spotify.com/api/token', headers={'Authorization':'Basic ' + s, 'Content-Type': 'application/x-www-form-urlencoded'},data={'grant_type':'client_credentials', 'scope':'streaming'})

    if rx.status_code == 200 or rx.status_code == 403:
        SPOTIFY_TOKEN = json.loads(rx.text)['access_token']

    auth_manager = SpotifyClientCredentials(SPOTIFY_ID, SPOTIFY_SECRET)
    SPOTIFY = spotipy.Spotify(auth_manager=auth_manager)

spotify_token_retrieve()

#region General Messages
@bot.event
async def on_message(message):
    if message.author == bot.user:
       return
    elif message.content.lower() == 'hello rina' or message.content.lower() == 'hey rina'or message.content.lower() == 'hi rina':

        responseArray = ['Hello ', 'Hey ', 'Hi ', 'heyyyyyyyyyyy ']

        text = responseArray[randint(0, len(responseArray) - 1)]

        id = message.author.id
        if id == 210798139320434690:
            text += "Weston "
        elif id == 178976168622424065:
            text += "Jacob "
        elif id == 181866295891984384:
            text += "Jack "    
        elif id == 199626966717038592:
            text += "Olive "
        elif id == 331608394203136003:
            text += "Abbi "

        emoteArray = ['😋','😊','😄','😂','😏']
        
        text += emoteArray[randint(0, len(emoteArray) - 1)]

        await message.channel.send(text)

    elif message.content.lower() == 'bye rina' or message.content.lower() == 'goodbye rina'or message.content.lower() == 'good bye rina':

        responseArray = ['Bye ', 'Goodbye ', 'Love you ', 'I will miss you ']

        text = responseArray[randint(0, len(responseArray) - 1)]

        id = message.author.id
        if id == 210798139320434690:
            text += "Weston "
        elif id == 178976168622424065:
            text += "Jacob "
        elif id == 181866295891984384:
            text += "Jack "    
        elif id == 199626966717038592:
            text += "Olive "
        elif id == 331608394203136003:
            text += "Abbi "

        emoteArray = ['😋','😊','😄','😂','😏']
        
        text += emoteArray[randint(0, len(emoteArray) - 1)]

        await message.channel.send(text)

    elif message.content.lower() == 'hewwo wina':

        responseArray = ['UwU hewwo ', 'OwO hewwo ']

        text = responseArray[randint(0, len(responseArray) - 1)]

        id = message.author.id
        if id == 210798139320434690:
            text += "Weston "
        elif id == 178976168622424065:
            text += "Jacob "
        elif id == 181866295891984384:
            text += "Jack "    
        elif id == 199626966717038592:
            text += "Olive "
        elif id == 331608394203136003:
            text += "Abbi "

        emoteArray = ['😽']
        
        text += emoteArray[randint(0, len(emoteArray) - 1)]

        await message.channel.send(text)

    await bot.process_commands(message)

# 178976168622424065 Jacob, Jack 181866295891984384, Olive 199626966717038592, Weston 210798139320434690, Abbi 331608394203136003
#@bot.event
#async def on_typing(channel, user, when):
    #if user.id == 178976168622424065:
        #message = await channel.send('I see you typing, Jacob 👀')
        #await asyncio.sleep(1.00)
        #await message.delete()
#endregion


#region Wikipedia

@bot.command(name='wiki')
async def wiki(ctx, *, text):  
    try:
        params = {
            'action': 'query',
            'list': 'search',
            'srsearch': text,
            'format': 'json'
        }

        api_url = "https://en.wikipedia.org/w/api.php"
        api_url = api_url + "?origin=*"
        for key in params.keys():
            api_url = api_url + '&' + key + '=' + params[key]

        r = requests.get(api_url)
        data = json.loads(r.text)

        resultNum = randint(0,len(data['query']['search']) - 1)

        if len(data['query']['search'][resultNum]['snippet']) > 2:
            result = cleanhtml(data['query']['search'][resultNum]['snippet'][0:1998], re.compile('<.*?>') )
            await ctx.send(result)
        else:
            await ctx.send('Snippet Error')
    except:
        await ctx.send('Wiki Error')

@bot.command(name='wiki-image')
async def wiki_image(ctx, *, text):  
    try:
        params = {
            'action': 'query',
            'list': 'allimages',
            'aiprefix': text,
            'format': 'json'
        }

        api_url = "https://en.wikipedia.org/w/api.php"
        api_url = api_url + "?origin=*"
        for key in params.keys():
            api_url = api_url + '&' + key + '=' + params[key]

        r = requests.get(api_url)
        data = json.loads(r.text)

        resultNum = randint(0,len(data['query']['allimages']) - 1)

        await ctx.send(data['query']['allimages'][resultNum]['url'])
    except:
        await ctx.send('🤪')

def cleanhtml(raw_html, cleaner):
    cleantext = re.sub(cleaner, '', raw_html)
    return cleantext

#endregion


#region ASCII ART

#@bot.command(name='ascii')
#async def ascii(ctx, *, text):  
#    try:
#        api_url = "http://api.textart.io/img2txt.json"
#        urllib.request.urlretrieve(text, filename) 
#
#        _body = {
#            'image': 'https://upload.wikimedia.org/wikipedia/en/0/04/SandC_Shame.jpg'
#        }
#
#        r = requests.post(api_url,data=_body)
#        data = json.loads(r.text)
#
#        await ctx.send(r.text)
#    except:
#        await ctx.send('No Image, try using dashes between words')

@bot.command(name='ascii')
async def ascii(ctx, *, text):  
    with webdriver.Chrome(executable_path=r'C:\Users\Administrator\Desktop\RinaSawayamaEvolved\RinaSawayamaEvolved\WebDriver\chromedriver.exe') as driver:
        await ctx.send("PROCESSING")
        wait = WebDriverWait(driver, 10)
        driver.get("https://www.ascii-art-generator.org/")

        driver.find_element(By.ID, "fileupfield-url").send_keys(text + Keys.TAB)

        driver.find_element(By.ID, "numberfield-width").send_keys("60" + Keys.TAB)

        driver.find_element(By.ID, "fbut").send_keys(Keys.ENTER)

        wait = WebDriverWait(driver, 10)
        notLoaded = True
        while notLoaded: #dont ever write something like this in real code it's awful
            try:
                driver.find_element(By.ID, "result-preview-wrap")
                notLoaded = False
            except:
                notLoaded = True

        el = driver.find_element(By.ID, "result-preview-wrap").text
        #txt = driver.find_element(By.ID, "result-preview-wrap")
        
        await ctx.send('```' + el[0:1960] + '```')
        #.send_keys("cheese" + Keys.RETURN)


@bot.command(name='cum-meter')
async def cum_meter(ctx):  
        recieved_message = (await ctx.channel.history(limit=2, oldest_first=False).flatten())[1]
        # 178976168622424065 Jacob, Jack 181866295891984384, Olive 199626966717038592, Weston 210798139320434690, Abbi 331608394203136003
        text = ''
        id = recieved_message.author.id
        if id == 210798139320434690:
            text += "Cum Level on Weston's message: "
        elif id == 178976168622424065:
            text += "Cum Level on Jacob's message: "
        elif id == 181866295891984384:
            text += "Cum Level on Jack's message: "    
        elif id == 199626966717038592:
            text += "Cum Level on Olive's message: "
        elif id == 331608394203136003:
            text += "Cum Level on Abbi's message: "
        else :
            text += "Cum Level on my message: "

        text += '\n'

        level = randint(1,20)

        for x in range(level):
            text += '⬜'

        for x in range(20 - level):
            text += '⬛' 

        text += ' ' + str(level * 5) + '%'

        await ctx.send(text)

@bot.command(name='hello')
async def hello(ctx):  
        # 178976168622424065 Jacob, Jack 181866295891984384, Olive 199626966717038592, Weston 210798139320434690, Abbi 331608394203136003
        text = 'Hello '
        id = ctx.author.id
        if id == 210798139320434690:
            text += "Weston "
        elif id == 178976168622424065:
            text += "Jacob"
        elif id == 181866295891984384:
            text += "Jack"    
        elif id == 199626966717038592:
            text += "Olive"
        elif id == 331608394203136003:
            text += "Abbi"
        else :
            text += ""

        text += '😊'

        await ctx.send(text)
#endregion


#region Response Commands
#https://gtts.readthedocs.io/en/latest/module.html#languages-gtts-lang
def do_tts(message):
	f = io.BytesIO()
	global voiceCode
	tts = gTTS(text=message.lower(), lang=voiceCode)
	tts.write_to_fp(f)
	f.seek(0)
	return f

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

@bot.command(name='horoscope')
async def horoscope(ctx, *, text):  
    try:
        api_url = "https://www.ganeshaspeaks.com/horoscopes/daily-horoscope/"
        api_url = api_url + text + '/'

        r = requests.get(api_url)
        data = r.text

        srch = '<p id="horo_content">'
        start = data.find(srch) + len(srch)
        end = data[start:len(data) - start].find('</p>')
        message = data[start:start + end]

        await ctx.send(text.upper() + '\n' + "Today's date: " + str(date.today()) + '\n' + message)
    except:
        await ctx.send('Whatever you typed in for the sign was wrong')

@bot.command(name='ffxiv-lore')
async def ffxivLore(ctx, *, text):
    global ffxivClient
    lore = await ffxivClient.lore_search(
    query=text,
    language="en"
    )
    if len(lore['Results']) > 0:
        await ctx.send(str(lore['Results'][random.randint(0,len(lore['Results']))]['Text'])[0:3200])
    else:
        await ctx.send("No results")

@bot.command(name='ffxiv-character')
async def ffxivCharacter(ctx, *, text):
    global ffxivClient
    character = await ffxivClient.character_search(
    world="sargatanas",
    forename=text.split()[0], 
    surname=text.split()[1]
    )
    if len(character['Results']) > 0:
        await ctx.send(character['Results'][0]['Avatar'])
    else:
        await ctx.send("No results")

@bot.command(name='slots')
async def slot(ctx): 
    emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
    a = random.choice(emojis)
    b = random.choice(emojis)
    c = random.choice(emojis)
    slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"
    if (a == b == c):
        await ctx.send(embed=discord.Embed.from_dict({"title":"Slot machine", "description":f"{slotmachine} All matchings, you won!"}))
    elif (a == b) or (a == c) or (b == c):
        await ctx.send(embed=discord.Embed.from_dict({"title":"Slot machine", "description":f"{slotmachine} 2 in a row, you won!"}))
    else:
        await ctx.send(embed=discord.Embed.from_dict({"title":"Slot machine", "description":f"{slotmachine} No match, you lost"}))

@bot.command(name='joke')
async def joke(ctx):  
    headers = {
        "Accept": "application/json"
    }

    api_url = "https://icanhazdadjoke.com"
    r = requests.get(api_url, headers=headers)
    joke = json.loads(r.text)['joke']

    await ctx.send(joke)

@bot.command(name='role')
async def role(ctx, *, text):

    if str(text).__contains__('d'):
        r = text.split('d')
        x = 0
        full = ""
        while x < int(r[0]):
            x += 1
            full += str(random.randint(1,int(r[1]))) + ', '
        embeded = discord.Embed(description='')
        embeded.add_field(name="Roles:", value=full[0:len(full) - 2])
        await ctx.send(embed=embeded)
    else:
        await ctx.send("Wrong format baka")

@bot.command(name='nani') #THIS CODE IS REALLY WRONG BUT ITS FUNNY
async def nani(ctx):
    api_url = "https://ranmoji.herokuapp.com/emojis/api/v.1.0/"
    response = requests.get(api_url)

    emojiHTMLEntity = json.loads(response.text)['emoji']

    emojiHTMLEntityHex = emojiHTMLEntity[3:len(emojiHTMLEntity) - 1].lower() + "0"
    emojiBytes = codecs.decode(emojiHTMLEntityHex, "hex")
    emojiUTF16 = emojiBytes.decode("utf-16", "ignore")

    await ctx.send(emojiUTF16)

@bot.command(name='random-word') #THIS CODE IS REALLY WRONG BUT ITS FUNNY
async def randomWord(ctx):
    RiTa = RiTaAccess()
    word = RiTa.randomWord()
    await ctx.send(word)

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

@bot.command(name='first-message')
async def first_message(ctx, channel: discord.TextChannel = None): 
    await ctx.message.delete()  
    if channel is None:
        channel = ctx.channel
    first_message = (await channel.history(limit=1, oldest_first=True).flatten())[0]
    embed = discord.Embed(description=first_message.content)
    embed.add_field(name="First Message", value=f"[Jump]({first_message.jump_url})")
    await ctx.send(embed=embed)

#endregion

@bot.command(name='tts')
async def tts(ctx, *, message):
    buff = do_tts(message)
    a_file=discord.File(buff, f"{message}.wav")

    byt = buff.getvalue()
    player = FFmpegPCMAudio_FIX(byt, pipe=True)

    server = ctx.message.guild
    global voice_channel
    voice_channel = server.voice_client

    global voiceCode
    await ctx.send('(Voice: ' + voiceCode +') ' + message)

    if not player == None:
        q.put(player)
        if(q.qsize() == 1 and not(voice_channel.is_playing())):
            voice_channel.play(source=q.get(), after=lambda x: check_queue(x))

@bot.command(name='set-voice')
async def set_voice(ctx, *, message):
    global voiceCode
    voiceCode = message
    if gtts.tts.tts_langs().__contains__(message):
        await ctx.send('Voice set to: ' + gtts.tts.tts_langs()[message])
    else:
        await ctx.send('No voice with that code')

@bot.command(name='get-voices')
async def get_voices(ctx):
    allVoices = ''
    for x in gtts.tts.tts_langs():
        allVoices += x + ' - ' + gtts.tts.tts_langs()[x] + '\n'
    embeded = discord.Embed(description=allVoices)
    await ctx.send(embed=embeded)

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
async def download(ctx, *,url):
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
async def play(ctx, *, url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"):
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

@bot.command(name='play-spotify', help='Streams a song directly from Spotify')
async def play_spotify(ctx, *, track):
    server = ctx.message.guild
    global voice_channel
    voice_channel = server.voice_client

    async with ctx.typing():
        player = await SpotifySource.from_track_name(track)
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
@tts.before_invoke
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
        #ytdl.cache.remove()
        voice_channel.play(source=q.get(), after=lambda x: check_queue(x))    
#endregion


#region Youtube-DL Functionality

ytdl_format_options = {
    'cachedir': False,
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': False,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

yt_dlp.utils.bug_reports_message = lambda: ''
ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, ctx, url, *, loop=None, stream=False):
        global ytdl
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download = not stream))
        if 'entries' in data:
            data = data['entries'] #THIS IS FOR PLAYLISTS, JUST LOOPS THE PLAY FUNCTION
            if len(data) < MAX_PLAYLIST_SIZE:
                for d in data:
                    nameQ.put(d['title'])
                    await play(ctx,url=d['url'])
            else:
                await ctx.send("Cannot load a playlist with more than 20 songs")
        else:
            filename = data['url'] if stream else ytdl.prepare_filename(data)
            ret = cls(FFmpegPCMAudio_FIX(filename, **ffmpeg_options), data=data)
            if ret.title == 'videoplayback':
                await asyncio.sleep(0.1) # FOR NAMING PLAYLIST SONGS
                ret.title = nameQ.get()
            return ret
#endregion

class SpotifySource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data['tracks']['items'][0]['name']
        self.url = data['tracks']['items'][0]['href']

    @classmethod
    async def from_track_name(cls, track):
        api_url = 'https://api.spotify.com/v1/search?type=track&include_external=audio&limit=1&q='
        api_url += track

        spotify_token_retrieve()

        response = requests.get(api_url,headers={'Authorization': 'Bearer ' + SPOTIFY_TOKEN, 'Content-Type': 'application/json'})
        data = json.loads(response.text)
        filename = data['tracks']['items'][0]['href']
        x = SPOTIFY.track(data['tracks']['items'][0]['id'])
        ret = cls(FFmpegPCMAudio_FIX(x['href'], **ffmpeg_options), data=data)
        return ret

@bot.command(name="commands", description="Returns all commands available")
async def commands(ctx):
    helptext = "```"
    strList = []
    for command in bot.commands:
        strList.append(command.qualified_name)
    helptext += 'COMMANDS:\n\n'
    for command in sorted(strList):
        helptext += f"{command}\n"
    helptext+="```"
    await ctx.send(helptext)

bot.run(TOKEN)


#Legacy Code V V V

@bot.command(name='member-ids')
async def member_ids(ctx):
    await ctx.message.delete()  
    channel = client.get_channel(846302309712789504) #gets the channel you want to get the list from

    members = channel.members #finds members connected to the channel

    memids = [] #(list)
    for member in members:
        memids.append(member.id)

    print(memids) #print info

@bot.command('get-channel')
async def get_channel(ctx, *, given_name=None):
    await ctx.message.delete()  
    for channel in ctx.guild.channels:
        if channel.name == given_name:
            wanted_channel_id = channel.id

    print(wanted_channel_id) # this is just to check 
