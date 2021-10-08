import os
from pathlib import Path
import atexit
import subprocess
import shlex
import discord
import io
from discord.ext import commands
from discord.opus import Encoder
from dotenv import load_dotenv
import os.path
import gtts
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
from gtts import gTTS
import gtts
import yt_dlp
from queue import Queue


class HelperFunctions:
    @staticmethod
    def remove_downloads(path):
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
        HelperFunctions.remove_downloads("TempDownloads/")
		
class FFmpegPCMAudio(discord.AudioSource):
    def __init__(self, source, *, executable='ffmpeg', pipe=False, stderr=None, before_options=None, options=None):
        stdin = None if not pipe else source
        args = [executable]
        if isinstance(before_options, str):
            args.extend(shlex.split(before_options))
        args.append('-i')
        args.append('-' if pipe else source)
        args.extend(('-f', 's16le', '-ar', '48000', '-ac', '2', '-loglevel', 'warning'))
        if isinstance(options, str):
            args.extend(shlex.split(options))
        args.append('pipe:1')
        self._process = None
        try:
            self._process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=stderr)
            self._stdout = io.BytesIO(
                self._process.communicate(input=stdin)[0]
            )
        except FileNotFoundError:
            raise discord.ClientException(executable + ' was not found.') from None
        except subprocess.SubprocessError as exc:
            raise discord.ClientException('Popen failed: {0.__class__.__name__}: {0}'.format(exc)) from exc
    def read(self):
        ret = self._stdout.read(Encoder.FRAME_SIZE)
        if len(ret) != Encoder.FRAME_SIZE:
            return b''
        return ret
    def cleanup(self):
        proc = self._process
        if proc is None:
            return
        proc.kill()
        if proc.poll() is None:
            proc.communicate()

        self._process = None


#LEGACY CODE
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
