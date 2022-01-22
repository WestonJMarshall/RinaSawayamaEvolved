from RinasAssistant import *

class RinaCore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def status(self, ctx, *, text):  
        await self.bot.change_presence(activity=discord.Game(name=text))

    @commands.command()
    async def wiki(self, ctx, *, text):  
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
                result = self.cleanhtml(data['query']['search'][resultNum]['snippet'][0:1998], re.compile('<.*?>') )
                await ctx.send(result)
            else:
                await ctx.send('Snippet Error')
        except:
            await ctx.send('Wiki Error')

    @commands.command()
    async def wiki_image(self, ctx, *, text):  
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

    @commands.command()
    async def ascii(self, ctx, *, text):  
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


    @commands.command(name='cum-meter')
    async def cum_meter(self, ctx):  
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

            level = randint(0,20)

            for x in range(level):
                text += '⬜'

            for x in range(20 - level):
                text += '⬛' 

            text += ' ' + str(level * 5) + '%'

            await ctx.send(text)

    @commands.command()
    async def cringe(self, ctx):
        response = '<:suffer:885330089523437638>'
        await ctx.send(response)

    @commands.command()
    async def spongebob(self, ctx, *, text):
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

    @commands.command()
    async def horoscope(self, ctx, *, text):  
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

    
    @commands.command()
    async def tarot(self, ctx):  
        await ctx.send(file=discord.File('Tarot/' + str(randint(1,77)) + '.jpg'))

    @commands.command()
    async def slots(slef, ctx): 
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

    @commands.command()
    async def joke(self, ctx):  
        headers = {
            "Accept": "application/json"
        }

        api_url = "https://icanhazdadjoke.com"
        r = requests.get(api_url, headers=headers)
        joke = json.loads(r.text)['joke']

        await ctx.send(joke)

    @commands.command()
    async def role(self, ctx, *, text):

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

    @commands.command() #THIS CODE IS REALLY WRONG BUT ITS FUNNY
    async def nani(self, ctx):
        api_url = "https://ranmoji.herokuapp.com/emojis/api/v.1.0/"
        response = requests.get(api_url)

        emojiHTMLEntity = json.loads(response.text)['emoji']

        emojiHTMLEntityHex = emojiHTMLEntity[3:len(emojiHTMLEntity) - 1].lower() + "0"
        emojiBytes = codecs.decode(emojiHTMLEntityHex, "hex")
        emojiUTF16 = emojiBytes.decode("utf-16", "ignore")

        await ctx.send(emojiUTF16)

    @commands.command(name='current-emotion')
    async def emotion(self, ctx):
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

    @commands.command(name='random-message')
    async def random_message(self, ctx, channel: discord.TextChannel = None): 
        if channel is None:
            channel = ctx.channel
        async with ctx.typing():
            d = self.random_date("4/24/2021 1:30 PM", str(date.today().month) + '/' + str(date.today().day) + '/' + str(date.today().year) + " 12:00 AM", random.random())
            d = parser.parse(d)
            messages = await channel.history(limit=1, around=d , oldest_first=False,).flatten()
        try:
            rand_message = messages[0]
            embed = discord.Embed(description=rand_message.content)
            embed.add_field(name="Random Message", value=f"[Jump]({rand_message.jump_url})")
            await ctx.send(embed=embed)
        except:
            await ctx.message.delete()  

    def random_date(self, start, end, prop):
        return self.str_time_prop(start, end, '%m/%d/%Y %I:%M %p', prop)

    def str_time_prop(self, start, end, time_format, prop):
        """Get a time at a proportion of a range of two formatted times.

        start and end should be strings specifying times formatted in the
        given format (strftime-style), giving an interval [start, end].
        prop specifies how a proportion of the interval to be taken after
        start.  The returned time will be in the specified format.
        """

        stime = time.mktime(time.strptime(start, time_format))
        etime = time.mktime(time.strptime(end, time_format))

        ptime = stime + prop * (etime - stime)

        return time.strftime(time_format, time.localtime(ptime))

    @commands.command()
    async def commands(self, ctx):
        helptext = "```"
        strList = []
        for command in self.bot.commands:
            strList.append(command.qualified_name)
        helptext += 'COMMANDS:\n\n'
        for command in sorted(strList):
            helptext += f"{command}\n"
        helptext+="```"
        await ctx.send(helptext)


