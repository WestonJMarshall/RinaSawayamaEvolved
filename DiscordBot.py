from RinaModules import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents().all()
client = discord.Client(intents=intents)
ffxivClient = pyxivapi.XIVAPIClient(api_key="baa9efb43d5940228cff609d8430cb7226461d8d92cf4a3dab95f3f7376f29ef")

bot = commands.Bot(command_prefix=['!','Rina-'], intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="with Dennis"))

@bot.event
async def on_message(message):
    if message.author == bot.user:
       return
    elif message.content.lower() == 'hello rina' or message.content.lower() == 'hey rina'or message.content.lower() == 'hi rina':

        responseArray = ['Hello ', 'Hey ', 'Hi ', 'heyyyyyyyyyyy ']

        text = responseArray[randint(0, len(responseArray) - 1)]

        id = message.author.id
        text += id_name_split(id) + ' '

        emoteArray = ['😋','😊','😄','😂','😏','😍']
        
        text += emoteArray[randint(0, len(emoteArray) - 1)]

        await message.channel.send(text)

    elif message.content.lower() == 'bye rina' or message.content.lower() == 'goodbye rina'or message.content.lower() == 'good bye rina':

        responseArray = ['Bye ', 'Goodbye ', 'Love you ', 'I will miss you ', 'bye bye ', 'bye bye ']

        text = responseArray[randint(0, len(responseArray) - 1)]

        id = message.author.id
        text += id_name_split(id) + ' '

        emoteArray = ['😋','😊','😄','😂','😏','😅','😍','😞','😢','😣','😨','😭', '🅱', '⁉']
        
        text += emoteArray[randint(0, len(emoteArray) - 1)]

        await message.channel.send(text)

    elif message.content.lower() == 'hewwo wina' or message.content.lower() == 'hewwo rina':

        responseArray = ['UwU hewwo ', 'OwO hewwo ', 'I think this is a little cringe ']

        text = responseArray[randint(0, len(responseArray) - 1)]

        id = message.author.id
        text += id_name_split(id) + ' '

        emoteArray = ['😽']
        
        text += emoteArray[randint(0, len(emoteArray) - 1)]

        await message.channel.send(text)

    elif message.content.lower().__contains__('thank you rina') or message.content.lower().__contains__('thanks rina') or message.content.lower().__contains__('thankyou rina'):

        responseArray = ['... ']

        text = responseArray[randint(0, len(responseArray) - 1)]

        #id = message.author.id
        #text += id_name_split(id) + ' '

        emoteArray = ['🌚']
        
        text += emoteArray[randint(0, len(emoteArray) - 1)]

        await message.channel.send(text)

    await bot.process_commands(message)

def id_name_split(id):
    text = ''
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
    return text

bot.add_cog(RinaCore(bot))
bot.add_cog(RinaFinalFantasy(bot, ffxivClient))
bot.add_cog(RinaAudio(bot))
bot.add_cog(RinaWordle(bot))
bot.add_cog(RinaScrabble(bot))

try:
    bot.loop.run_until_complete(bot.start(TOKEN))
except KeyboardInterrupt:
    bot.loop.run_until_complete(bot.close())
finally:
    bot.loop.close()




