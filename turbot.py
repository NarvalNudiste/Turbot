"""
.. module:: turbot
   :platform: Windows, I guess
   :synopsis: simple music bot for discord

.. moduleauthor:: Narval Nudiste <guillaume.noguera@gmail.com>

"""

from __future__ import unicode_literals
import youtube_dl
import os
import sys
import asyncio
import json
import discord
from discord import opus
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import ydl
import random
import os

# global names
basePath = os.path.dirname(os.path.realpath(__file__));
ytplayer = None
voice = None
songs = []
currentSongId = 0
skipRequestB = False

# const
ytdl_opts = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': "mp3",
    'outtmpl': '%(id)s',
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'quiet': False,
    'no_warnings': False,
    'default_search': 'auto'
    }

#classes
class Song:
    '''Tiny class to store a youtube video url, as well as it's name. 
    video infos are pulled from youtube by the youtube-dl library.
    '''
    songCount = 0
    #song with title and location
    def __init__(self, name, url):
        self.name = name
        self.url = 'https://www.youtube.com/watch?v=' + url
        Song.songCount += 1
        self.infos = getVidInfo(self.url)
        print(f"info >> {self.infos['title']}")

    def __str__(self):
        duration = self.infos['duration']
        seconds = duration % 60
        minutes = round(duration / 60)
        return f"```{self.infos['title']} ({minutes}:{seconds})``` \b {self.url}"

with open(basePath + '\conf.json') as data:
    config = json.load(data)

yuna = config['invoker']

YOUTUBEKEY = 'AIzaSyBn1ND49GaqA9JFOeaE0b6IZqDuKlZ_Gaw'
DEVELOPER_KEY = "AIzaSyBn1ND49GaqA9JFOeaE0b6IZqDuKlZ_Gaw"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

client = discord.Client()

#onstart
@client.event
async def on_ready():
    """Pretty self-explanatory: prints turbot ID and loads the opus module

    :returns: nothing
    """
    print(client.user.name)
    print(client.user.id)
    print('------')
    #if sys.maxsize > 2**32:
    opus.load_opus('libopus-0.x64.dll')
    #else:
        #opus.load_opus('libopus-0.x86.dll')
    if  discord.opus.is_loaded():
       print("Opus module loaded")
    else:
       print("Error : opus module couldn't be loaded")
    print('------')

async def pause(player):
    """Pauses the current song
    :param player: the ytdl_player currently playing
    :type player: ytdl player from discord wrapper
    :returns: nothing
    """
    if player.is_playing():
        player.pause()

async def resume(player):
    """Resumes the current song

    :param player: the ytdl_player currently playing
    :type player: ytdl player from discord wrapper
    :returns: nothing
    """
    if not player.is_playing():
        player.resume()

def skip_request(skipRequested):
    """Utility func that should help to skip the current songs but actually does retard stuff and get called two times

    :param skipRequested: the flag used to skip stuff
    :type skipRequested: bool
    :returns: bool
    """
    if skipRequested is True:
        skipRequested = False
        return True
    else:
        return False

def getVidInfo(url):
    """func used to get youtube information; uses youtube_dl library

    :param url: the video url
    :type url: string
    :returns: the infos
    """
    yt = youtube_dl.YoutubeDL(ytdl_opts)
    infos = yt.extract_info(url, download=False, process=False)
    return infos

async def printHelp(client, message):
    """func used to print the help menu

    :param client: this bot
    :type client: discord.Client
    :param message: the message that just got posted in this sweet discord chan
    :type message: discord.Message
    :returns: nothing
    """
    m = f"""```############################################################################# \b
    # Welcome to the 1.0 turbot version
    # commands :
    # {yuna}queue *args* : queues a song to be played next (first youtube result) \b
    # {yuna}join : asks the bot to join the current vocal channel \b
    # {yuna}start : start to play the queue \b
    # {yuna}stop : stop playback process \b
    # {yuna}pause : pauses the playback process (wow) \b
    # {yuna}resume : resumes the playback process (much wow) \b
    # {yuna}viewqueue : display the current queue \b
    # {yuna}quit : kills the bot \b
    # {yuna}skip : skips the song, still broken tho \b
    # {yuna}gtfo : asks the bot to kindly leaves the channel \b
    # {yuna}emptyqueue : erases the current queue \b
    #############################################################################````"""
    await client.send_message(message.channel, m)

#defining commands
@client.event
async def on_message(message):
    """func used to process bot requests

    :param message: the message that just got posted in this sweet discord chan
    :type message: discord.Message
    :returns: nothing
    """
    if message.content.startswith(yuna):
        command = message.content[1:]
        print("command received : " + command)
        if message.content.startswith(yuna + 'queue'):
            #parses the request to find a video link, then add a song object with the url in it
            videoUrl = ydl.ytSearch(message.content[6:])
            global songs
            if random.randrange(10000) <= 1:
                #most needed feature
                songs.append(Song('[T]//','oHg5SJYRHA0'))
            else:
                songs.append(Song(message.content[6:], videoUrl))
            print(songs[len(songs)-1])
        elif command == 'join':
            try:
                global voice
                global ytplayer
                global currentSongId
                voice = await client.join_voice_channel(message.author.voice_channel)
            except:
                print(ytplayer.error)
                pass
        elif command == 'start':
            if voice is None:
                voice = await client.join_voice_channel(message.author.voice_channel)
            if len(songs) == 0:
                await client.send_message(message.channel, "```Error : ensure to queue something up before asking me to do stuff```")
            while songs:
                currentSong = songs.pop(0)
                beforeArgs = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
                ytplayer = await voice.create_ytdl_player(currentSong.url, ytdl_options = ytdl_opts, before_options = beforeArgs)
                ytplayer.start()
                await client.send_message(message.channel, f"```Currently playing : ```{str(currentSong)}")
                while not ytplayer.is_done():
                    global skipRequestB
                    if skip_request(skipRequestB):
                        ytplayer.stop()
                        await asyncio.sleep(3)
                    else:
                        await asyncio.sleep(1)
        elif command == 'skip':
            skipRequestB = True
        elif command == 'pause':
            await pause(ytplayer)
        elif command == 'resume':
            await resume(ytplayer)
        elif command == 'gtfo':
            await voice.disconnect()
        elif command == 'stop':
            ytplayer.pause()
        elif command == 'viewqueue':
            m = f'```Current queue : ({len(songs)} songs \b)'
            for i in range(len(songs)):
                m += (f"{i}: {songs[i].infos['title']} \b")
            m += ('```')
            await client.send_message(message.channel, m)
        elif command == 'quit':
            exit()
        elif command == 'help':
            await printHelp(client, message)
        elif command == 'emptyqueue':
            songs = []

#running
#client.run(config['token'])
