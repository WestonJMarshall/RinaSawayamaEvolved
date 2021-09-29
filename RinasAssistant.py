import os
from pathlib import Path
import atexit
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os.path
import youtube_dl
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