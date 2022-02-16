from RinasAssistant import *

q = Queue(maxsize = 32)
voice_channel = None
voiceCode = 'fr'

MAX_PLAYLIST_SIZE = 16
nameQ = Queue(maxsize = MAX_PLAYLIST_SIZE)

ffmpeg_options = {
    'options': '-vn'
}

class RinaAudio(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def skip(self, ctx):
        await self.pause(ctx)
        await asyncio.sleep(1)
        self.check_queue("Skipped")

    @commands.command()
    async def queue(self, ctx):
        s = 'Queued Items: \n'
        i = 0
        for qi in q.queue:
            i += 1
            s += '[' + str(i) + ']' + ' ' + qi.title + '\n'
        await ctx.send(s)

    @commands.command(name='play', help='Streams a song directly from YouTube')
    async def play(self, ctx, *, url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"):
        server = ctx.message.guild
        global voice_channel
        voice_channel = server.voice_client

        async with ctx.typing():
            player = await YTDLSource.from_url(ctx, self, url, loop=self.bot.loop, stream=True)
            if not player == None:
                q.put(player)
                if(q.qsize() == 1 and not(voice_channel.is_playing())):
                    await self.ensure_voice(ctx)
                    voice_channel.play(source=q.get(), after=lambda x: self.check_queue(x))
                await ctx.send('**Added Audio:** {}'.format(player.title))

    @commands.command(name='pause', help='This command pauses the song')
    async def pause(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            voice_client.pause()
        else:
            await ctx.send("The bot is not playing anything at the moment.")
        
    @commands.command(name='resume', help='Resumes the song')
    async def resume(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            await voice_client.resume()
        else:
            await ctx.send("The bot was not playing anything before this. Use play_song command")

    @commands.command(name='stop', help='Stops the song')
    async def stop(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            voice_client.stop()
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    @commands.command(name='join', help='Tells the bot to join the voice channel')
    async def join(self, ctx):
        if not ctx.message.author.voice:
            await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
            return
        else:
            channel = ctx.message.author.voice.channel
        await channel.connect()

    @commands.command(name='leave', help='To make the bot leave the voice channel')
    async def leave(self, ctx):
        voice_client = ctx.message.guild.voice_client   

        if voice_client.is_playing():
            voice_client.stop()

        await voice_client.disconnect()
        await asyncio.sleep(1)

    #https://gtts.readthedocs.io/en/latest/module.html#languages-gtts-lang
    def do_tts(self, message):
        f = io.BytesIO()
        global voiceCode
        tts = gTTS(text=message.lower(), lang=voiceCode)
        tts.write_to_fp(f)
        f.seek(0)
        return f

    @commands.command()
    async def tts(self, ctx, *, message):
        buff = self.do_tts(message)
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
                voice_channel.play(source=self.q.get(), after=lambda x: self.check_queue(x))

    @commands.command(name='set-voice')
    async def set_voice(self, ctx, *, message):
        global voiceCode
        voiceCode = message
        if gtts.tts.tts_langs().__contains__(message):
            await ctx.send('Voice set to: ' + gtts.tts.tts_langs()[message])
        else:
            await ctx.send('No voice with that code')

    @commands.command(name='get-voices')
    async def get_voices(self, ctx):
        allVoices = ''
        for x in gtts.tts.tts_langs():
            allVoices += x + ' - ' + gtts.tts.tts_langs()[x] + '\n'
        embeded = discord.Embed(description=allVoices)
        await ctx.send(embed=embeded)

    @play.before_invoke
    @tts.before_invoke
    async def ensure_voice(self, ctx):
        if (ctx.voice_client is None) or (ctx.voice_client.channel is not ctx.author.voice.channel):
            if ctx.author.voice:
                if ctx.voice_client is not None:
                    await ctx.voice_client.disconnect()
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")

    def check_queue(self, x):
        print(x)
        if(q.qsize() > 0):
            voice_channel.play(source=q.get(), after=lambda x: self.check_queue(x))    

ytdl_format_options = {
    'cachedir': False,
    'format': '250',
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

ytdl_format_options_BACKUP = {
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
        self.title = data.get('title') + '\n [[Duration: ' + str(data.get('duration') / 60).split('.')[0] + ':' + str(data.get('duration') % 60)[0:2] + ']]'
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, caller, ctx, url, *, loop=None, stream=False):
        try:
            global ytdl
            loop = loop or asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download = not stream))
            if 'entries' in data and len(data['entries']) == 1:
                data = data['entries'][0]
            if 'entries' in data:
                data = data['entries'] #THIS IS FOR PLAYLISTS, JUST LOOPS THE PLAY FUNCTION
                if len(data) < MAX_PLAYLIST_SIZE:
                    for d in data:
                        nameQ.put(d['title'])
                        await caller.play(ctx,url=d['url'])
                else:
                    await ctx.send("Cannot load a playlist with more than 20 songs")
            else:
                filename = data['url'] if stream else ytdl.prepare_filename(data)
                if data['duration'] > 850:
                    ret = cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
                else:
                    ret = cls(FFmpegPCMAudio_FIX(filename, **ffmpeg_options), data=data)
                if ret.title == 'videoplayback':
                    await asyncio.sleep(0.1) # FOR NAMING PLAYLIST SONGS
                    ret.title = nameQ.get()
                return ret
        except Exception as e: #BACKUP WITH LESS STRICT SETTINGS
            try:
                await ctx.send('running backup...')
                if str(e).__contains__('Requested format is not available'):
                    tdlTEMP = yt_dlp.YoutubeDL(ytdl_format_options_BACKUP)
                    loop = loop or asyncio.get_event_loop()
                    data = await loop.run_in_executor(None, lambda: tdlTEMP.extract_info(url, download = not stream))
                    if 'entries' in data and len(data['entries']) == 1:
                        data = data['entries'][0]
                    if 'entries' in data:
                        data = data['entries'] #THIS IS FOR PLAYLISTS, JUST LOOPS THE PLAY FUNCTION
                        if len(data) < MAX_PLAYLIST_SIZE:
                            for d in data:
                                nameQ.put(d['title'])
                                await caller.play(ctx,url=d['url'])
                        else:
                            await ctx.send("Cannot load a playlist with more than 20 songs")
                    else:
                        filename = data['url'] if stream else tdlTEMP.prepare_filename(data)
                        if data['duration'] > 520:
                            ret = cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
                        else:
                            ret = cls(FFmpegPCMAudio_FIX(filename, **ffmpeg_options), data=data)
                        if ret.title == 'videoplayback':
                            await asyncio.sleep(0.1) # FOR NAMING PLAYLIST SONGS
                            ret.title = nameQ.get()
                        return ret
            except Exception as e:
                await ctx.send("Can't load song :(")

            
