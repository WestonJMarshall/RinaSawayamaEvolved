import os
from pathlib import Path
import atexit
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os.path
import js2py #JavaScript -> Python converter
import youtube_dl
import pyxivapi
from pyxivapi.models import Filter, Sort
import requests
import json
import codecs
from collections import OrderedDict
import re
import random
import asyncio
from queue import Queue

class HelperFunctions:
    @staticmethod
    def Remove(path):
        #Check if folder path exists, create one if it doesn't
        root = Path().absolute()
        full = root.joinpath(path)
        if not(os.path.exists(full) and os.path.isdir(full)):
            os.makedirs(full)
        #Delete all files in the path
        files = os.listdir(full)
        for file in files:
            fileFull = full.joinpath(file)
            os.remove(fileFull)

    @staticmethod
    def exit_handler():
        HelperFunctions.Remove("TempDownloads/")

vocodesVoices = {
	'altman': "sam-altman",
	'arnold': "arnold-schwarzenegger",
	'attenborough': "david-attenborough",
	'ayoade': "richard-ayoade",
	'barker': "bob-barker",
	'bart': "bart-simpson",
	'bill': "bill-clinton",
	'boss': "the-boss",
	'brimley': "wilford-brimley",
	'broomstick': "boomstick",
	'bush': "george-w-bush",
	'carter': "jimmy-carter",
	'cooper': "anderson-cooper",
	'cramer': "jim-cramer",
	'cranston': "bryan-cranston",
	'cross': "david-cross",
	'darth': "darth-vader",
	'deen': "paula-deen",
	'degrasse': "neil-degrasse-tyson",
	'dench': "judi-dench",
	'devito': "danny-devito",
	'ferguson': "craig-ferguson",
	'gates': "bill-gates",
	'gottfried': "gilbert-gottfried",
	'graham': "paul-graham",
	'hillary': "hillary-clinton",
	'homer': "homer-simpson",
	'jones': "james-earl-jones",
	'keeper': "crypt-keeper",
	'king': "larry-king",
	'krabs': "mr-krabs",
	'lee': "christopher-lee",
	'lisa': "lisa-simpson",
	'luckey': "palmer-luckey",
	'mcconnell': "mitch-mcconnell",
	'nimoy': "leonard-nimoy",
	'nixon': "richard-nixon",
	'nye': "bill-nye",
	'obama': "barack-obama",
	'oliver': "john-oliver",
	'palin': "sarah-palin",
	'penguinz0': "moistcr1tikal",
	'phil': "dr-phil-mcgraw",
	'reagan': "ronald-reagan",
	'rickman': "alan-rickman",
	'rogers': "fred-rogers",
	'rosen': "michael-rosen",
	'saruman': "saruman",
	'scout': "scout",
	'shapiro': "ben-shapiro",
	'shohreh': "shohreh-aghdashloo",
	'simmons': "j-k-simmons",
	'snake': "solid-snake",
	'snape': "severus-snape",
	'sonic': "sonic",
	'spongebob': "spongebob-squarepants",
	'squidward': "squidward",
	'stein': "ben-stein",
	'takei': "george-takei",
	'thiel': "peter-thiel",
	'trevor': "trevor-philips",
	'trump': "donald-trump",
	'tucker': "tucker-carlson",
	'tupac': "tupac-shakur",
	'vegeta': "vegeta",
	'white': "betty-white",
	'wiseau': "tommy-wiseau",
	'wizard': "wizard",
	'yugi': "yami-yugi",
	'zuckerberg': "mark-zuckerberg"
}

vocodesVoice = vocodesVoices['obama']

def RiTaAccess():
    #Get RiTa Source code
    jsCode = requests.get("https://unpkg.com/rita")

    #Write it to a JavaScript file
    file = open("RiTa.js", "w") 
    file.write(jsCode.text) 
    file.close() 

    #Convert to python code in a temporary variable
    tempRiTaCode = js2py.eval_js6("RiTa.js")
    return tempRiTaCode
