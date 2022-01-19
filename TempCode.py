




from RinaModules import *

rinaWordle = RinaWordle(bot,5)

"""
@bot.command(name='wordle', help='Play Wordle')
async def wordle(ctx):
    await rinaWordle.wordle_start(ctx)

@bot.command(name='guess', help='End Wordle')
async def wordle_guess(ctx, * ,text):
    await rinaWordle.wordle_guess(ctx, text = text)
"""



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