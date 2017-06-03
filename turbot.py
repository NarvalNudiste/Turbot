from __future__ import unicode_literals
import youtube_dl
import os
import sys
import asyncio
import json

import urllib.request
import urllib.parse
import re

import discord
from discord import opus



from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

#vars
import os

basePath = os.path.dirname(os.path.realpath(__file__));
player = None

with open(basePath + '\conf.json') as data:
    config = json.load(data)

yuna = config['invoker']

YOUTUBEKEY = 'AIzaSyBn1ND49GaqA9JFOeaE0b6IZqDuKlZ_Gaw'
DEVELOPER_KEY = "AIzaSyBn1ND49GaqA9JFOeaE0b6IZqDuKlZ_Gaw"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

#youtube-dl part
ydl_opts = {
    'format' : 'bestaudio/best',
    'postprocessors': [{'key': 'FFmpegExtractAudio',
                        'preferredcodec' : 'mp3',
						'preferredquality': '320',}],
    'outtmpl':'/temp/song.%(ext)s'
            }

#simple request to avoid youtube api data usage
def ytSearch(searchString):
    #returns the video id of a youtube search
    query_string = urllib.parse.urlencode({"search_query" : searchString})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    return search_results[0]


client = discord.Client()

@client.event
async def on_ready():

    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    #if sys.maxsize > 2**32:
    opus.load_opus('libopus-0.x64.dll')
    #else:
        #opus.load_opus('libopus-0.x86.dll')
    if  discord.opus.is_loaded():
       print("opus loaded")

#defining commands

@client.event
async def on_message(message):
    if message.content.startswith(yuna):
        if message.content.startswith('!test'):
            counter = 0
            tmp = await client.send_message(message.channel, 'Calculating messages...')
            async for log in client.logs_from(message.channel, limit=100):
                if log.author == message.author:
                    counter += 1
            await client.edit_message(tmp, 'You have {} messages.'.format(counter))

        elif message.content.startswith('!sleep'):
            await asyncio.sleep(5)
            await client.send_message(message.channel, 'Done sleeping')

        elif message.content.startswith('!download'):
            await client.send_message(message.channel, 'Searching youtube video .. ')
            videoId = ytSearch(message.content[-9:])
            await client.send_message(message.channel, 'Buffering ..')
            with youtube_dl.YoutubeDL(ydl_opts) as yd:
                url = 'https://www.youtube.com/watch?v=' + videoId
                yd.download([url])
        elif message.content.startswith('!quit'):
            exit()
        elif message.content.startswith('!joinme'):
            try:
                global player
                voice = await client.join_voice_channel(message.author.voice_channel)
                player = voice.create_ffmpeg_player(basePath + '\music.mp3')
                player.start()
            except:
                print(player.error);
                pass
        elif message.content.startswith('!ping'):
            await client.send_message(message.channel, 'pong')
        elif message.content.startswith('!titsorgtfo'):
            await voice.disconnect()
        elif message.content.startswith('!stop'):
            await player.stop()

#running
client.run(config['token'])
