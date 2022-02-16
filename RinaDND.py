from RinasAssistant import *
from GameWords import *
from io import BytesIO

class RinaDND(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="dnd-spell")
    async def dnd_spell(self, ctx, *, text): 
        async with ctx.typing():
            await ctx.send("Loading spell details")
            if text.lower().__contains__("abi-dalzim's horrid wilting"):
                searchTerm = text.replace(' ', '%20')
                searchTerm = searchTerm.lower()
                url = "https://5etools-mirror-1.github.io/spells.html#" + searchTerm
                browser = webdriver.Chrome(executable_path=r'C:\Users\Weston Marshall\Desktop\RinaSawayamaEvolved\RinaSawayamaEvolved\WebDriver\chromedriver.exe', options=chrome_options)
                browser.get(url)
                element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "stats"))
                )
                WebDriverWait(browser, 10).until_not(EC.text_to_be_present_in_element((By.CLASS_NAME, "stats"), "Select a spell from the list to view it here"))
                data = element.text
                message = data
                await ctx.send(message[0:1990])
                return

            searchTerm = text.replace(' ', '%20')
            searchTerm = text.replace('/', '%2f')
            searchTerm = searchTerm.lower()

            searchTerms = [searchTerm, searchTerm + '_phb', searchTerm + '_xge', searchTerm + '_ftd', searchTerm + '_tce', searchTerm + '_scc', searchTerm + '_idrotf', searchTerm + '_egw', searchTerm + '_ai', searchTerm + '_ggr']

            data = "Abi-Dalzim's Horrid Wilting"

            count = 0
            while data.__contains__("Abi-Dalzim's Horrid Wilting") and count < len(searchTerms):
                url = "https://5etools-mirror-1.github.io/spells.html#" + searchTerms[count]
                browser = webdriver.Chrome(executable_path=r'C:\Users\Weston Marshall\Desktop\RinaSawayamaEvolved\RinaSawayamaEvolved\WebDriver\chromedriver.exe', options=chrome_options)
                browser.get(url)
                element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "stats"))
                )
                WebDriverWait(browser, 10).until_not(EC.text_to_be_present_in_element((By.CLASS_NAME, "stats"), "Select a spell from the list to view it here"))
                data = element.text
                count += 1

            if count == len(searchTerms):
                message = "No entry found"
            else:
                message = data
            await ctx.send(message[0:1990])

    def cleanhtml(self, raw_html, cleaner):
        cleantext = re.sub(cleaner, '', raw_html)
        return cleantext

    @commands.command(name="mood-board")
    async def mood_board(self, ctx): 
        await ctx.send(file=discord.File("MoodBoard/MoodBoardOutput.png"))

    @commands.command(name="mood-board-paste")
    async def mood_board_paste(self, ctx, *, text): 
        splitText = text.split()
        posX = 0
        posY = 0
        scale = 1
        url = "https://bitsofco.de/content/images/2018/12/broken-1.png"
        for part in splitText:
            if (part.__contains__("x") or part.__contains__("X")) and not part.__contains__("http") and not part.__contains__("/"):
                posX = int(re.search(r'\d+', part).group())
            elif (part.__contains__("y")or part.__contains__("Y")) and not part.__contains__("http") and not part.__contains__("/"):
                posY = int(re.search(r'\d+', part).group())
            elif (part.__contains__("scale") or part.__contains__("Scale")) and not part.__contains__("http") and not part.__contains__("/"):
                result = re.findall(r"[-+]?\d*\.\d+|\d+", part)
                scale = float(self.convert(result))
            else:
                url = part
        response = requests.get(url)
        inputImage = Image.open(BytesIO(response.content))
        outputImage = Image.open("MoodBoard/MoodBoard.png")
        scaledVal = (round(inputImage.size[0]*scale), round(inputImage.size[1]*scale))
        inputImage = inputImage.resize(scaledVal)
        outputImage.paste(inputImage, (posX, posY))
        outputImage.save("MoodBoard/MoodBoard.png")
        outputImage.save("MoodBoard/MoodBoardOutput.png")
        while os.path.getsize("MoodBoard/MoodBoardOutput.png") > 7000000:
            outputImage.resize(round(outputImage.size[0]*0.75), round(outputImage.size[1]*0.75))
            outputImage.save("MoodBoard/MoodBoardOutput.png")
        await ctx.send(file=discord.File("MoodBoard/MoodBoardOutput.png"))

    @commands.command(name="mood-board-reset")
    async def mood_board_reset(self, ctx): 
        inputImage = Image.open("MoodBoard/Reset.png")
        outputImage = Image.open("MoodBoard/MoodBoard.png")
        outputImage.paste(inputImage, (0, 0))
        outputImage.save("MoodBoard/MoodBoard.png")
        outputImage.save("MoodBoard/MoodBoardOutput.png")
        await ctx.send("Board Reset :)")

    def convert(self, s):
        new = ""
        for x in s:
            new += x 
        return new