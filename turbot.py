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
import os

# global names
basePath = os.path.dirname(os.path.realpath(__file__));
ytplayer = None
voice = None
songs = []
currentSongId = 0

# const
ytdl_opts = {
    'source_address': '0.0.0.0',
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': "mp3",
    'outtmpl': '%(id)s',
    'noplaylist': False,
    'yesplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': True,
    'quiet': True,
    'no_warnings': True,
    'outtmpl': "data/audio/cache/%(id)s",
    'default_search': 'auto'
    }

#classes
class Song:
    songCount = 0
    #song with title and location
    def __init__(self, name, url):
        self.name = name
        self.url = 'https://www.youtube.com/watch?v=' + url
        Song.songCount += 1
    def __str__(self):
        return f'Song : {self.name} - url : {self.url}'

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

async def watch(player, songId, bArgs):
    while not player.is_done():
            await asyncio.sleep(1)
    if len(songs) > songId + 1:
        songId += 1
        ytplayer = await voice.create_ytdl_player(songs[songId].id, ytdl_options = ytdl_opts, before_options = bArgs)
        await watch(ytplayer, songId, bArgs)

#defining commands
@client.event
async def on_message(message):
    if message.content.startswith(yuna):
        print('command - ', message.content[1:])
        if message.content.startswith(yuna + 'queue'):
            videoUrl = ydl.ytSearch(message.content[6:])
            global songs
            songs.append(Song(message.content[6:], videoUrl))
            print(songs[len(songs)-1])
        elif message.content[1:] == 'join':
            try:
                global voice
                global ytplayer
                global currentSongId
                voice = await client.join_voice_channel(message.author.voice_channel)
            except:
                print(ytplayer.error)
                pass
        elif message.content[1:] == 'start':
            if voice is None:
                voice = await client.join_voice_channel(message.author.voice_channel)
            while songs:
                currentSong = songs.pop(0)
                beforeArgs = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
                ytplayer = await voice.create_ytdl_player(currentSong.url, ytdl_options = ytdl_opts, before_options = beforeArgs)
                ytplayer.start()
                while not ytplayer.is_done():
                    await asyncio.sleep(1)
        elif message.content[1:] == 'gtfo':
            await voice.disconnect()
        elif message.content[1:] == 'stop':
            ytplayer.pause()
        elif message.content[1:] == 'viewQueue':
            await client.send_message(message.channel, 'Current queue :')
            for i in range(len(songs)):
                await client.send_message(message.channel, str(i) +  ':' + str(songs[i]))
        elif message.content[1:] == 'quit':
            exit()


#running
client.run(config['token'])
