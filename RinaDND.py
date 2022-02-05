from RinasAssistant import *
from GameWords import *

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