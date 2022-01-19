from RinasAssistant import *
from GameWords import *

class RinaWordle(commands.Cog):

    bot = None
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


class RinaScrabble(commands.Cog):

    letters = ['a','b','c','d','e','f','g','h','i','j','l','m','n','o']
    numbers = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15']

    lettersPoints = {'a':1,'b':3,'c':3,'d':2,'e':1,'f':4,'g':2,'h':4,'i':1,'j':8,'k':5,'l':1,'m':3,'n':1,'o':1,'p':3,'q':10,'r':1,'s':1,'t':1,'u':1,'v':4,'w':4,'x':8,'y':4,'z':10}
    lettersCountsStatic = {'a':9,'b':2,'c':2,'d':4,'e':12,'f':2,'g':3,'h':2,'i':9,'j':1,'k':1,'l':4,'m':2,'n':6,'o':8,'p':2,'q':1,'r':6,'s':4,'t':6,'u':4,'v':2,'w':2,'x':1,'y':2,'z':1}
    lettersCounts = lettersCountsStatic

    class ScrabblePlayer:
        discordInfo = None
        points = 0
        currentLetters = []

        def __init__(self, discordInfo):
            self.discordInfo = discordInfo

    scrabbleActive = False
    scrabblePlayers = 0
    scrabbleRotation = 0
    scrabbleTurn = 0
    players = []
    boardStatic = {'a1': '*w3', 'a2': '*', 'a3': '*', 'a4': '*l2', 'a5': '*', 'a6': '*', 'a7': '*', 'a8': '*w3', 'a9': '*', 'a10': '*', 'a11': '*', 'a12': '*l2', 'a13': '*', 'a14': '*', 'a15': '*w3', 'b1': '*', 'b2': '*w2', 'b3': '*', 'b4': '*', 'b5': '*', 'b6': '*l3', 'b7': '*', 'b8': '*', 'b9': '*', 'b10': '*l3', 'b11': '*', 'b12': '*', 'b13': '*', 'b14': '*w2', 'b15': '*', 'c1': '*', 'c2': '*', 'c3': '*w2', 'c4': '*', 'c5': '*', 'c6': '*', 'c7': '*l2', 'c8': '*', 'c9': '*l2', 'c10': '*', 'c11': '*', 'c12': '*', 'c13': '*w2', 'c14': '*', 'c15': '*', 'd1': '*l2', 'd2': '*', 'd3': '*', 'd4': '*w2', 'd5': '*', 'd6': '*', 'd7': '*', 'd8': '*l2', 'd9': '*', 'd10': '*', 'd11': '*', 'd12': '*w2', 'd13': '*', 'd14': '*', 'd15': '*l2', 'e1': '*', 'e2': '*', 'e3': '*', 'e4': '*', 'e5': '*w2', 'e6': '*', 'e7': '*', 'e8': '*', 'e9': '*', 'e10': '*', 'e11': '*w2', 'e12': '*', 'e13': '*', 'e14': '*', 'e15': '*', 'f1': '*', 'f2': '*l3', 'f3': '*', 'f4': '*', 'f5': '*', 'f6': '*l3', 'f7': '*', 'f8': '*', 'f9': '*', 'f10': '*l3', 'f11': '*', 'f12': '*', 'f13': '*', 'f14': '*l3', 'f15': '*', 'g1': '*', 'g2': '*', 'g3': '*l2', 'g4': '*', 'g5': '*', 'g6': '*', 'g7': '*l2', 'g8': '*', 'g9': '*l2', 'g10': '*', 'g11': '*', 'g12': '*', 'g13': '*l2', 'g14': '*', 'g15': '*', 'h1': '*w3', 'h2': '*', 'h3': '*', 'h4': '*l2', 'h5': '*', 'h6': '*', 'h7': '*', 'h8': '*w2', 'h9': '*', 'h10': '*', 'h11': '*', 'h12': '*l2', 'h13': '*', 'h14': '*', 'h15': '*w3', 'i1': '*', 'i2': '*', 'i3': '*l2', 'i4': '*', 'i5': '*', 'i6': '*', 'i7': '*', 'i8': '*', 'i9': '*', 'i10': '*', 'i11': '*', 'i12': '*', 'i13': '*l2', 'i14': '*', 'i15': '*', 'j1': '*', 'j2': '*l3', 'j3': '*', 'j4': '*', 'j5': '*', 'j6': '*l3', 'j7': '*', 'j8': '*', 'j9': '*', 'j10': '*l3', 'j11': '*', 'j12': '*', 'j13': '*', 'j14': '*l3', 'j15': '*', 'k1': '*', 'k2': '*', 'k3': '*', 'k4': '*', 'k5': '*w2', 'k6': '*', 'k7': '*', 'k8': '*', 'k9': '*', 'k10': '*', 'k11': '*w2', 'k12': '*', 'k13': '*', 'k14': '*', 'k15': '*', 'l1': '*l2', 'l2': '*', 'l3': '*', 'l4': '*w2', 'l5': '*', 'l6': '*', 'l7': '*l2', 'l8': '*', 'l9': '*l2', 'l10': '*', 'l11': '*', 'l12': '*w2', 'l13': '*', 'l14': '*', 'l15': '*l2', 'm1': '*', 'm2': '*', 'm3': '*w2', 'm4': '*', 'm5': '*', 'm6': '*', 'm7': '*l2', 'm8': '*', 'm9': '*l2', 'm10': '*', 'm11': '*', 'm12': '*', 'm13': '*w2', 'm14': '*', 'm15': '*', 'n1': '*', 'n2': '*w2', 'n3': '*', 'n4': '*', 'n5': '*', 'n6': '*l3', 'n7': '*', 'n8': '*', 'n9': '*', 'n10': '*l3', 'n11': '*', 'n12': '*', 'n13': '*', 'n14': '*w2', 'n15': '*', 'o1': '*w3', 'o2': '*', 'o3': '*', 'o4': '*l2', 'o5': '*', 'o6': '*', 'o7': '*', 'o8': '*w3', 'o9': '*', 'o10': '*', 'o11': '*', 'o12': '*l2', 'o13': '*', 'o14': '*', 'o15': '*w3'}
    board = boardStatic
    letterBag = []

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='scrabble')
    async def scrabble(self, ctx):
        if not self.scrabbleActive and self.scrabblePlayers == 0:
            async with ctx.typing():
                await ctx.send("**🌟Welcome to Scrabble Rina Edition©🌟**")
                await ctx.send("**🌟" + ctx.message.author.nick + " has joined the game🌟**")
                self.players.append(self.ScrabblePlayer(ctx.message.author))
                self.scrabblePlayers += 1
                await ctx.send("**🌟Use !scrabble to join the game!🌟**")
                await ctx.send("**🌟When 2-4 players have joined, start the game with !scrabble-start🌟**")
        elif not self.scrabbleActive and self.scrabblePlayers < 4:
            await ctx.send("**🌟" + ctx.message.author.nick + " has joined the game🌟**")
            self.players.append(self.ScrabblePlayer(ctx.message.author))
            self.scrabblePlayers += 1
            await ctx.send("**🌟" + str(self.scrabblePlayers) + " waiting to play!🌟**")
        elif not self.scrabbleActive:
            await ctx.send("**🌟Sorry, already 4 players!🌟**")
        else:
            await ctx.send("**🌟Game currently in progress, " + str(self.scrabblePlayers) + " Players, Turn #" + str(self.scrabbleTurn) + "🌟**")
            await ctx.send("**🌟!scrabble-quit to quit🌟**")

    @commands.command(name='scrabble-start')
    async def scrabble_start(self, ctx):
        if self.scrabbleActive:
            await ctx.send("**🌟Game currently in progress, " + str(self.scrabblePlayers) + " Players, Turn #" + str(self.scrabbleTurn) + "🌟**")
        else:
            if len([author for author in self.players if author == ctx.message.author]) == 0:
                await ctx.send("**🌟You are not a player in this Scrabble game and cannot start the game🌟**")
            elif self.scrabblePlayers > 4 or self.scrabblePlayers < 2:
                await ctx.send("**🌟There are not between 2-4 memebers in the Scrabble lobby!🌟**")
            else:
                await ctx.send("**🌟Starting Game!🌟**")
                self.scrabbleTurn = 1
                self.scrabbleActive = True
                await ctx.send("**🌟Player 1 is " + self.players[self.scrabbleRotation].discordInfo.nick + "🌟**")
                await ctx.send("**🌟Use !scrabble-word + {STARTING TILE} + {DIRECTION ←↑→↓} + {WORD}🌟**")

    @commands.command(name='scrabble-word')
    async def scrabble_word(self, ctx, * , text):
        text = text.lower()
        if not self.scrabbleActive:
            await ctx.send("**🌟No game running!🌟**")
        else:
            if not self.players[self.scrabbleRotation].discordInfo == ctx.message.author:
                await ctx.send("**🌟It is not your turn!🌟**")
                await ctx.send("**🌟Current player is " + self.players[self.scrabbleRotation].discordInfo.nick + "🌟**")
            else:
                textParts = text.split()
                if len(textParts) != 3:
                    await ctx.send("**🌟You did not type all 3 required properties!🌟**")
                    return
                elif not self.board.__contains__(textParts[0]):
                    await ctx.send("**🌟Invalid tile!🌟**")
                    return
                elif not any(letter in textParts[1] for letter in '→↓'):
                    await ctx.send("**🌟Direction must contain one of the →↓ symbols🌟**")
                    return
                elif not ScrabbleWordList.__contains__(textParts[2]):
                    await ctx.send("**🌟" + textParts[2] + " is not a word in the Rina Scrabble dictionary!🌟**")
                    return
                else:
                    validityResult = self.validate_placement(textParts[0], textParts[1], textParts[2])
                    if validityResult[0] == "valid":
                        validityResult = self.validate_words(validityResult[1], textParts[2], textParts[1])
                        if not validityResult[0] == "valid":
                            await ctx.send(validityResult[0])
                            return
                        else:



                    else:
                        await ctx.send(validityResult[0])
                        return

    def validate_placement(self, startingTile, direction, word):
        tiles = []
        tiles.append(startingTile)

        for _ in word[0 : len(word) - 1]:
            nextTile = tiles[len(tiles) - 1]

            tileComponents = re.split('(\d+)', nextTile)

            if direction.__contains__('→'):
                if tileComponents[0] == 'o':
                    return ["**🌟→ is not a valid direction for this word, not enough space!🌟**", None]
                tileComponents[0] = self.letters[self.letters.index(tileComponents[0]) + 1]
                tiles.append(tileComponents[0] + tileComponents[1])
            elif direction.__contains__('↓'):
                if tileComponents[1] == '15':
                    return ["**🌟↓ is not a valid direction for this word, not enough space!🌟**", None]
                tileComponents[1] = self.numbers[self.numbers.index(tileComponents[1]) + 1]
                tiles.append(tileComponents[0] + tileComponents[1])

        if self.scrabbleTurn == 1 and self.scrabbleRotation == 0:
            if not tiles.__contains__('h8'):
                return "**🌟The first word placed must go through the center tile (H8)!🌟**"
        
        for i in range(len(tiles)):
            if not self.board[tiles[i]] == word[i] and not self.players[self.scrabbleRotation].currentLetters.__contains__(word[i]):
                return ["**🌟You do not have the letters to make that word!🌟**", tiles]

        return ["valid", None]

    def validate_words(self, tiles, word, direction):   
        allWords = []     
        for i in range(len(tiles)):
            validArr = []
            if direction.__contains__('↓'):
                if i == 0 and self.board[tiles[i]].__contains__('*'):
                    validArr = [self.validate_word_branch_left(tiles[i], "", direction, word, tiles), self.validate_word_branch_up(tiles[i], "", direction, word, tiles)]
                elif i == 0:
                    validArr = [self.validate_word_branch_up(tiles[i], "", direction, word, tiles)]
                else:
                    validArr = [self.validate_word_branch_left(tiles[i], "", direction, word, tiles)]
            else:
                if i == 0 and self.board[tiles[i]].__contains__('*'):
                    validArr = [self.validate_word_branch_left(tiles[i], "", direction, word, tiles), self.validate_word_branch_up(tiles[i], "", direction, word, tiles)]
                elif i == 0:
                    validArr = [self.validate_word_branch_left(tiles[i], "", direction, word, tiles)]
                else:
                    validArr = [self.validate_word_branch_up(tiles[i], "", direction, word, tiles)]

            if any(x for x in validArr if not x[0] == 'valid'):
                for x in validArr:  
                    if not x[0] == 'valid':
                        return [x[0], None]
            else:
                for x in validArr:  
                    if not x[1] == "":
                        allWords.append(x[1])
        return ["valid", allWords]
                

        
    def validate_word_branch_left(self, startTile, buildWord, direction, inputWord, inputTiles):
        tileComponents = re.split('(\d+)', startTile)
        if not tileComponents[0] == 'a':
            nextTile = self.letters[self.letters.index(tileComponents[0]) - 1] + tileComponents[1]
            if not self.board[nextTile].__contains__('*'):
                buildWord.insert(0, self.board[nextTile])
                self.validate_word_branch_left(nextTile, buildWord)
            else:
                return self.validate_word_branch_right(startTile, buildWord, direction, inputWord, inputTiles)
        else:
            return self.validate_word_branch_right(startTile, buildWord, direction, inputWord, inputTiles)

    def validate_word_branch_right(self, startTile, buildWord, direction, inputWord, inputTiles):
        tileComponents = re.split('(\d+)', startTile)
        if not tileComponents[0] == 'o':
            nextTile = self.letters[self.letters.index(tileComponents[0]) + 1] + tileComponents[1]
            if not self.board[nextTile].__contains__('*'):
                buildWord.append(self.board[nextTile])
                return self.validate_word_branch_right(nextTile, buildWord)
            elif direction == '→' and inputTiles.__contains__(nextTile):
                buildWord.append(inputWord[inputTiles.index(nextTile)])
                return self.validate_word_branch_right(nextTile, buildWord)
            else:
                if ScrabbleWordList.__contains__(buildWord):
                    return ["valid", buildWord]
                elif len(buildWord) == 1:
                    return ["valid", ""]
                else:
                    return ["**🌟" + buildWord + " is not a word in the Rina Scrabble dictionary!🌟**", None]
        else:
            if ScrabbleWordList.__contains__(buildWord):
                return ["valid", buildWord]
            elif len(buildWord) == 1:
                return ["valid", ""]
            else:
                return ["**🌟" + buildWord + " is not a word in the Rina Scrabble dictionary!🌟**", None]

    def validate_word_branch_up(self, startTile, buildWord, direction, inputWord, inputTiles):
        tileComponents = re.split('(\d+)', startTile)
        if not tileComponents[0] == 'a':
            nextTile = tileComponents[0] + self.numbers[self.numbers.index(tileComponents[1]) - 1]
            if not self.board[nextTile].__contains__('*'):
                buildWord.insert(0, self.board[nextTile])
                self.validate_word_branch_up(nextTile, buildWord)
            else:
                return self.validate_word_branch_down(startTile, buildWord, direction, inputWord, inputTiles)
        else:
            return self.validate_word_branch_down(startTile, buildWord, direction, inputWord, inputTiles)

    def validate_word_branch_down(self, startTile, buildWord, direction, inputWord, inputTiles):
        tileComponents = re.split('(\d+)', startTile)
        if not tileComponents[1] == '15':
            nextTile = tileComponents[0] + self.numbers[self.numbers.index(tileComponents[1]) + 1]
            if not self.board[nextTile].__contains__('*'):
                buildWord.append(self.board[nextTile])
                return self.validate_word_branch_down(nextTile, buildWord)
            elif direction == '↓' and inputTiles.__contains__(nextTile):
                buildWord.append(inputWord[inputTiles.index(nextTile)])
                return self.validate_word_branch_down(nextTile, buildWord)
            else:
                if ScrabbleWordList.__contains__(buildWord):
                    return ["valid", [buildWord, points]]
                elif len(buildWord) == 1:
                    return ["valid", ""]
                else:
                    return ["**🌟" + buildWord + " is not a word in the Rina Scrabble dictionary!🌟**", None]
        else:
            if ScrabbleWordList.__contains__(buildWord):
                return ["valid", buildWord, points]
            elif len(buildWord) == 1:
                return ["valid", ""]
            else:
                return ["**🌟" + buildWord + " is not a word in the Rina Scrabble dictionary!🌟**", None]





    def draw_letters():
        print("not implemented")

    def knockout():
        print("not implemented")

    def show_letters():
        print("not implemented")

    @commands.command(name='scrabble-quit')
    async def scrabble_quit(self, ctx):
        await ctx.send("**🌟Game ended!🌟**")
        self.board = self.boardStatic
        self.scrabbleActive = False
        self.players = []
        self.scrabblePlayers = 0
        self.scrabbleTurn = 0
        self.scrabbleRotation = 0

