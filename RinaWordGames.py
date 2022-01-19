from RinasAssistant import *

class RinaWordle(commands.Cog):

    wordle_start = None

    bot = None
    length = 5
    wordleWord = ''
    wordleDefinition = ''
    wordleActive = False
    wordleGuesses = 0
    valueArrCache = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    alpha = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M']
    alphaEmoji = ['🇶', '🇼', '🇪', '🇷', '🇹', '🇾', '🇺', '🇮', '🇴', '🇵', '🇦', '🇸', '🇩', '🇫', '🇬', '🇭', '🇯', '🇰', '🇱', '🇿', '🇽', '🇨', '🇻', '🇧', '🇳', '🇲']

    def __init__(self, bot, length = 5):
        self.bot = bot
        self.length = length

    @commands.command(name='wordle', help='Play Wordle')
    async def wordle_start(self, ctx):
        if not self.wordleActive:
            async with ctx.typing():
                await ctx.send("**🍥Welcome to Wordle Rina Edition©🍥**")

                url = "https://wordsapiv1.p.rapidapi.com/words/"
                querystring = {"random":"true","letters":self.length,"hasDetails":"typeOf"}
                headers = {
                    'x-rapidapi-host': "wordsapiv1.p.rapidapi.com",
                    'x-rapidapi-key': "b68f6a2307mshd055943a83ec8c8p1cd7e3jsn1bec9e8fec00"
                    }
                response = requests.get(url, headers=headers, params=querystring)
                data = json.loads(response.text)

                self.wordleWord = data["word"]
                self.valueArrCache = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                self.wordleDefinition = data["results"][0]["definition"]

                await ctx.send("**🍥Your word has been generated!🍥**")
                await ctx.send("**🍥Use !guess to guess a " + str(self.length) + " letter word!🍥**")

            self.wordleActive = True  
            self.wordleGuesses = 0   
            self.alphaEmoji = ['🇶', '🇼', '🇪', '🇷', '🇹', '🇾', '🇺', '🇮', '🇴', '🇵', '🇦', '🇸', '🇩', '🇫', '🇬', '🇭', '🇯', '🇰', '🇱', '🇿', '🇽', '🇨', '🇻', '🇧', '🇳', '🇲']
        else:
            await ctx.send("**🍥Wordle Rina Edition© is currently running! Guesses taken so far: " + str(self.wordleGuesses) + "🍥**")
            await ctx.send("**🍥Use !wordle-quit to quit🍥**")

    @commands.command(name='guess', help='Guess a Wordle word')
    async def wordle_guess(self, ctx, * ,text):
        if self.wordleActive:
            if len(text) == self.length:
                language = "en-us"
                word_id = text
                url = "https://od-api.oxforddictionaries.com:443/api/v2/lemmas/" + language + "/" + word_id.lower()
                response = requests.get(url, headers={"app_id": "7ffea31f", "app_key": "58e0caf11c3edf8553a2c8312ded7a41"})
                if response.status_code == 404 and not text.lower() == self.wordleWord:
                    await ctx.send("**🍥Not a word in the dictionary, try again!🍥**")
                else:
                    text = text.lower()
                    await ctx.send("**🍥Guess #" + str(self.wordleGuesses + 1) + "🍥**")
                    count = 0
                    for letter in text:
                        cVal = count + (self.wordleGuesses * self.length)
                        if self.wordleWord.__contains__(letter):
                            self.valueArrCache[cVal] = 1
                        else:
                            index = self.alpha.index(letter.upper())
                            self.alphaEmoji[index] = "  " + self.alpha[index] + "  "
                        if self.wordleWord[count] == text[count]:
                            self.valueArrCache[cVal] = 2
                        count += 1
                    win = False
                    if all(flag == 2 for (flag) in self.valueArrCache[self.wordleGuesses * self.length: (self.wordleGuesses * self.length) + self.length]):
                        win = True
                    self.wordleGuesses += 1
                    count = 0
                    outStr = ''

                    for val in self.valueArrCache:
                        if val == 0:
                            outStr += '⬜'
                        elif val == 1:
                            outStr += '🟨'
                        else:
                            outStr += '🟩'
                        count += 1
                        if count % self.length == 0:
                            alphaRange = range(0)
                            if count == self.length:
                                outStr += "           "
                                alphaRange = range(10)
                            if count == self.length * 3:
                                outStr += "               "
                                alphaRange = range(10, 19)
                            if count == self.length * 5:
                                outStr += "                      "
                                alphaRange = range(19, 26)
                            for i in alphaRange:
                                outStr += " " + self.alphaEmoji[i]
                            outStr += '\n'
                    await ctx.send(outStr) 
                    if win:
                        await ctx.send("**🍥Congratulations! You Win!🍥**") 
                        await ctx.send("Wordle " + str(self.wordleGuesses) + "/6") 
                        await ctx.send("**🍥Word was: " + self.wordleWord + "🍥**") 
                        await ctx.send("**🍥Definition: " + self.wordleDefinition + "🍥**") 
                        self.wordleActive = False
                    elif self.wordleGuesses == 6:
                        await ctx.send("**🍥You Lose WOW!🍥**" if random.random() >= 0.05 else "**🍥 " + ctx.message.author.mention + " are you serious? THAT was your last guess?🍥**") 
                        await ctx.send("**🍥Word was: " + self.wordleWord + "🍥**") 
                        await ctx.send("**🍥Definition: " + self.wordleDefinition + "🍥**") 
                        self.wordleActive = False
            else:
                await ctx.send("**🍥You must guess a " + str(self.length) + " letter word🍥**") 
        else:
            await ctx.send("**🍥Wordle Rina Edition© is not currently running🍥**")

    @commands.command(name='wordle-easy', help='Play Wordle')
    async def wordle_easy(self, ctx):
        if not self.wordleActive:
            async with ctx.typing():
                await ctx.send("**🍥Welcome to Wordle Rina Edition©🍥**")

                spl = self.wordleWordsList[0].split()
                self.wordleWord = spl[randint(0,len(spl) - 1)]
                self.wordleWord = self.wordleWord.lower()

                self.wordleDefinition = "No definition on easy mode"

                await ctx.send("**🍥Your word has been generated!🍥**")
                await ctx.send("**🍥Use !guess to guess a 5 letter word!🍥**")

            self.wordleActive = True  
            self.wordleGuesses = 0 
            self.alphaEmoji = ['🇶', '🇼', '🇪', '🇷', '🇹', '🇾', '🇺', '🇮', '🇴', '🇵', '🇦', '🇸', '🇩', '🇫', '🇬', '🇭', '🇯', '🇰', '🇱', '🇿', '🇽', '🇨', '🇻', '🇧', '🇳', '🇲']
        else:
            await ctx.send("**🍥Wordle Rina Edition© is currently running! Guesses taken so far: " + str(self.wordleGuesses) + "🍥**")
            await ctx.send("**🍥Use !wordle-quit to quit🍥**")

    @commands.command(name='wordle-quit', help='End Wordle')
    async def wordle_quit(self, ctx):
        self.wordleActive = False
        self.valueArrCache = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        await ctx.send("**🍥Wordle Rina Edition© has ended!🍥**")


  #Scrabble