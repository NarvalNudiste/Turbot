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
#vars
import os

basePath = os.path.dirname(os.path.realpath(__file__));
player = None
voice = None
currentSongId = 0

class Song:
    songCount = 0
    #song with title and location
    def __init__(self, _name, _path):
        self.name = _name
        self.path = _path
        Song.songCount += 1
    def __str__(self):
        return 'Song : ' + self.name + ' - Loc : ' + self.path


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

#defining commands
@client.event
async def on_message(message):
    if message.content.startswith(yuna):
        print('command - ', message.content[1:])
        if message.content.startswith(yuna +'queue'):
            await client.send_message(message.channel, 'Searching youtube video .. ')
            videoId = ydl.ytSearch(message.content[-9:])
            await client.send_message(message.channel, 'Buffering ..')
            global currentSongId
            ydl_opts = {
                'format' : 'bestaudio/best',
                'postprocessors': [{'key': 'FFmpegExtractAudio',
                'preferredcodec' : 'mp3',
                'preferredquality': '320',}],
                'outtmpl': basePath + '/songs/song' + str(currentSongId) + '.%(ext)s'
                                        }
            with youtube_dl.YoutubeDL(ydl_opts) as yd:
                url = 'https://www.youtube.com/watch?v=' + videoId
                yd.download([url])
                currentSongId+=1
        elif message.content[1:] == 'quit':
            exit()
        elif message.content[1:] == 'join':
            try:
                global voice
                voice = await client.join_voice_channel(message.author.voice_channel)
            except:
                pass
        elif message.content[1:] == 'start':
            try:
                global player
                player = voice.create_ffmpeg_player(basePath + '\songs\song'+ str(currentSongId - 1) +'.mp3')
                player.start()
            except:
                pass
        elif message.content[1:] == 'ping':
            await client.send_message(message.channel, 'pong')
        elif message.content[1:] == 'titsorgtfo':
            await voice.disconnect()
        elif message.content[1:] == 'stop':
            player.pause()

#running
client.run(config['token'])
