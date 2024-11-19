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

urls = []

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/play'):
        url = message.content.split(' ')[1]

        try:
            channel = message.author.voice.channel
            await channel.connect()
        except:
            pass

        vc = discord.utils.get(client.voice_clients, guild=message.guild)

        ffmpeg_options = {'options': '-vn'}
        ydl_opts = {'format': 'bestaudio/best'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            song_info = ydl.extract_info(url, download=False)
        vc.play(discord.FFmpegPCMAudio(song_info["url"], **ffmpeg_options))
        while vc.is_playing() or vc.is_paused():
            await asyncio.sleep(1)

        await message.channel.send("Josh is GIGA gay!")

client.run(os.getenv('DISCORD_TOKEN'))
