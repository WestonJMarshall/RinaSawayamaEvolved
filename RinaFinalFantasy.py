from RinasAssistant import *

class RinaFinalFantasy(commands.Cog):
    def __init__(self, bot, ffxivClient):
        self.ffxivClient = ffxivClient
        self.bot = bot
    
    @commands.command(name='ffxiv-lore')
    async def ffxivLore(self, ctx, *, text):
        global ffxivClient
        lore = await self.ffxivClient.lore_search(
        query=text,
        language="en"
        )
        if len(lore['Results']) > 0:
            await ctx.send(str(lore['Results'][random.randint(0,len(lore['Results']))]['Text'])[0:3200])
        else:
            await ctx.send("No results")

    @commands.command(name='ffxiv-character')
    async def ffxivCharacter(self, ctx, *, text):
        global ffxivClient
        character = await self.ffxivClient.character_search(
        world="sargatanas",
        forename=text.split()[0], 
        surname=text.split()[1]
        )
        if len(character['Results']) > 0:
            await ctx.send(character['Results'][0]['Avatar'])
        else:
            await ctx.send("No results")