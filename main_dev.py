import discord
import yt_dlp
import os
from time import sleep
from get_playlist import get_playlist_videos
import asyncio
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

ydl_opts = {
    'outtmpl': 'josh',
    'format': 'm4a/bestaudio/best',
    # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
    'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a',
    }],
}

urls = [()]

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

async def play(vc):
    global urls
    while len(urls) > 0:
        url = urls[0]
        print(url)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(url)
        vc.play(discord.FFmpegPCMAudio('josh.m4a'))
        await asyncio.sleep(int(url[1]))
        urls.remove(url)

initial = True

@client.event
async def on_message(message):
    global urls
    global initial

    if message.author == client.user:
        return

    if message.content.startswith('/skip'):
        urls.pop(0)
        vc = discord.utils.get(client.voice_clients, guild=message.guild)
        vc.stop()
        await play(vc)

    if message.content.startswith('/play'):
        url = message.content.split(' ')[1]

        try:
            vc = discord.utils.get(client.voice_clients, guild=message.guild)
            vc.stop()
        except:
            pass
        try:
            channel = message.author.voice.channel
            await channel.connect()
        except:
            pass
        vc = discord.utils.get(client.voice_clients, guild=message.guild)
        try:
            os.remove('josh.m4a')
        except:
            pass

        if not url.startswith('https://www.youtube.com/playlist?list='):
            urls.append(url)
            if initial:
                initial = False
                await play(vc)
        else:
            urls += get_playlist_videos(url)
            if initial:
                initial = False
                await play(vc)
        
        await message.channel.send("Josh is GIGA gay!")

client.run(os.getenv('DISCORD_TOKEN'))
